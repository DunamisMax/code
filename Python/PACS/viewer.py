import sys
import pydicom
import config
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PIL import Image


class DICOMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple DICOM Viewer")
        self.metadata = None  # Store metadata for potential use 

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
                self.metadata = load_dicom_metadata(file_path) 
                self.display_image(self.metadata['PixelData'])  # Assuming 'PixelData' is the correct tag
                self.display_metadata(self.metadata)

            except (pydicom.errors.InvalidDicomError, KeyError, ValueError) as e:
                self.show_error(f"Error loading DICOM file: {str(e)}")

    def display_image(self, pixel_data):
        if not self.convert_pixel_data_to_image(pixel_data):
            self.show_error("Error converting image data.")

    def convert_pixel_data_to_image(self, pixel_data):
        try:
            image = Image.fromarray(pixel_data)

            if self.metadata and 'WindowCenter' in self.metadata and 'WindowWidth' in self.metadata:
                image = self.apply_windowing(image, self.metadata['WindowCenter'], self.metadata['WindowWidth'])

            data = image.tobytes("raw", image.mode) 
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

    def display_metadata(self, metadata):
    metadata_text = ""
    # Example - You can customize what metadata is displayed:
    for tag, value in metadata.items():
        if tag in ["PatientName", "PatientID", "Modality", "StudyDate"]: 
            metadata_text += f"{tag}: {value}\n" 

    self.metadata_display.setText(metadata_text)
    
    def show_error(self, message):
    QMessageBox.warning(self, "Error", message)
    
    def load_dicom_metadata(file_path):
    try:
        ds = pydicom.dcmread(file_path) 
        return ds  # Return the pydicom dataset object
    except pydicom.errors.InvalidDicomError:
        raise  # Re-raise the original exception for handling

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DICOMViewer()
    viewer.show()
    sys.exit(app.exec())