import os

# Specify the path
path = "D:\Entertainment\Hi-Res Movies"

# Get the list of directories in the specified path
directories = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]

# Print the folder names
print("Folder names in the specified path:")
for folder_name in directories:
    print(folder_name)