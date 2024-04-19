import os
import shutil

def delete_specific_folders(start_path, folder_names):
    """
    Recursively deletes folders with specific names from a start_path, with user confirmation and logging.

    :param start_path: The directory path to start the recursive search.
    :param folder_names: A set of folder names to search for and delete.
    """
    deleted_folders = []
    try:
        for root, dirs, files in os.walk(start_path, topdown=False):
            for name in dirs:
                if name in folder_names:
                    full_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(full_path, ignore_errors=False)
                        deleted_folders.append(full_path)
                        print(f"Deleted folder: {full_path}")
                    except Exception as e:
                        print(f"Error deleting folder {full_path}: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return deleted_folders

def main():
    # Prompt for the starting directory
    start_directory = input("Enter the path to the starting directory: ").strip()

    # Confirm the action
    confirm = input(f"Are you sure you want to delete specific folders from '{start_directory}'? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

    # Define the specific folder names to delete
    folders_to_delete = {
        "Specials", "Featurettes", "Webisodes", "Behind The Scenes",
        "Deleted Scenes", "Interviews", "Scenes", "Shorts",
        "Trailers", "Other"
    }

    # Call the function to start the deletion process
    deleted_folders = delete_specific_folders(start_directory, folders_to_delete)

    # Print summary
    if deleted_folders:
        print(f"Deletion process completed. Total folders deleted: {len(deleted_folders)}.")
    else:
        print("No matching folders were found or deleted.")

if __name__ == "__main__":
    main()
