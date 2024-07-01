import os
import re
import shutil


def clean_name(name):
    # Remove everything after the year
    name = re.sub(r"\(\d{4}\).*$", "", name)
    # Remove common tags and extras
    name = re.sub(
        r"\[.*?\]|\(.*?\)|\d+p|x265|HEVC|10bit|BluRay|Dual Audio|AAC|Prof|WEB-DL|DDP5\.1|Atmos|H\.264.*$",
        "",
        name,
    )
    # Replace dots and underscores with spaces
    name = name.replace(".", " ").replace("_", " ")
    # Remove extra spaces
    name = " ".join(name.split())
    return name.strip()


def extract_year(name):
    # Try to find a year in parentheses first
    match = re.search(r"\((\d{4})\)", name)
    if match:
        return match.group(1)
    # If not found, look for a year without parentheses
    match = re.search(r"\b(\d{4})\b", name)
    if match:
        return match.group(1)
    return None


def rename_and_organize_files(root_dir):
    if not os.path.exists(root_dir):
        print(f"The directory {root_dir} does not exist.")
        return

    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)

        if not os.path.isfile(file_path):
            continue

        # Clean the filename
        cleaned_name = clean_name(filename)

        # Extract year
        year = extract_year(filename)

        if year:
            movie_name = clean_name(cleaned_name.replace(year, "").strip())
            new_name = f"{movie_name} ({year})"

            new_file_path = os.path.join(
                root_dir, new_name + os.path.splitext(filename)[1]
            )
            new_folder_path = os.path.join(root_dir, new_name)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_name}")

            # Create the new folder if it doesn't exist
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(f"Created folder: {new_name}")

            # Move the file into the new folder
            shutil.move(
                new_file_path,
                os.path.join(new_folder_path, os.path.basename(new_file_path)),
            )
            print(f"Moved {new_name} into its folder")
        else:
            print(f"Skipped {filename} - couldn't extract year")


# Usage
root_directory = r"D:\Downloads"
rename_and_organize_files(root_directory)
