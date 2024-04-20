import sys
import pydicom
import logging  # Import logging module
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap

class DICOMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple DICOM Viewer")

        # UI Elements
        self.image_label = QLabel()
        self.metadata_display = QLabel()

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.metadata_display)
        self.setCentralWidget(central_widget)

        # Menu action
        open_action = self.menuBar().addAction("Open DICOM")
        open_action.triggered.connect(self.open_dicom_file)

    def open_dicom_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", filter="DICOM Files (*.dcm)")
        if file_path:
            try:
                metadata = load_dicom_metadata(file_path)
                self.display_image(metadata['Pixel Data'])
                self.display_metadata(metadata)
            except (pydicom.errors.InvalidDicomError, KeyError, ValueError) as e:
                self.show_error(f"Error loading DICOM file: {str(e)}")

    def display_image(self, pixel_data):
        if not self.convert_pixel_data_to_image(pixel_data):
            self.show_error("Error converting image data.")

    def convert_pixel_data_to_image(self, pixel_data):
        """Converts pixel_data to a QPixmap. 
           Implement your conversion logic here (potentially using Pillow or OpenCV) 
        """
        try:
            # Placeholder - Replace this with your image conversion logic 
            pixmap = QPixmap()
            pixmap.loadFromData(pixel_data) 
            self.image_label.setPixmap(pixmap)
            return True  # Indicate success
        except Exception as e:
            logging.error(f"Image conversion error: {str(e)}") 
            return False

    def display_metadata(self, metadata):
        # ... (Same as before)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)
        
    def convert_pixel_data_to_image(self, pixel_data):
    """Converts DICOM pixel_data to a QPixmap using Pillow (PIL)."""
    try:
        # Assuming you've extracted the necessary image data from the DICOM file:
        image = Image.fromarray(pixel_data)  # Create a PIL Image object

        # Potential adjustments for windowing (if needed)
        if 'WindowCenter' in self.metadata and 'WindowWidth' in self.metadata:
            image = self.apply_windowing(image, self.metadata['WindowCenter'], self.metadata['WindowWidth'])

        # Convert PIL Image to QPixmap
        data = image.tobytes("raw", image.mode)  # Get raw image data
        qimage = QImage(data, image.size[0], image.size[1], QImage.Format_RGB888)  # For RGB example
        pixmap = QPixmap.fromImage(qimage)

        self.image_label.setPixmap(pixmap)
        return True

    except Exception as e:
        logging.error(f"Image conversion error: {str(e)}")
        return False

def apply_windowing(self, image, window_center, window_width):
    """Applies DICOM windowing to a Pillow Image."""

    # Calculate minimum and maximum intensity values based on windowing
    min_intensity = window_center - window_width // 2
    max_intensity = window_center + window_width // 2

    # Apply linear scaling with clipping
    def normalize(value):
        return min(max(value, min_intensity), max_intensity)

    image = image.point(normalize)

    # Convert to 8-bit grayscale (if not already)
    if image.mode != 'L': 
        image = image.convert('L')

    return image


# ... (Your load_dicom_metadata function, with error handling)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DICOMViewer()
    viewer.show()
    sys.exit(app.exec())
