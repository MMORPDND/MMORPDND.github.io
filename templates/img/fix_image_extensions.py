#!/bin/python3
import os

def rename_jpeg_to_jpg():
    """
    Rename all .jpeg files in the current folder to have a .jpg extension.
    """
    current_folder = os.getcwd()  # Get the current folder path
    files = os.listdir(current_folder)  # List all files in the current folder

    count = 0  # Track the number of files renamed

    for file in files:
        if file.endswith(".jpeg"):  # Check if the file has a .jpeg extension
            new_name = file.replace(".jpeg", ".jpg")  # Create the new name with .jpg extension
            os.rename(file, new_name)  # Rename the file
            count += 1  # Increment the count

            print(f"Renamed file: {file} -> {new_name}")

    print(f"Renamed {count} file(s).")

rename_jpeg_to_jpg()

