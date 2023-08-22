#!/bin/python3
import os
import re
import random
import tkinter as tk
from tkinter import PhotoImage
from cssbeautifier import beautify
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='MMORPDND Tools and apps.')
parser.add_argument('-t', '--test', action='store_true', help='Runs the test-all feature then exit.')
parser.add_argument('-u', '--update', action='store_true', help='Runs the update-all feature then exit.')

args = parser.parse_args()


class MMORPDND_VARS:
    """
    This is a class for storing variables used by MMORPDND* classes.
    """

    def __init__(self):
        """
        Initialization method.
        """
        # Define the directory structure
        self.directory_structure = {
            "campaign": {
                "locations": {
                    "planet": {
                        "continents": {},
                        "oceans": {},
                        "seas": {}
                    },
                    "regions": {},
                    "dungeons": {},
                    "cities": {},
                    "landmarks": {},
                    "towns": {},
                    "maps": {},
                    "planes": {}
                },
                "items": {
                    "consumables": {
                        "potions": {},
                        "food": {},
                        "drink": {},
                        "herbs": {}
                    },
                    "plants": {},
                    "magic": {},
                    "weapons": {},
                    "armor": {},
                    "trinkets": {},
                    "quest": {},
                    "treasure": {},
                    "devices": {},
                    "other": {}
                },
                "notes": {},
                "creatures": {
                    "animals": {},
                    "monsters": {},
                    "critters": {},
                    "insects": {}
                },
                "lore": {
                    "history": {},
                    "factions": {},
                    "guilds": {},
                    "races": {},
                    "classes": {},
                    "backgrounds": {},
                    "deities": {},
                    "myths": {},
                    "languages": {}
                },
                "puzzles": {},
                "quests": {},
                "encounters": {},
                "characters": {
                    "player": {},
                    "non-player": {
                        "human": {},
                        "elf": {},
                        "halfling": {},
                        "dwarf": {},
                        "tiefling": {},
                        "dragonborn": {},
                        "half-elf": {},
                        "genasi": {}
                    }
                },
                "spells": {
                    "level_0": {},
                    "level_1": {},
                    "level_2": {},
                    "level_3": {},
                    "level_4": {},
                    "level_5": {},
                    "level_6": {},
                    "level_7": {},
                    "level_8": {},
                    "level_9": {},
                },
                "timeline": {}
            }
        }

        # Define the number of HTML files to create in each subdirectory
        self.num_dummy_files_per_subdir = 3  # Stores all files created so far.
        self.all_index_files = []

        # Define the root directory
        self.root_dir = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.directories_to_exclude = ["templates", "css", ".git", ".idea", ".github", "scripts", "docs"]

        # Define the regular expression to match the header section
        self.header_regex = re.compile(r"<head>.*?</head>", re.DOTALL)

        # Define the regular expression to match the header section
        self.title_regex = re.compile(r"<title>.*?</title>", re.DOTALL)

        # Define the template file paths
        self.header_template_file = "templates/headerTemplate.html"
        self.nav_template_file = "templates/navTemplate.html"
        self.css_path = "css/mmorpdnd.css"


# Define a global variable containing the declared vars. Use this so they are all only defined once and can be
# updated/stored throughout the applications lifetime.
global_vars = MMORPDND_VARS()


def is_image_file(file_name):
    """
    Checks if a file name is an image file based on its extension.

    Args:
        file_name (str): The name of the file to check.

    Returns:
        bool: True if the file name has an image extension, False otherwise.

    Example:
        >>> is_image_file('myphoto.jpg')
        True
        >>> is_image_file('document.pdf')
        False
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for ext in image_extensions:
        if file_name.endswith(ext):
            return True
    return False


def get_relative_path(from_file, to_file):
    """
    Returns the relative path from one file to another.

    Args:
        from_file (str): The path of the source file.
        to_file (str): The path of the target file.

    Returns:
        str: The relative path from the source file to the target file.

    Raises:
        None.

    This method takes two file paths, `from_file` and `to_file`, and calculates the relative path from `from_file`
    to `to_file`. The relative path represents the path that, when followed from `from_file`, leads to `to_file`.

    Example:
        Assuming from_file = '/path/to/source/file.html' and to_file = '/path/to/target/image.jpg',
        the method will return '../../target/image.jpg' as the relative path.

    Note: The method uses the `os.path.relpath()` function to calculate the relative path.

    Example usage:
        get_relative_path('/path/to/source/file.html', '/path/to/target/image.jpg')
        print(relative_path)  # Output: '../../target/image.jpg'
    """
    return os.path.relpath(to_file, os.path.dirname(from_file))


def create_dummy_html_files(directory=global_vars.root_dir):
    """
    Creates dummy HTML files in all directories and subdirectories for testing purposes.

    Args:
        directory (str): The directory path to start creating dummy HTML files from. Defaults to global_vars.root_dir.

    Returns:
        None.

    Raises:
        None.

    This method recursively walks through the directory structure, creates an index.html file in each directory,
    and creates additional HTML files with random links in each subdirectory.

    The method performs the following steps:
    1. Creates an index.html file in the specified directory with a basic HTML structure.
    2. Recursively walks through the directory structure using `os.walk`.
    3. For each subdirectory, excluding any directories listed in `global_vars.directories_to_exclude`:
        - Creates an index.html file in the subdirectory with a basic HTML structure.
        - Generates a specified number of dummy HTML files in the subdirectory, each containing a random link to another dummy file.
        - Prints a message indicating the successful creation of each HTML file.
    4. Creates additional dummy HTML files in the script directory (specified by the `directory` argument), each containing a random link to another dummy file.
    5. Prints a message indicating the successful creation of all HTML files.

    Note: The content of the generated HTML files consists of a basic HTML structure with a header and body.
    Each dummy file includes a link to two randomly chosen dummy files, facilitating testing scenarios.

    Example usage:
        create_dummy_html_files()
    """
    all_dummy_files = []
    # Create an index.html file in the current directory
    with open(os.path.join(directory, "index.html"), "w") as f:
        f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")

    # Recursively walk through the directory structure and create HTML files in each subdirectory
    for root, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:

            # Check if we are looking at a file in our exclude list.
            if any(exclude in root for exclude in global_vars.directories_to_exclude):
                continue
            if any(exclude in dirname for exclude in global_vars.directories_to_exclude):
                continue

            # Create an index.html file in each subdirectory
            with open(os.path.join(root, dirname, "index.html"), "w") as f:
                f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")

            for i in range(global_vars.num_dummy_files_per_subdir):
                # Use the current directory name as part of the filename
                filename = f"{dirname}_{i}.html"
                all_dummy_files.append(filename.split('.html')[0])
                random_one = random.choice(all_dummy_files)
                random_two = random.choice(all_dummy_files)
                with open(os.path.join(root, dirname, filename), "w") as f:
                    f.write(
                        f"<html><head></head><body><h1>This is {filename} in {dirname} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")
                    print(f"HTML file {directory}/{filename} created successfully!")

    # Create additional HTML files in the script directory
    for i in range(global_vars.num_dummy_files_per_subdir):
        # Use the script directory name as part of the filename
        filename = f"{os.path.basename(directory)}_{i}.html"
        all_dummy_files.append(filename.split('.html')[0])
        random_one = random.choice(all_dummy_files)
        random_two = random.choice(all_dummy_files)
        with open(os.path.join(directory, filename), "w") as f:
            f.write(
                f"<html><head></head><body><h1>This is {filename} in {directory} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")
            print(f"HTML file {directory}/{filename} created successfully!")

    print("HTML files created successfully!")


def alphabetize_links(list_of_links):
    """
    Alphabetizes the items in a list of links.

    Args:
        list_of_links (str): A multiline string representing a list of links in the format
            "<li><a href="url">link_text</a></li>". Each link should be on a separate line.

    Returns:
        str: A multiline string representing the alphabetized list of links.

    Example:
        links = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                   <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                   <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
                   <li><a href="foobar.html">foobar</a></li>
                   <li><a href="aria_thistlewood.html">aria_thistlewood</a></li>
                   <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                   <li><a href="elara_nightshade.html">elara_nightshade</a></li>'''

        sorted_list = alphabetize_links(links)

        print(sorted_list)
    """
    link_pattern = r'<li><a href="([^"]+)"(?:\sclass="[^"]*")?>([^<]+)</a></li>'
    matches = re.findall(link_pattern, list_of_links)

    sorted_links = sorted(matches, key=lambda x: x[1])

    sorted_list = ""
    for link in sorted_links:
        if "img/" in link[1]:
            sorted_list += f'<li><a href="{link[0]}" class="image-index-link"><i class="fas fa-camera"></i> {link[1]}</a></li>\n'
        elif "/" in link[0]:
            sorted_list += f'<li><a href="{link[0]}" class="dir-index-link"><i class="fas fa-folder"></i> {link[1]}</a></li>\n'
        else:
            sorted_list += f'<li><a href="{link[0]}">{link[1]}</a></li>\n'

    return sorted_list


class MMORPDND:
    """
    A class for all the main MMORPDND features.
    """

    def __init__(self):
        """
        Initialization method.
        """

    # Define a function to create directories recursively
    def create_directories(self, path: str, structure: dict) -> None:
        """
        Recursively creates directories in the given path according to the structure specified in the dictionary.
        
        Args:
            path (str): The root path where directories will be created.
            structure (dict): A dictionary representing the structure of the directories to be created.
            
        Returns:
            None
        """
        for key in structure:
            subpath = os.path.join(path, key)
            if not os.path.exists(subpath):
                os.makedirs(subpath)
                print(f"Created directory: {subpath}")
            if structure[key]:
                self.create_directories(os.path.join(path, key), structure[key])

    def create_index_files(self, directory=global_vars.root_dir):
        """
        Creates index files for all subdirectories within the specified directory.

        Args:
            directory (str): The directory path to start creating index files from. Defaults to global_vars.root_dir.

        Returns:
            None.

        Raises:
            None.

        This method traverses through all subdirectories and files starting from the specified directory and creates an
        index file named "index.html" in each directory that doesn't already have one.

        The method performs the following steps:
        1. Loop through all directories and files using `os.walk` starting from the specified directory.
        2. Check if an index file named "index.html" already exists in the current directory. If so, skip that directory.
        3. Check if the current directory matches any of the excluded directories defined in `global_vars.directories_to_exclude`.
           If so, skip that directory.
        4. Create an index.html file in the current directory.
        5. Write the HTML content to the index.html file, including the directory name in the title and header.
        6. Print a message indicating the creation of the index file.

        Note: The index.html file created contains a basic HTML structure with the title and header set to "Index of [directory_name]".

        Example usage:
            create_index_files()
        """
        # Loop through all directories and files starting from the specified directory.
        for root, dirnames, filenames in os.walk(directory):
            # Create index file in current directory.
            index_file_path = os.path.join(root, "index.html")

            # Skip this directory if index.html already exists.
            if os.path.exists(index_file_path):
                continue
            # Check if we are looking at a file in our exclude list.
            if any(exclude in index_file_path for exclude in global_vars.directories_to_exclude):
                continue

            # Create the index.html file and write the HTML content to it
            directory_name = os.path.basename(root)
            with open(index_file_path, 'w') as f:
                f.write(f"<html>\n<head>\n<title>Index of {directory_name}/{directory_name}</title>\n</head>\n<body>\n")
                f.write(f"<h1>Index of {root}</h1>\n</body>\n</html>\n")
            print(f"Created index file at {index_file_path}")

    def move_dir_items_to_end(self, string):
        """
        Moves directory items (lines containing "/index.html") to the end of the input string.

        This method takes a multi-line string as input and separates lines that contain "/index.html"
        (directory items) from other lines (non-directory items). It then rearranges the lines by moving
        the directory items to the end while maintaining the order of non-directory items.

        Args:
            string (str): The input multi-line string to be processed.

        Returns:
            str: A modified string with directory items moved to the end.

        Example:
            input_string = "Line 1\n/index.html\nLine 2\nLine 3\n/index.html"
            result = move_dir_items_to_end(input_string)
            # result will be "Line 1\nLine 2\nLine 3\n/index.html\n/index.html"
        """
        lines = string.split('\n')
        dir_items = []
        non_dir_items = []

        for line in lines:
            if "/index.html" in line:
                dir_items.append(line)
            else:
                non_dir_items.append(line)

        new_lines = non_dir_items + dir_items
        new_string = '\n'.join(new_lines)

        return new_string

    def move_img_items_to_end(self, string):
        """
        Moves items containing "img/" to the end of the string while preserving their original order.

        Args:
            string (str): A string containing items in the format '<li><a href="url">link_text</a></li>'.

        Returns:
            str: A new string with items containing "img/" moved to the end while preserving their original order.

        Example:
            >>> string = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
            ...            <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
            ...            <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
            ...            <li><a href="foobar.html">img/foobar</a></li>
            ...            <li><a href="aria_thistlewood.html">img/aria_thistlewood</a></li>
            ...            <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
            ...            <li><a href="elara_nightshade.html">elara_nightshade</a></li>'''
            >>> new_string = move_img_items_to_end(string)
            >>> print(new_string)
            <li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
            <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
            <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
            <li><a href="aria_thistlewood.html">img/aria_thistlewood</a></li>
            <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
            <li><a href="elara_nightshade.html">elara_nightshade</a></li>
            <li><a href="foobar.html">img/foobar</a></li>
        """
        lines = string.split('\n')
        img_items = []
        non_img_items = []

        for line in lines:
            if "img/" in line:
                img_items.append(line)
            else:
                non_img_items.append(line)

        new_lines = non_img_items + img_items
        new_string = '\n'.join(new_lines)

        return new_string

    def update_index_files(self):
        """
        Updates all index files in the directory and subdirectories to include links to other files in the same directory.

        Returns:
            None.

        Raises:
            None.

        This method performs the following steps:
        1. Prints a message indicating that index files are being updated.
        2. Retrieves a list of all HTML index files in the current directory and subdirectories, excluding any directories listed in `global_vars.directories_to_exclude`.
        3. For each index file found:
            - Reads the file data.
            - Identifies the HTML files present in the same directory as the current index file.
            - If the index links div section does not exist in the file, it adds the div section just before the closing </body> tag.
            - Updates the index links by generating HTML code for each HTML file in the directory (excluding the index.html file) and appending it to the index links div.
            - Replaces the old index links section in the file with the updated index links div.
            - Writes the updated file data back to the file.
            - Prints a message indicating that the index file has been updated.
        4. Prints a message indicating that all index.html files have been updated.

        Note: The method relies on regular expressions for searching and updating the index links section in each index file.

        Example usage:
            update_index_files()
        """
        print("Updating index files...")

        # Get list of all HTML index files in directory and subdirectories
        for root, dirnames, filenames in os.walk("."):
            for file in filenames:

                # Check if we are looking at a file in our exclude list.
                if any(exclude in root for exclude in global_vars.directories_to_exclude):
                    continue

                if file.endswith("index.html"):
                    global_vars.all_index_files.append(os.path.join(root, file))

        # Loop through each index file found
        for file in global_vars.all_index_files:

            # check if the file still exists.
            if not os.path.isfile(file):
                print(f"File no longer exists: {file}")
                continue

            with open(file, 'r+') as f:
                file_data = f.read()

                # Find all HTML files in same directory as current file
                dir_path = os.path.dirname(file)
                files_in_dir = []

                # Add each html file to the list of html files in that directory.
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)
                    if file_name.endswith(".html") or is_image_file(file_name) or os.path.isdir(
                            file_path) or file_name.endswith(".mp3"):
                        files_in_dir.append(file_name)

                # Create index links div section if it does not exist
                index_links_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*>.*?</div>'
                index_links_match = re.search(index_links_pattern, file_data, re.DOTALL)
                if not index_links_match:
                    index_links_div = '<div class="indexLinks"><ul></ul></div>'
                    file_data = re.sub(r'</body>', index_links_div + '\n</body>', file_data)

                # Update index links
                index_links_div_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*><ul>'
                index_links_div_match = re.search(index_links_div_pattern, file_data, re.DOTALL)
                index_links_div = index_links_div_match.group(
                    0) if index_links_div_match else '<div class="indexLinks"><ul>'
                index_links = ''
                for file_n in files_in_dir:
                    if file_n != 'index.html':
                        link_text = file_n.replace('.html', '').replace('_', " ")
                        file_path = os.path.join(dir_path, file_n)
                        if os.path.isdir(file_path):
                            if file_n == "img":
                                for image in os.listdir(file_path):
                                    if is_image_file(image):
                                        img_link = "img/" + image
                                        link = f'<li><a href="{img_link}" class="image-index-link">{img_link}</a></li>'
                                        index_links += f'{link}\n'
                                continue
                            else:
                                dir_link = file_n + "/index.html"
                                link = f'<li><a href="{dir_link}" class="dir-index-link">{link_text}</a></li>'
                        else:
                            link = f'<li><a href="{file_n}">{link_text}</a></li>'
                        index_links += f'{link}\n'

                index_links = alphabetize_links(index_links)
                index_links = self.move_dir_items_to_end(index_links)
                index_links = self.move_img_items_to_end(index_links)

                # Replace index links in file
                updated_data = re.sub(index_links_pattern, index_links_div + '\n' + index_links + '</ul></div>',
                                      file_data, flags=re.DOTALL)

                # Write updated file data to file
                f.seek(0)
                f.write(updated_data)
                f.truncate()
                print(f"{file} updated")
        print("All index.html files updated.")

    def update_headers(self, directory=global_vars.root_dir):
        """
        Updates the headers of HTML files in the specified directory and its subdirectories to match a predefined template.

        Args:
            directory (str): The directory path to update the HTML files in. Defaults to global_vars.root_dir.

        Returns:
            None.

        Raises:
            None.

        This method performs the following steps:
        1. Loop through all HTML files in the specified directory and its subdirectories.
        2. For each HTML file found that does not contain "Template" in its filename:
            - Read the contents of the HTML file.
            - Check if the file is in the list of directories to exclude.
            - Read the contents of the header template file.
            - Replace the header section in the HTML file with the contents of the template.
            - Generate a title based on the filename and replace the title section in the HTML file.
            - Determine the relative path to the CSS file.
            - Calculate the number of subdirectories between the HTML file and the CSS file.
            - Create the correct link path for the CSS file.
            - Replace the placeholder in the HTML file with the link to the CSS file.
            - Overwrite the HTML file with the updated contents.
            - Print a progress update indicating the file that has been updated.
        3. Print a message indicating that the headers and CSS have been updated in all relevant HTML files.

        Note: The method relies on regular expressions for pattern matching and modification.

        Example usage:
            update_headers()
        """
        # Loop through all HTML files in the current directory and its subdirectories
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # check for html file and if "Template" is in filename.
                if filename.endswith(".html") and "Template" not in filename:
                    # Read the contents of the HTML file
                    file_path = os.path.join(root, filename)

                    # Check if we are looking at a file in our exclude list.
                    if any(exclude in file_path for exclude in global_vars.directories_to_exclude):
                        continue

                    with open(file_path, "r") as f:
                        contents = f.read()

                    # Read the contents of the template file
                    with open(global_vars.header_template_file, "r") as f:
                        template = f.read()

                    # Replace the header section with the contents of the template
                    contents = re.sub(global_vars.header_regex, template, contents)

                    title = "<title>" + filename.split('.')[0].replace('_', ' ') + "</title>"
                    print(title)

                    # Replace the title section with the file name
                    contents = re.sub(global_vars.title_regex, title, contents)

                    # Determine the relative path to the CSS file
                    css_relative_path = os.path.relpath(global_vars.css_path, start=root)

                    # Determine the number of subdirectories between the HTML file and the CSS file
                    num_subdirs = css_relative_path.count(os.sep) - 1

                    # Create the correct link path for the CSS file
                    link_path = "../" * num_subdirs + global_vars.css_path

                    # Replace the placeholder with the link to the CSS file
                    contents = contents.replace("%OPENAICSS%", f'<link href="{link_path}" rel="stylesheet"/>')

                    # Overwrite the HTML file with the updated contents 
                    with open(file_path, "w") as f:
                        f.write(contents)

                    print(f"Updated head and css in {file_path}")  # Print progress update

    def update_navigation(self, directory=global_vars.root_dir):
        """
        Updates the navigation block of HTML files in the specified directory and its subdirectories to match a predefined template.

        Args:
            directory (str): The directory path to update the HTML files in. Defaults to global_vars.root_dir.

        Returns:
            None.

        Raises:
            None.

        This method performs the following steps:
        1. Loop through all HTML files in the specified directory and its subdirectories.
        2. For each HTML file found that does not contain "Template" in its filename:
            - Read the contents of the HTML file.
            - Check if the file is in the list of directories to exclude.
            - Print a progress message indicating the file being processed.
            - Read the contents of the navigation template file.
            - Find the navigation block in the original HTML file using a regular expression.
            - If a navigation block is found:
                - Replace the navigation block in the HTML file with the contents of the template.
                - Write the modified HTML back to the file.
                - Print a message indicating that the navigation block has been replaced.
            - If no navigation block is found:
                - Print a message indicating that the navigation block was not found.
                - Insert the navigation contents at the start of the body tag in the HTML file.
                - Overwrite the file with the updated contents.
                - Print a message indicating that the navigation contents have been inserted.

        Note: The method relies on regular expressions for pattern matching and modification.

        Example usage:
            update_navigation()
        """
        # loop through all files in directory and subdirectories
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".html") and "Template" not in filename:
                    # open the file and read the contents
                    file_path = os.path.join(root, filename)

                    # Check if we are looking at a file in our exclude list.
                    if any(exclude in file_path for exclude in global_vars.directories_to_exclude):
                        continue

                    print(f"Processing file: {file_path}")

                    # Read the original contents of the file in.
                    with open(file_path, "r") as file:
                        contents = file.read()

                    # open the nav file and read the contents
                    with open(global_vars.nav_template_file, "r") as file:
                        nav_contents = file.read()

                    # Find the navigation block in the original HTML file
                    navRegex = re.compile(r'<div class="navigation">(.*?)</div>', re.DOTALL)
                    navMatch = navRegex.search(contents)

                    if navMatch:
                        print(" -- Found navigation block")
                        # Replace the navigation block with the contents of the template
                        contents = contents.replace(navMatch.group(0), nav_contents)

                        # Write the modified HTML back to the file
                        with open(file_path, 'w') as f:
                            f.write(contents)

                        print(" -- Replaced navigation block!")
                    else:
                        print(" -- Navigation block not found!")

                        # insert the nav contents at the start of the body tag
                        new_contents = contents.replace("<body>", f"<body>\n{nav_contents}")

                        # overwrite the file with the new contents
                        with open(file_path, "w") as file:
                            file.write(new_contents)

                        print(" -- Inserted nav contents at the start of the body tag")

    def beautify_files(self, directory=global_vars.root_dir):
        """
        Beautifies HTML and CSS files in the specified directory and its subdirectories.

        Args:
            directory (str): The directory path to beautify the files in. Defaults to global_vars.root_dir.

        Returns:
            None.

        Raises:
            None.

        This method performs the following steps:
        1. Modifies the directories_to_exclude list to include template and CSS files.
        2. Loops through all files and subdirectories in the specified directory.
        3. For each HTML or CSS file found (excluding those in the modified directories_to_exclude list):
            - Constructs the file path.
            - Checks if the file is an HTML or CSS file, and skips it if not.
            - Reads the contents of the file.
            - If the file is an HTML file:
                - Uses BeautifulSoup to parse the HTML and prettify it.
            - If the file is a CSS file:
                - Uses cssbeautifier to prettify the CSS code.
            - Writes the prettified code back to the file.
            - Prints a message indicating that the file has been prettified.

        Note: The method relies on BeautifulSoup for HTML parsing and prettifying, and cssbeautifier for CSS prettifying.

        Example usage:
            navigator = Navigator()
            navigator.beautify_files()
        """
        # Modify our exclude list to include template and css files.
        modified_directories_to_exclude = global_vars.directories_to_exclude[:]
        if "templates" in modified_directories_to_exclude:
            modified_directories_to_exclude.remove("templates")

        if "css" in modified_directories_to_exclude:
            modified_directories_to_exclude.remove("css")

        # Loop through all files and subdirectories in the directory
        for root, dirnames, filenames in os.walk(directory):
            # Loop through all HTML files in the current directory
            for file in filenames:
                file_path = os.path.join(root, file)

                # Check if we are looking at a file in our exclude list.
                if any(exclude in file_path for exclude in modified_directories_to_exclude):
                    continue

                if not file.endswith(".html") and not file.endswith(".css"):
                    continue

                # Read in the HTML file
                print(file_path)
                with open(file_path, "r") as f:
                    contents = f.read()

                # html files.
                if file.endswith(".html"):
                    # Use BeautifulSoup to parse the HTML and prettify it
                    soup = BeautifulSoup(contents, "html.parser")
                    prettified_content = soup.prettify()

                    # This section fixes a bug with the newline and spaces on the newline adding a space before the commas.
                    prettified_content = re.sub(r'[\s\n]+,', ',', prettified_content)
                    prettified_content = re.sub(r'[\s\n]+</a>,', '</a>,', prettified_content)

                # html files.
                elif file.endswith(".css"):
                    # Use cssbeautifier to prettify the CSS code
                    prettified_content = beautify(contents)

                # Write the prettified code back to the file
                with open(file_path, "w") as f:
                    f.write(prettified_content)

                print(f"File {file_path} has been prettified.")

    def find_all_html_files(self, directory=global_vars.root_dir):
        """
        Finds all HTML files (not index.html files) in a directory and its subdirectories.

        Args:
            directory: The directory to search. Defaults to the current directory.
        Return: 
            A list of dictionaries containing the name (without extension), name (with extension), and full path
                 of each HTML file found.
        """
        html_files = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)

                # Check if we are looking at a file in our exclude list.
                if any(exclude in file_path for exclude in global_vars.directories_to_exclude):
                    continue

                if filename.endswith('.html') and "index.html" not in filename:
                    name_no_ext = os.path.splitext(filename)[0]
                    html_files.append({
                        'name_no_ext': name_no_ext,
                        'name_with_ext': filename,
                        'full_path': file_path
                    })
        return html_files

    def update_html_links(self, directory=global_vars.root_dir):
        """
        Update the links in the various HTML files to link to the appropriate file.

        Args:
            directory (str): The directory to search for HTML files. Defaults to global_vars.root_dir.

        Returns:
            None
        """
        html_files = self.find_all_html_files(directory)
        # Search the body text of each HTML file for the search strings
        for file_info in html_files:
            print("Parsing {0} for link updates!".format(file_info['full_path']))
            file_path = file_info['full_path']

            # Read in the contents of the file.
            with open(file_path, 'r') as f:
                content = f.read()

            # Use regular expressions to find the body text of the HTML file
            body_match = re.search("<body.*?>(.*?)</body>", content, flags=re.DOTALL)
            if body_match:
                body_text = body_match.group(1)
                # Search the body text for the search string
                for search_word in html_files:
                    search_string = search_word['name_no_ext']

                    # No need to link it it's to the current file.
                    if search_string == file_info['name_no_ext']:
                        continue

                    # Define the patterns to search for.
                    patterns = []
                    # Append a regular expression pattern to the `patterns` list
                    # The pattern matches the exact word `search_string` as a standalone word, avoiding matches within HTML tags or attributes
                    # The `(?ix)` flags enable case-insensitive and verbose mode for the regular expression
                    # The `(?<![-/">])` negative lookbehind ensures that the word is not preceded by certain characters (-, /, ", or >)
                    # The `(?<!>)` negative lookbehind ensures that the word is not preceded by the > character (to exclude matches within HTML tags)
                    # The `\b` word boundary markers ensure that the word is not part of a larger word
                    # The `re.escape(search_string)` escapes any special characters in the search_string to treat it literally
                    # The `(?<![-/.])` negative lookbehind ensures that the word is not preceded by certain characters (-, /, or .) to exclude matches within URLs or file paths
                    # The `(?![^<]*<\/a>)` negative lookahead ensures that the word is not followed by </a> to exclude matches within HTML anchor tags
                    patterns.append(
                        r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(re.escape(search_string)))
                    patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                        re.escape(search_string.replace('_', ' '))))
                    # Search for the plural strings too.
                    if not search_string.endswith('s'):
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string.replace('_', ' ') + 's')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string.replace('_', ' ') + '\'s')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string + 's')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string + '\'s')))
                    else:
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string.replace('_', ' ') + '\'')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string.replace('_', ' ') + 'es')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string + '\'')))
                        patterns.append(r'(?ix)(?<![-/">])(?<!>)\b{}\b(?<![-/.])(?![^<]*<\/a>)'.format(
                            re.escape(search_string + 'es')))

                    # Search through all possible patterns.
                    for pattern in patterns:
                        search_string_match = re.search(pattern, body_text, flags=re.DOTALL | re.VERBOSE)
                        if search_string_match:
                            print(" -- {0} found in {1}".format(search_string, file_path))
                            link_path = get_relative_path(file_path, search_word['full_path'])

                            # Replace the search string with the new string
                            new_string = "<a href=\"{0}\">{1}</a>".format(link_path, search_string.replace('_', ' '))
                            new_body_text = re.sub(pattern, new_string, body_text)
                            body_text = new_body_text
                            body_tags = re.search("<body(.*?)>", content, flags=re.DOTALL)
                            content = re.sub(r"<body[^>]*>(.*?)</body>", "<body>" + new_body_text + "</body>", content,
                                             flags=re.DOTALL)
                            content = re.sub(r"<body>", "<body" + body_tags.group(1) + ">", content, flags=re.DOTALL)
                            print(" -- Replacing {0} with {1}".format(search_string, new_string))

                            # Write the modified HTML file
                            with open(file_path, "w") as f:
                                f.write(content)


class MMORPDND_GUI:
    """
    Class to store GUI functions and operations.
    """

    def __init__(self):
        """
        Initialization method.
        Creates and configures the GUI window, sets up menu bar, and defines button styles.
        """
        self.mmorpdnd = MMORPDND()
        self.gui = tk.Tk()
        self.gui.title("MMORPDND")
        self.gui.geometry("300x470")

        # set the background color to black
        self.gui.configure(bg="black")

        # Load icon image
        icon = PhotoImage(file='{}/mmorpdnd.png'.format(global_vars.root_dir))
        # Set icon image
        self.gui.tk.call('wm', 'iconphoto', self.gui._w, icon)

        # Create the menu bar
        menubar = tk.Menu(self.gui)
        # Create a file menu and add it to the menu bar   
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.gui.quit)

        blue_button_style = {"font": ("Arial", 14), "bg": "#4287f5", "fg": "#ffffff", "activebackground": "#ffffff",
                             "activeforeground": "#4287f5"}

        red_button_style = {"font": ("Arial", 14), "bg": "#f54251", "fg": "#ffffff", "activebackground": "#ffffff",
                            "activeforeground": "#f54251"}

        test_all_button = tk.Button(self.gui, text="Test All", command=self.test_all, **red_button_style)
        test_all_button.pack(pady=5)

        update_all_button = tk.Button(self.gui, text="Update All", command=self.update_all, **red_button_style)
        update_all_button.pack(pady=5)

        create_directories_button = tk.Button(self.gui, text="Create Directories", command=self.create_directories,
                                              **blue_button_style)
        create_directories_button.pack(pady=5)

        create_dummy_html_files_button = tk.Button(self.gui, text="Create Dummy HTML Files",
                                                   command=self.create_dummy_html_files, **blue_button_style)
        create_dummy_html_files_button.pack(pady=5)

        create_index_files_button = tk.Button(self.gui, text="Create Index Files", command=self.create_index_files,
                                              **blue_button_style)
        create_index_files_button.pack(pady=5)

        update_index_links_button = tk.Button(self.gui, text="Update Index File Links", command=self.update_index_links,
                                              **blue_button_style)
        update_index_links_button.pack(pady=5)

        update_headers_button = tk.Button(self.gui, text="Update HTML Headers", command=self.update_headers,
                                          **blue_button_style)
        update_headers_button.pack(pady=5)

        update_navigation_button = tk.Button(self.gui, text="Update Navigation Blocks", command=self.update_navigation,
                                             **blue_button_style)
        update_navigation_button.pack(pady=5)

        update_html_links_button = tk.Button(self.gui, text="Update Links", command=self.update_html_links,
                                             **blue_button_style)
        update_html_links_button.pack(pady=5)

        beautify_files_button = tk.Button(self.gui, text="Beautify Files", command=self.beautify_files,
                                          **blue_button_style)
        beautify_files_button.pack(pady=5)

    def run(self):
        """
        This method will run/open the GUI.
        """
        self.gui.mainloop()

    def test_all(self):
        """
        This method will update all files.
        """
        self.create_directories()
        self.create_dummy_html_files()
        self.create_index_files()
        self.update_index_links()
        self.update_headers()
        self.update_navigation()
        self.update_html_links()
        self.beautify_files()

    def update_all(self):
        """
        This method will update all files.
        
        Note: The order of these matter!
        """
        self.create_directories()
        self.create_index_files()
        self.update_index_links()
        self.update_headers()
        self.update_navigation()
        self.update_html_links()
        self.beautify_files()

    def create_directories(self):
        self.mmorpdnd.create_directories(global_vars.root_dir, global_vars.directory_structure)

    def create_dummy_html_files(self):
        create_dummy_html_files(global_vars.root_dir)

    def create_index_files(self):
        self.mmorpdnd.create_index_files(global_vars.root_dir)

    def update_index_links(self):
        self.mmorpdnd.update_index_files()

    def update_headers(self):
        self.mmorpdnd.update_headers(global_vars.root_dir)

    def update_navigation(self):
        self.mmorpdnd.update_navigation(global_vars.root_dir)

    def beautify_files(self):
        self.mmorpdnd.beautify_files(global_vars.root_dir)

    def update_html_links(self):
        self.mmorpdnd.update_html_links(global_vars.root_dir)


def main():
    # main method code here
    gui = MMORPDND_GUI()

    if args.test:
        gui.test_all()
        exit(1)
    elif args.update:
        gui.update_all()
        exit(1)
    else:
        parser.print_help()

    gui.run()


if __name__ == '__main__':
    main()
