import pydicom
import os
import config
import shutil  # For file operations
from pydicom.uid import generate_uid  # To generate unique identifiers 

def load_dicom_image(file_path):
    """Loads a DICOM image file and returns basic metadata.

    Args:
        file_path: Path to the DICOM file.

    Returns:
        A tuple containing:
            - pydicom dataset object
            - Patient Name (str)
            - Study Date (str)
            - Modality (str)
            - SOP Instance UID (str) 
    """

    ds = pydicom.dcmread(file_path)
    patient_name = ds.get('PatientName', '')
    study_date = ds.get('StudyDate', '')
    modality = ds.get('Modality', '')
    sop_instance_uid = ds.get('SOPInstanceUID', '')

    return ds, patient_name, study_date, modality, sop_instance_uid

def extract_image_pixel_data(ds):
    """Extracts pixel data from a pydicom dataset.

    Args:
        ds: pydicom dataset object.

    Returns:
        Pixel data suitable for image display (often a NumPy array).
    """
    return ds.pixel_array

def store_dicom(ds, file_path):
    """Stores the modified DICOM dataset to a file.

    Args:
        ds: pydicom dataset object.
        file_path: Destination file path.
    """
    pydicom.dcmwrite(file_path, ds) 

def anonymize_dicom(ds):
    """Removes potentially identifying patient information.

    Args:
        ds: pydicom dataset object.

    Returns:
        Modified pydicom dataset object. 
    """
    # Replace with thorough anonymization:
    ds.PatientName = 'Anonymous' 
    ds.PatientID = '000000'  

    # Consider removing other sensitive tags based on your requirements

    return ds

# --- Optional network functions using pydicom's network capabilities ---

def send_dicom_cecho(destination_ae, destination_host, destination_port):
    """Send a DICOM C-ECHO request to test connectivity

    Args:
        destination_ae: The Application Entity title of the remote node
        destination_host: IP address of the remote node
        destination_port: Port of the remote node
    """
    # Basic implementation. Refer to pydicom docs for more advanced usage
    from pydicom.dataset import Dataset
    from pydicom.uid import ExplicitVRLittleEndian

    # Create a minimal Verification SOP Class dataset
    ds = Dataset()
    ds.SOPClassUID = '1.2.840.10008.1.1' 
    ds.SOPInstanceUID = generate_uid() 

    # Associate with our local AE title (you'll need to define this)
    assoc = pydicom.net.association.Association(ae_title=b'MY_LOCAL_AE') 

    # Send the request
    status = assoc.send_c_echo((destination_host, destination_port), destination_ae, 
                                context=assoc.presentation_contexts[0], 
                                dataset=ds, implicit_vr=ExplicitVRLittleEndian)   
    assoc.release()
    return status


if __name__ == '__main__':
    # ... (Add test code if you want to test functions directly)
