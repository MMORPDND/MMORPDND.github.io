#!/bin/python3
import os

def delete_index_html_files(directory):
    """
    Deletes all 'index.html' files in a directory and its subdirectories.

    Args:
        directory (str): The path to the directory.

    Returns:
        None
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "index.html":
                file_path = os.path.join(root, file)
                os.remove(file_path)

    print("Index.html files deleted successfully!")

# Example usage:
directory_path = "."
delete_index_html_files(directory_path)

