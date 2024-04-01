import os
import shutil

def delete_sample_files_and_dirs(start_path):
    """
    Deletes any files or directories named 'sample' or 'Sample' (regardless of file extension) 
    in the specified directory and all subdirectories.

    Parameters:
    - start_path (str): The path of the directory to start searching from.
    """
    for root, dirs, files in os.walk(start_path, topdown=False):
        for name in files:
            if name.lower() == 'sample':
                file_path = os.path.join(root, name)
                try:
                    print(f"Deleting file: {file_path}")
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

        for name in dirs:
            if name.lower() == 'sample':
                dir_path = os.path.join(root, name)
                try:
                    print(f"Deleting directory: {dir_path}")
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"Error deleting directory {dir_path}: {e}")

if __name__ == "__main__":
    print("Please enter the directory to start searching from:")
    directory_to_search = input().strip()  # Strip whitespace to clean the input
    if os.path.isdir(directory_to_search):
        delete_sample_files_and_dirs(directory_to_search)
    else:
        print(f"The directory '{directory_to_search}' does not exist. Please check the path and try again.")
