import os
import shutil

def delete_featurettes(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            if name == "Special":
                full_path = os.path.join(root, name)
                shutil.rmtree(full_path)
                print(f"Deleted: {full_path}")

if __name__ == "__main__":
    starting_directory = "D:\Entertainment"
    delete_featurettes(starting_directory)
