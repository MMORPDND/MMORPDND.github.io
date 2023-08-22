#!/bin/python3
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import os
import re
import shutil
import random
import json
import requests
from bs4 import BeautifulSoup

# Used for music
from pytube import YouTube
from moviepy.editor import *

# Used for progress bars
from tqdm import tqdm


def get_youtube_video_name(url):
    """
    Retrieves the title of a YouTube video based on the provided URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str or None: The title of the YouTube video if it can be retrieved successfully,
                     None if there was an error.

    Raises:
        None

    Example:
        >>> url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        >>> title = get_youtube_video_name(url)
        >>> print(title)
        "Rick Astley - Never Gonna Give You Up (Official Music Video)"
    """
    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(url)

        # Get the video title
        video_title = yt.title

        return video_title
    except Exception as e:
        print(f"Error: {e}")
        return None


def find_longest_and_shortest(words):
    """
    Find the lengths of the longest and shortest words in a given list.

    Args:
        words (list): A list of words.

    Returns:
        tuple: A tuple containing the lengths of the longest and shortest words.

    Raises:
        ValueError: If the input list is empty.

    Examples:
        >>> word_list = ["one", "two", "three", "four", "five"]
        >>> longest_length, shortest_length = find_longest_and_shortest(word_list)
        >>> print("Longest word length:", longest_length)
        >>> print("Shortest word length:", shortest_length)
        Longest word length: 5
        Shortest word length: 3
    """
    longest_word_length = len(max(words, key=len))
    shortest_word_length = len(min(words, key=len))
    return shortest_word_length, longest_word_length


def remove_numbers_at_start(string):
    """
    Remove numbers at the start of a string.

    Args:
        string (str): The input string.

    Returns:
        str: The string with numbers removed from the start.
    """
    index = 0
    while index < len(string) and string[index].isdigit():
        index += 1

    return string[index:].strip()


def append_to_file(file_path, string_to_append):
    """
    Append a string to a file.

    Parameters:
        file_path: The path to the file to append to.
        string_to_append: The string to append to the file.
    """
    with open(file_path, 'a') as file:
        file.write(string_to_append + '\n')


def read_lines_from_file(file_name):
    """
    Reads lines from a file and returns them as a list.

    Parameters:
        file_name (str): The name of the file to read.

    Returns:
        A list of strings, where each string represents a line from the file.
        Any leading and trailing whitespace is stripped from each line.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the specified file cannot be opened due to insufficient permissions.
    """
    lines = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            lines.append(line)
    return lines


def calculate_hp(class_type: str, level: int, constitution: int) -> int:
    """
    Calculate the hit points (hp) of a Dungeons & Dragons (DnD) 5th edition character
    based on their class, level, and constitution modifier.

    Args:
        class_type (str): The character's class (e.g. 'fighter', 'wizard', 'rogue').
        level (int): The character's level, between 1 and 20.
        constitution (int): The character's constitution score, between 1 and 30.

    Returns:
        int: The character's hit points, based on their class and level, modified by their
           constitution modifier.

    Raises:
        ValueError: If the given class_type is not recognized.
    """
    hit_die = 0

    # Determine hit die for the class
    if class_type == 'barbarian':
        hit_die = 12
    elif class_type == 'fighter' or class_type == 'paladin' or class_type == 'ranger':
        hit_die = 10
    elif class_type == 'cleric' or class_type == 'druid' or class_type == 'monk' or class_type == 'rogue' or class_type == 'warlock':
        hit_die = 8
    elif class_type == 'sorcerer' or class_type == 'wizard':
        hit_die = 6

    # Calculate base hit points
    base_hp = hit_die + (constitution - 10) // 2

    additional_hp = 0
    # Calculate additional hit points based on level
    for i in range(2, level):
        additional_hp += random.randint(1, hit_die) + ((constitution - 10) // 2)

    # Calculate total hit points
    total_hp = base_hp + additional_hp

    return total_hp


def calculate_proficiency_bonus(level):
    """
    Calculate the proficiency bonus based on character level.

    Parameters:
        level (int): The character's level.

    Returns:
        int: The character's proficiency bonus.
    """
    if level < 5:
        return 2
    elif level < 9:
        return 3
    elif level < 13:
        return 4
    elif level < 17:
        return 5
    else:
        return 6


def roll_4d6_drop_lowest():
    """
    Rolls 4d6 and returns the sum of the highest 3 dice.
    Returns:
        int: The sum of the highest 3 dice.
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    total = sum(sorted(rolls)[1:])
    print("Rolling 4d6: {0} - Dropping lowest -> {1}".format(rolls, total))
    return total


def get_stat_priority(character_class):
    """
    Returns a list of attributes ordered by the stat priority for a given class.
    Args:
        character_class (str): The class to get the stat priority for.
    Returns:
        list: The list of attributes ordered by the stat priority.
    """
    stat_priorities = {
        'barbarian': ['strength', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'charisma'],
        'bard': ['charisma', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'strength'],
        'cleric': ['wisdom', 'constitution', 'strength', 'intelligence', 'dexterity', 'charisma'],
        'druid': ['wisdom', 'constitution', 'dexterity', 'intelligence', 'charisma', 'strength'],
        'fighter': ['strength', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'charisma'],
        'monk': ['dexterity', 'wisdom', 'constitution', 'strength', 'intelligence', 'charisma'],
        'paladin': ['strength', 'constitution', 'charisma', 'wisdom', 'intelligence', 'dexterity'],
        'ranger': ['dexterity', 'wisdom', 'constitution', 'intelligence', 'strength', 'charisma'],
        'rogue': ['dexterity', 'intelligence', 'constitution', 'wisdom', 'strength', 'charisma'],
        'sorcerer': ['charisma', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'strength'],
        'warlock': ['charisma', 'constitution', 'dexterity', 'wisdom', 'intelligence', 'strength'],
        'wizard': ['intelligence', 'constitution', 'dexterity', 'wisdom', 'charisma', 'strength']
    }
    return stat_priorities.get(character_class.lower(), [])


def adjust_stats_for_level(assigned_stats, level):
    """
    Adjusts the stats for a character based on their level.

    Args:
        assigned_stats (dict): A dictionary representing the character's current stats, where keys are
            the stat names and values are the corresponding stat values.
        level (int): The level of the character.

    Returns:
        dict: A dictionary representing the adjusted stats based on the character's level.

    Raises:
        None.

    This method takes the current stats of a character, represented by the `assigned_stats` dictionary,
    and adjusts the stats based on the character's level. The adjusted stats are returned as a new dictionary.

    The adjustment of stats is determined by the character's level:
    - For levels below 4, no adjustments are made, and the original stats are returned.
    - For levels 4 to 7, 2 bonus attribute points are awarded.
    - For levels 8 to 11, 4 bonus attribute points are awarded.
    - For levels 12 to 15, 6 bonus attribute points are awarded.
    - For levels 16 to 18, 8 bonus attribute points are awarded.
    - For levels 19 and above, 10 bonus attribute points are awarded.

    The method prints the awarded bonus points and the original and updated attributes for informational purposes.

    Note: The stats dictionary is assumed to have numeric values for each stat.

    Example usage:
        assigned_stats = {'strength': 10, 'dexterity': 12, 'intelligence': 14}
        adjusted_stats = adjust_stats_for_level(assigned_stats, 8)
    """
    if level < 4:
        return assigned_stats
    elif level < 8:
        bonus_points = 2
    elif level < 12:
        bonus_points = 4
    elif level < 16:
        bonus_points = 6
    elif level < 19:
        bonus_points = 8
    else:
        bonus_points = 10

    print(f"level {level} awards {bonus_points} bonus attribute points")
    print(f"Original attributes: {assigned_stats}")

    # Sort the dictionary by descending values   
    sorted_dict = dict(sorted(assigned_stats.items(), key=lambda item: item[1], reverse=True))
    print(sorted_dict)

    # Calculate the maximum possible value for each key, without exceeding 22
    max_value = 22

    # Distribute bonus_points among the highest keys without exceeding 22
    for key in sorted_dict.keys():
        if sorted_dict[key] == 22 or bonus_points == 0:
            continue
        else:
            add_value = min(bonus_points, max_value - sorted_dict[key])
            sorted_dict[key] += add_value
            bonus_points -= add_value

    print(f"Updated attributes: {sorted_dict}")

    return sorted_dict


def generate_character_stats(character_class, level=1):
    """
    Generates a list of six stats for a character based on their class and level.
    Args:
        character_class (str): The character's class.
    Returns:
        list: The list of six stats.
    """
    # Get the stat priority for the character's class
    stat_priority = get_stat_priority(character_class)

    # Roll 4d6 and drop the lowest die for each of the six stats
    stats = [roll_4d6_drop_lowest() for _ in range(6)]

    # Assign the stats based on the stat priority for the character's class
    assigned_stats = {}
    for stat_name in stat_priority:
        stat_value = max(stats)
        stats.remove(stat_value)
        assigned_stats[stat_name] = stat_value

    # Adjust for character level.
    assigned_stats = adjust_stats_for_level(assigned_stats, level)

    return assigned_stats


def calculate_modifier(attribute_value):
    """
    Calculate the DnD attribute modifier based on the value of the attribute.

    Args:
        attribute_value (int): The value of the attribute.

    Returns:
        int: The modifier value for the attribute.

    Example:
        >>> calculate_modifier(15)
        2
    """
    modifier = (attribute_value - 10) // 2
    return modifier


def copy_file_to_directory(file_path, directory_path):
    """
    Copy a file to a directory.

    Args:
        file_path (str): The path to the file to copy.
        directory_path (str): The path to the directory to copy the file to.

    Raises:
        ValueError: If the file or directory doesn't exist.

    Returns:
        None
    """

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist")

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist. Creating directory...")
        os.makedirs(directory_path)

    new_file = directory_path + "/" + file_path.split('/')[-1].strip()
    if not os.path.isfile(new_file):
        # Copy the file to the directory
        print(f"Copying {file_path} to {directory_path}")
        shutil.copy(file_path, directory_path)
        print(f"File {file_path} copied to {directory_path}")
    else:
        print(f"file {new_file} already exists!")


def move_file_to_directory(file_path, directory_path):
    """
    Move a file to a directory.

    Args:
        file_path (str): The path to the file to move.
        directory_path (str): The path to the directory to move the file to.

    Raises:
        ValueError: If the file or directory doesn't exist.

    Returns:
        None
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise ValueError("File does not exist")

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist. Creating directory...")
        os.makedirs(directory_path)

    new_file = os.path.join(directory_path, os.path.basename(file_path))
    if not os.path.isfile(new_file):
        # Move the file to the directory
        print(f"Moving {file_path} to {directory_path}")
        shutil.move(file_path, directory_path)
        print(f"File {file_path} moved to {directory_path}")
    else:
        print(f"File {new_file} already exists!")


def print_prob_matrix(prob_matrix):
    """
    Prints a probability matrix to the console in JSON format.

    Parameters:
        prob_matrix (dict): A dictionary representing the probability matrix,
        where each key is an input character and the corresponding value is a dictionary
        of output characters and their probabilities.
    """
    # Convert the probability matrix to a JSON string with indentation and line breaks
    json_str = json.dumps(prob_matrix, indent=4, sort_keys=True)

    # Print the JSON string
    print(json_str)


def generate_prob_matrix(words):
    """
    Generates a probability matrix based on a list of words.

    Parameters:
        words (list of str): A list of words to use in generating the probability matrix.

    Returns:
        A dictionary representing the probability matrix, where each key is an input character
        and the corresponding value is a dictionary of output characters and their probabilities.

    Example:
        >>> words = ["cat", "dog", "cut", "cog", "cot", "caught"]
        >>> prob_matrix = generate_prob_matrix(words)
        >>> prob_matrix
    {
        'c': {'a': 0.4, 'u': 0.2, 'o': 0.4},
        'a': {'t': 0.5, 'u': 0.5},
        't': {},
        'd': {'o': 1.0},
        'o': {'g': 0.6666666666666666, 't': 0.3333333333333333},
        'g': {'h': 1.0},
        'u': {'t': 0.5, 'g': 0.5},
        'h': {'t': 1.0}
    }

    Note that the probabilities for each output character are normalized so that they sum to 1.0.
    """
    # Create an empty dictionary to store the probability matrix
    prob_matrix = {}

    # Iterate over the words in the list
    for word in words:
        # Iterate over the characters in the word
        for i in range(len(word)):
            input_char = word[i]

            # Get the dictionary of output characters and their counts for this input character
            output_counts = prob_matrix.get(input_char, {})

            # Increment the count for the next character in the word, if there is one
            if i < len(word) - 1:
                output_char = word[i + 1]
                output_counts[output_char] = output_counts.get(output_char, 0) + 1

            # Update the dictionary for this input character in the probability matrix
            prob_matrix[input_char] = output_counts

    # Convert the counts in the probability matrix to probabilities
    for input_char, output_counts in prob_matrix.items():
        total_count = sum(output_counts.values())
        output_probs = {output_char: count / total_count for output_char, count in output_counts.items()}
        prob_matrix[input_char] = output_probs

    return prob_matrix


def generate_word(prob_matrix, min_length=4, max_length=10):
    """
    Generate a random word using a probability matrix.

    Parameters:
        prob_matrix (dict): A dictionary representing the probability matrix for generating words.
        min_length (int): The minimum length of the generated word. Default value is 4.
        max_length (int): The maximum length of the generated word. Default value is 10.

    Returns:
        A string representing the generated word.

    Algorithm:
        1. Choose a random length between min_length and max_length.
        2. Initialize the word with a random input character.
        3. Generate the next characters based on the probabilities in the matrix.
            a. Get the output probabilities for the current input character.
            b. Create a list of possible next characters based on their probabilities.
            c. Choose a random next character from the list.
            d. Update the word and the input character for the next iteration.
        4. Return the generated word.
    """
    # Choose a random length between min_length and max_length
    length = random.randint(min_length, max_length)

    # Initialize the word with a random input character
    input_char = random.choice(list(prob_matrix.keys()))
    while prob_matrix.get(input_char) is None or not prob_matrix.get(input_char):
        # print(f"reloading {input_char}")
        input_char = random.choice(list(prob_matrix.keys()))

    # print(f"input_char: {input_char}")
    word = input_char

    # Generate the next (length - 1) characters based on the probabilities in the matrix
    for i in range(length - 1):
        output_probs = prob_matrix.get(input_char)

        # print(f"output_probs: {output_probs}")
        while output_probs is None or not output_probs:
            # print(f"reloading {output_probs}")
            os.system("sleep 1")
            output_probs = prob_matrix.get(input_char)

        # print(f"output_probs: {output_probs}")
        temp_list = []
        for possible_char in output_probs:
            # print("{0} -> {1}".format(possible_char, output_probs[possible_char]))
            for i in range(int(output_probs[possible_char] * 25)):  # 25 only pulls anything over 4%
                temp_list.append(possible_char)

        # print(f"temp_list: {temp_list}")
        next_char = random.choice(temp_list)
        output_probs = prob_matrix.get(next_char)

        if len(word) + 1 == length:
            return word + next_char
        else:
            while output_probs is None or not output_probs:
                # print(f"reloading {next_char}")
                next_char = random.choice(temp_list)
                output_probs = prob_matrix.get(next_char)

        # print(f"next char {next_char}")
        word += next_char
        input_char = next_char

    return word


def move_file(source_file_path, destination_folder_path):
    """
    Move a file from the source path to the destination folder.

    Args:
        source_file_path (str): The path to the file to be moved.
        destination_folder_path (str): The path to the destination folder.

    Returns:
        None
    """

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # Use shutil.move() to move the file to the destination folder
    shutil.move(source_file_path, destination_folder_path)


class Variables:
    """
    A class to store app wide variables.
    """

    def __init__(self):
        self.current_prob_matrix = None
        self.current_file = ""
        self.current_list = []
        self.output_file_folder = ""
        self.character_template_file = "characterTemplate.html"

        # Define directories to exclude
        self.directories_to_exclude = ["templates", "css", ".git", ".idea", ".github", "scripts", "docs"]

        # Define the root directory
        self.root_dir = os.getcwd()
        self.trash_dir = self.root_dir + "/trash"

    def trash_file(self, file):
        """
        Move a file to the trash folder.
        
        Parameters:
            file: The file to move.
            
        Returns: 
            None
        """
        if file.endswith(".char"):
            destination = self.trash_dir + "/chars"
        elif file.endswith(".py") or file.endswith(".sh"):
            destination = self.trash_dir + "/scripts"
        elif is_image_file(file):
            destination = self.trash_dir + "/img"
        else:
            destination = self.trash_dir

        move_file(file, destination)

    def reset(self):
        """
        Reset the state of some objects to their initial values.
        
        This method resets the state of the object by clearing the values of the current_file, current_list,
        and current_prob_matrix attributes. After calling this method, the object is restored to its initial
        state, ready for new data to be processed and stored.

        Example:
            my_object = MyClass()
            my_object.current_file = "data.txt"
            my_object.current_list = [1, 2, 3]
            my_object.current_prob_matrix = {"A": 0.2, "B": 0.3}
            my_object.reset()
            # After resetting, my_object's attributes are cleared and ready for new data.
        """
        self.current_file = ""
        self.current_list = []
        self.current_prob_matrix = {}


# Define a global variable containing the declared vars. Use this so they are all only defined once and can be
# updated/stored throughout the applications lifetime.
global_vars = Variables()


def get_character_fields(file):
    """
    Read a file containing character fields and their values, and return a dictionary of the fields.

    Args:
        file (str): The path to the file containing character fields.

    Returns:
        dict: A dictionary mapping character fields to their corresponding values.

    Raises:
        None.

    The method opens the specified file and reads its contents. Each line in the file is expected to
    represent a character field and its value, separated by an equals sign (=). The method parses each
    line, extracts the field name and value, converts them to lowercase, and stores them in a dictionary.
    The resulting dictionary is returned.

    If the 'class' field is not found in the character fields, an error message is printed, and an
    empty dictionary is returned.

    Example usage:
        character_fields = get_character_fields('character_data.txt')
    """
    char_fields = {}
    # Open the current file and read in the contents.
    with open(file, 'r') as f:
        contents = f.readlines()
    try:
        for line in contents:
            var = line.split('=')[0].strip().lower()
            if "name" in var or "information" in var or "notes" in var:
                val = line.split('=')[1].strip()
            else:
                val = line.split('=')[1].strip().lower()
            char_fields[var] = val
    except Exception:
        print(f"ERROR: Incorrect file format: {file}")

    # check to make sure class is defined.
    if "class" not in char_fields:
        print(f"ERROR: No 'class' value found in char_fields: {char_fields}")
        return

    return char_fields


def split_list(lst, n):
    """
    Split a list into n sublists of approximately equal size.

    Args:
        lst (list): The input list to be split.
        n (int): The number of sublists to create.

    Returns:
        list: A list containing n sublists.

    Example:
        >>> my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> sublists = split_list(my_list, 3)
        >>> print(sublists)
        [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]
    """
    length = len(lst)
    avg = length // n
    remainder = length % n

    result = []
    start = 0

    for i in range(n):
        end = start + avg + (1 if i < remainder else 0)
        result.append(lst[start:end])
        start = end

    return result


def create_html_list(values):
    """
    Create an HTML list from a string of semi-colon-separated values.

    Args:
        values (str): The string of semi-colon-separated values.

    Returns:
        str: The HTML list generated from the values.

    Example:
        >>> create_html_list("Item 1; Item 2; Item 3")
        '<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>\n</ul>'
    """
    items = values.split(";")  # Split the values by semi-colon

    # If we have between 20-40 elements, split into 2 columns.
    if 20 <= len(items) <= 40:
        html_list = "<div class=\"column-container\">\n"
        item_lists = split_list(items, 2)
        for item_list in item_lists:
            html_list += "<div class=\"column\"><ul>\n"  # Start the HTML list

            for item in item_list:
                item = item.strip()  # Remove leading/trailing whitespace
                html_list += f"<li>{item}</li>\n"  # Add each item as an HTML list item

            html_list += "</ul></div>"  # Close the HTML list
        html_list += "</div>\n"

    # If we have more than 40 elements, split into 3 columns.
    elif len(items) > 40:
        html_list = "<div class=\"column-container\">\n"
        item_lists = split_list(items, 4)
        for item_list in item_lists:
            html_list += "<div class=\"column\"><ul>\n"  # Start the HTML list

            for item in item_list:
                item = item.strip()  # Remove leading/trailing whitespace
                html_list += f"<li>{item}</li>\n"  # Add each item as an HTML list item

            html_list += "</ul></div>"  # Close the HTML list
        html_list += "</div>\n"

    # Normal list operations.
    else:
        html_list = "<ul>\n"  # Start the HTML list

        for item in items:
            item = item.strip()  # Remove leading/trailing whitespace
            html_list += f"<li>{item}</li>\n"  # Add each item as an HTML list item

        html_list += "</ul>"  # Close the HTML list

    return html_list


def separate_header_and_info(string):
    """
    Separates the header value and information from a string in the format "*header* Information here".

    Args:
        string (str): The input string in the specified format.

    Returns:
        tuple: A tuple containing the title value and the information.

    Example:
        >>> separate_title_and_info("*header* Information here")
        ('header', 'Information here')
    """
    start_index = string.find("*") + 1  # Find the index of the first "*"
    end_index = string.rfind("*")  # Find the index of the last "*"

    header = string[start_index:end_index].strip()  # Extract the title value
    info = string[end_index + 1:].strip()  # Extract the information

    return header, info


def create_html_info(values):
    """
    Create an HTML info block from a string of semi-colon-separated values.

    Args:
        values (str): The string of semi-colon-separated values.

    Returns:
        str: The HTML info block generated from the values.

    Example:
        >>> create_html_info("Item 1; - Item 2; - Item 3; Item 4")
        '<p class="first-paragraph">Item 1</p>\n<p><ul><li>Item 2</li>\n<li>Item 3</li>\n</ul></p>\n<p>Item 4</p>\n'
    """
    # Stores whether a section including a header was used last.
    header_section_last = False;
    items = values.split(";")  # Split the values by semi-colon
    html_info = ""  # Start the HTML list

    item_list = ""
    for item in items:
        print(f"item: {item}")
        item = item.strip()  # Remove leading/trailing whitespace
        if item.startswith('-'):
            print(f"List item detected in: {item}")
            item_list += item.replace("-", "") + ";"
            continue

        # If we reach here, we've finished the "-" items.
        if item_list != "":
            print(f"Creating list from: {item_list}")
            item_list = item_list[:-1]  # Remove the last semi-colon
            html_list = create_html_list(item_list)
            item_list = ""  # reset the list to be re-used if needed.
            if html_info == "" or header_section_last:
                html_info += f"<p class=\"first-paragraph\">{html_list}</p>\n"
                header_section_last = False
            else:
                html_info += f"<p>{html_list}</p>\n"

        if '*' not in item:
            if html_info == "" or header_section_last:
                html_info += f"<p class=\"first-paragraph\">{item}</p>\n"
                header_section_last = False
            else:
                html_info += f"<p>{item}</p>\n"

        # These are the criteria for a subsection (section with a small header)
        if item.startswith('*') and "*" in item[1:]:
            print(f"Header detected in: {item}")
            header, info = separate_header_and_info(item)
            if info.strip() == "":
                html_info += f"<h4>{header}</h4>"
            else:
                html_info += f"<h4>{header}</h4><p class=\"subsection\">{info}</p>"
                header_section_last = True
            continue

    # If we reach here, we've finished the ";" items. There still may be a list to populate though.
    if item_list != "":
        item_list = item_list[:-1]  # Remove the last semi-colon
        html_list = create_html_list(item_list)
        item_list = ""  # reset the list to be re-used if needed.
        if html_info == "" or header_section_last:
            html_info += f"<p class=\"first-paragraph\">{html_list}</p>\n"
        else:
            html_info += f"<p>{html_list}</p>\n"
    return html_info


def create_html_table(input_line):
    """
    Convert a single line input to an HTML table format.

    Args:
        input_line (str): Single line input containing semi-colon-separated values.

    Returns:
        str: HTML table structure representing the input values.

    Example:
        For a table of the form:

        -----------
        | a1 | a2 |
        |---------|
        | b1 | b2 |
        |---------|
        | c1 | c2 |
        -----------

        input: "2,a1,a2,b1,b2,c1,c2"
        output: '<table><tr><td>Value 1</td><td>Value 2</td></tr><tr><td>Value 3</td><td>Value 4</td></tr><tr><td>Value 5</td><td>Value 6</td></tr></table>'
    """
    # Split the single line by semi-colon
    values = input_line.split(';')

    # Extract the number of columns
    num_columns = int(values[0])

    # Prepare the HTML table structure
    html_table = '<table>'

    # Iterate over the values and construct the table rows
    num_rows = int((len(values) - 1) / num_columns)
    for i in range(0, num_rows):
        html_table += '<tr>'
        for j in range(num_columns):
            html_table += f'<td>{values[i * num_columns + j + 1].strip()}</td>'
        html_table += '</tr>'

    # Close the HTML table structure
    html_table += '</table>'

    return html_table


def download_image(url, file_path):
    """
    Download an image from a URL and save it to a file path.

    Args:
        url (str): The URL of the image to download.
        file_path (str): The file path to save the downloaded image.

    Returns:
        bool: True if the image was successfully downloaded and saved, False otherwise.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the image to the specified file path
            with open(file_path, 'wb') as file:
                file.write(response.content)

            print(f"Image downloaded and saved to: {file_path}")
            return True
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while downloading the image: {str(e)}")
        return False


def add_number_to_filename(filename, number):
    """
    Add a number to the filename before the extension.

    Args:
        filename (str): The original file name.
        number (int): The number to add.

    Returns:
        str: The updated file name with a number added before the extension.

    Example Usage:
        >>> new_filename = add_number_to_filename("document.txt")
        >>> print(new_filename, 3)
        document (3).txt
    """
    base_name, extension = os.path.splitext(filename)
    new_filename = f"{base_name} ({number}){extension}"

    return new_filename


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


def create_html_img(input_line):
    """
    Create an HTML block for an image section.

    Args:
        input_line (str): The input string of the form "image_file, image_source, caption".

    Returns:
        str: The HTML block representing the image section.

    Notes:
        - If the image file already exists, it will be used. Otherwise, the image will be downloaded from the provided image source URL.
        - The image file, image source URL, and caption are extracted from the input line.

    Example:
        input_line = "image.jpg; https://www.example.com/image.jpg; A beautiful sunset"
        html_block = create_html_img(input_line)
    """
    # Split the image data string by semi-colon
    input_line = input_line.split(';')

    # Extract the image file, image source, and caption
    image_file = input_line[0].strip()
    image_source = input_line[1].strip()
    image_caption = input_line[2].strip()

    image_files = []
    if " (1)" in image_file:
        img_file_enum = image_file
        count = 2
        while os.path.isfile(img_file_enum):
            image_files.append(img_file_enum)
            img_file_enum = img_file_enum.replace(f" ({count - 1})", f" ({count})")
            count += 1
    elif os.path.isfile(add_number_to_filename(image_file, 1)):
        if os.path.isfile(image_file):
            image_files.append(image_file)
        img_file_enum = add_number_to_filename(image_file, 1)
        count = 2
        while os.path.isfile(img_file_enum):
            image_files.append(img_file_enum)
            img_file_enum = img_file_enum.replace(f" ({count - 1})", f" ({count})")
            count += 1
    else:
        image_files.append(image_file)

    if not os.path.isfile(image_file):
        print(f"Image NOT found: {image_file}.")
        if "www." in image_source or "https:" in image_source:
            if not download_image(image_source, image_file):
                print(f"No image found: image section will be incomplete.")
    else:
        print(f"Image found: {image_file}.")

    # Generate the HTML block
    html_block = f'<div class="dnd-image-info">'
    html_block += f'<div class="dnd-image-list">'
    for file in image_files:
        html_block += f'<a href="{file}"><img src="{file}" alt="Image"></a>'
    html_block += f'</div>'
    html_block += f'<div class="dnd-image-source">'
    if "www." in image_source or "https:" in image_source:
        html_block += f'Source: <a href="{image_source}">{image_source}</a>'
    else:
        html_block += f'Source: {image_source}'
    html_block += f'</div>'
    html_block += f'<div class="dnd-image-caption">'
    html_block += f'Caption: {image_caption}'
    html_block += f'</div></div>'

    return html_block, image_files


def fix_image_extensions():
    """
    Updates all image extensions by running the fix_image_extensions.py script.

    Example usage:
        fix_image_extensions()
    """
    current_dir = os.getcwd()
    os.chdir("./img")
    if os.path.isfile("fix_image_extensions.py"):
        command = f"./fix_image_extensions.py"
    else:
        print("Error: 'fix_image_extensions.py' file not found.")
        return
    os.system(command)
    os.chdir(current_dir)


def update_all():
    """
    Updates all components of the MMORPDND system.

    This function updates the MMORPDND system by performing the following steps:
        1. Retrieves the current working directory.
        2. Changes the current working directory to the parent directory.
        3. Constructs a command to update the system by running './mmorpdnd.py -u'.
        4. Executes the update command using the system shell.
        5. Changes the current working directory back to the original directory.

    Note: This function assumes that the 'mmorpdnd.py' script is located in the parent directory.

    Example usage:
        update_all()
    """
    current_dir = os.getcwd()
    os.chdir("../")
    if os.path.isfile("mmorpdnd.py"):
        command = f"./mmorpdnd.py -u"
    else:
        print("Error: 'mmorpdnd.py' file not found.")
        return
    os.system(command)
    os.chdir(current_dir)


def get_random_line(file_path):
    """
    Return a random line from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: A random line from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            return random_line.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error reading file: {file_path}")


def extract_first_integer(string):
    """
    Extracts the first integer from a given string.

    Args:
        string (str): The input string.

    Returns:
        int or None: The first integer found in the string, or None if no integer is found.

    Example:
        >>> string = "'6 (barbarian 3, rogue 3)'"
        >>> first_integer = extract_first_integer(string)
        >>> print(first_integer)
        6
    """
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    else:
        return None


class Creator:
    def __init__(self):
        self.last_user_input = None
        self.gui = tk.Tk()
        self.gui.geometry("850x500")
        self.gui.title("File Browser")

        # Load icon image
        icon = PhotoImage(file='{}/../mmorpdnd.png'.format(global_vars.root_dir))
        # Set icon image
        self.gui.tk.call('wm', 'iconphoto', self.gui._w, icon)

        # Create the menu bar
        menubar = tk.Menu(self.gui)
        # Create a file menu and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.gui.quit)

        # Create a frame for the file path display and edit box
        path_frame = tk.Frame(self.gui)
        path_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create a label for the file path display
        path_label = tk.Label(path_frame, text="Input File:")
        path_label.pack(side=tk.LEFT, padx=(0, 5))

        # Create an editable text box for the file path display
        self.path_text = tk.Entry(path_frame, width=82)
        self.path_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Bind a function to the Entry widget that is called whenever the text is modified
        # self.path_text.bind('<KeyRelease>', self.path_text_updated)

        # Create a button to open the file browser
        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_files)
        browse_button.pack(side=tk.LEFT, padx=(5, 0))

        # Create a frame for the yes and no buttons
        top_button_frame = tk.Frame(self.gui)
        top_button_frame.pack(side=tk.TOP, pady=10)

        # Create a button to open the file browser
        generate_word_button = tk.Button(top_button_frame, text="Generate Word", command=self.generate_word)
        generate_word_button.pack(side=tk.LEFT, padx=10)

        # Create a button to open the file browser
        create_page_button = tk.Button(top_button_frame, text="Create Page", command=self.create_pages)
        create_page_button.pack(side=tk.LEFT, padx=10)

        # Create a button to open the file browser
        random_place_button = tk.Button(top_button_frame, text="Random Places", command=self.random_place)
        random_place_button.pack(side=tk.LEFT, padx=10)

        # Create a trash checkbox
        self.trash_checkbox_value = tk.BooleanVar(value=True)
        self.trash_checkbox_value.set(True)  # Set the variable to False
        trash_checkbox = tk.Checkbutton(top_button_frame, text="Trash", variable=self.trash_checkbox_value,
                                        command=self.checkbox_changed)
        trash_checkbox.pack(side=tk.LEFT, padx=1)

        # Create a trash checkbox
        self.download_checkbox_value = tk.BooleanVar(value=True)
        self.download_checkbox_value.set(True)  # Set the variable to False
        download_checkbox = tk.Checkbutton(top_button_frame, text="Download Files",
                                           variable=self.download_checkbox_value,
                                           command=self.checkbox_changed)
        download_checkbox.pack(side=tk.LEFT, padx=1)

        # Create a button to open the file browser
        update_button = tk.Button(top_button_frame, text="Update All", command=update_all)
        update_button.pack(side=tk.LEFT, padx=10)

        # Create a frame for the large text box and scrollbar
        text_frame = tk.Frame(self.gui)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=(10, 0), pady=10, expand=True)
        text_frame.pack_propagate(False)

        # Create a text widget for the large text box
        self.large_text = tk.Text(text_frame)
        self.large_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and attach it to the text widget
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        self.large_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.large_text.yview)

        # Create a frame for the yes and no buttons
        button_frame = tk.Frame(self.gui)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Create a button to store "yes"
        self.yes_button = tk.Button(button_frame, text="Yes", command=self.yes)
        self.yes_button.pack(side=tk.LEFT, padx=(10, 5))

        # Create a button to store "no"
        self.no_button = tk.Button(button_frame, text="No", command=self.no)
        self.no_button.pack(side=tk.LEFT, padx=(5, 10))

        # Create a button to store "reset"
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=(5, 10))

        self.no_button.config(state="disabled")
        self.yes_button.config(state="disabled")

    def create_html_music(self, urls):
        """
        Creates an HTML list with links to the provided URLs and a folder icon.

        Args:
            urls (str or list): The URL or list of URLs as a semicolon-delimited string or a list of strings.

        Returns:
            str: The HTML list portion with links and folder icons.

        Example:
            >>> urls = "https://www.youtube.com/watch?v=dQw4w9WgXcQ;https://www.youtube.com/watch?v=VIDEO2_ID"
            >>> html_list = self.create_html_music(urls)
            >>> print(html_list)
            <ul>
            <li><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Video 1</a><a href="local/path/video1.mp3"><i class="fas fa-folder"></i></a></li>
            <li><a href="https://www.youtube.com/watch?v=VIDEO2_ID">Video 2</a><a href="local/path/video2.mp3"><i class="fas fa-folder"></i></a></li>
            </ul>
        """
        if urls.strip() == "":
            return ""

        # Split the URLs into a list
        url_list = urls.split(";")

        # Create the HTML list
        html_list = '<ul>\n'
        for url in url_list:
            video_name = get_youtube_video_name(url)
            self.output_text(f"Downloading {video_name}. See terminal for progress report!")
            mp3_path = self.download_youtube_video_as_mp3(url)
            rel_mp3_path = os.path.relpath(mp3_path, global_vars.output_file_folder)
            html_list += f'<li><a href="{url}">{video_name}</a><a href="{rel_mp3_path}"><i class="fas fa-folder"></i></a></li>\n'
        html_list += '</ul>'

        return html_list

    def download_youtube_video_as_mp3(self, url, output_path="../music"):
        """
        Downloads a YouTube video as a high-quality MP3 file.

        Args:
            url (str): The URL of the YouTube video.
            output_path (str): The path to the directory where the MP3 file will be saved.

        Returns:
            str or None: The path of the downloaded MP3 file if the download and conversion
                         are successful, None if there was an error.

        Raises:
            None

        Example:
            >>> url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            >>> output_path = "/path/to/output/directory"
            >>> mp3_path = download_youtube_video_as_mp3(url, output_path)
            >>> print(mp3_path)
            "/path/to/output/directory/output.mp3"
        """
        try:
            if "youtube" not in url:
                print(f"Invalid Youtube url: {url}")
                return None

            output_name = get_youtube_video_name(url).replace("|", "").replace("/", "").replace(":", "").replace("-",
                                                                                                                 "").replace(
                " ", "_")
            mp3_path = f"{output_path}/{output_name}.mp3"
            if os.path.isfile(mp3_path):
                print(f"File already exists: {mp3_path}")
                return mp3_path

            if not self.download_checkbox_value.get():
                print(f"Downloading option not checked: {mp3_path}")
                return mp3_path

            # Create a YouTube object with the provided URL
            yt = YouTube(url)

            # Get the video stream with the highest resolution
            video_stream = yt.streams.get_highest_resolution()

            if video_stream is None:
                print("No suitable video stream found for the video.")
                return None

            # Download the video stream with progress bar
            video_path = f"{output_path}/temp_video.{video_stream.subtype}"
            response = requests.get(video_stream.url, stream=True)

            total_size = int(response.headers.get('Content-Length', 0))
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, ncols=80)

            with open(video_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    progress_bar.update(len(data))

            progress_bar.close()

            # Convert the downloaded video to MP3
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(mp3_path)

            # Delete the temporary video file
            video.close()
            os.remove(video_path)

            print(f"Video downloaded as MP3: {mp3_path}")
            return mp3_path
        except Exception as e:
            print(f"Error: {e}")

            # Try again
            mp3_path = self.download_youtube_video_as_mp3(url, output_path)
            return mp3_path

    def random_place(self, number=100):
        """
        Generates random place names along with their corresponding types.

        Args:
            number (int, optional): The number of random place names to generate. Defaults to 50.

        Returns:
            None
        """
        self.update_input_file()

        random_places_file = "./lists/random_place.names"
        random_places = []
        type_list = "./lists/location_types.list"
        if not os.path.isfile(type_list):
            self.output_text(f"List file not found or invalid: {type_list}")
            return

        self.output_text(f"Generating {number} random place names!")
        self.output_text(f"---------------------------------")
        if os.path.isfile(global_vars.current_file):
            for i in range(number):
                place = get_random_line(global_vars.current_file)
                place_type = get_random_line(type_list)
                place_combo = f"{place} {place_type}"
                self.output_text(place_combo)
                random_places.append(place_combo)

        # Store the random places in the random places file.
        with open(random_places_file, 'a') as f:
            for place in random_places:
                f.write(place + '\n')

    def create_pages(self):
        """
        Generate page files for a file or each file within a directory.

        This method checks if the current file (global_vars.current_file) is a directory.
        If it is a file, it calls the generate_char() or create_page() method based on the file extension.
        If it is a directory, it iterates through each file within the directory and calls the generate_char()
        or create_page() method for each individual file.

        Returns:
            None

        Raises:
            None
        """
        self.update_input_file()
        fix_image_extensions()

        if os.path.isfile(global_vars.current_file):
            if global_vars.current_file.endswith(".char"):
                self.generate_char(global_vars.current_file)
            elif global_vars.current_file.endswith(".input"):
                self.create_page(global_vars.current_file)
        elif os.path.isdir(global_vars.current_file):
            directory = global_vars.current_file
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    if file_path.endswith(".char"):
                        self.generate_char(file_path)
                    elif file_path.endswith(".input"):
                        self.create_page(file_path)

            self.output_text(f"Page generation completed for all files in the directory: {directory}.")
        else:
            # If the current file is not a file or directory, display an error message and return.
            self.output_text(f"Error: {global_vars.current_file} is not a file or directory.")
            return

    def create_page(self, file=global_vars.current_file):
        """
        Create an HTML page based on the input file.

        Reads the input file specified by global_vars.current_file and extracts the content to generate an HTML page.
        The input file should have a '.input' extension.
        The output HTML file is created in the specified destination folder or the current directory if not specified.

        Returns:
            None
        """
        if not file.endswith(".input"):
            self.output_text(f"Wrong input file type: {file}")
            self.output_text(f"File should end with '.input'")
            return

        # read input file
        with open(file, 'r') as f:
            lines = f.readlines()

        folder = "."

        for line in lines:
            if "folder" in line:
                folder = line.split('=')[1].strip()
                print(f"Destination folder set to {folder}")

        global_vars.output_file_folder = '.'  # used for testing mainly
        for dirpath, dirnames, filenames in os.walk("../"):

            # Check if we are looking at a file in our exclude list.
            if any(exclude in dirnames for exclude in global_vars.directories_to_exclude):
                continue
            # Check if we are looking at a file in our exclude list.
            if any(exclude in dirpath for exclude in global_vars.directories_to_exclude):
                continue

            if folder in dirnames:
                global_vars.output_file_folder = dirpath + "/" + folder
                break
            elif dirpath.endswith(folder):
                global_vars.output_file_folder = dirpath + "/"
                break

        print(f"Output file folder set to: {global_vars.output_file_folder}")

        output_fn = os.path.basename(file).split('.')[0]
        output_images = []
        output_file = global_vars.output_file_folder + "/" + output_fn + ".html"
        print(f"Output file: {output_file}")

        # create HTML file
        with open(output_file, 'w') as f:
            # write HTML boilerplate
            f.write('<!DOCTYPE html>\n<html>\n<head>\n<title></title>\n</head>\n<body>\n')

            file_name_val = output_file.split('/')[-1].split('.')[0].replace("_", " ")
            header = f"<div class=\"dnd-header\"><h1>{file_name_val}</h1></div><hr/>"
            f.write(header)

            # iterate over lines in input file
            for line in lines:
                print(line, end='')
                # Skip the line with folder in it or a comment line.
                if "folder" in line or line.startswith('#') or line.strip() == "":
                    continue

                # parse line
                variable_class, value = line.split('=', 1)
                variable, class_name = variable_class.split('[')
                class_name = class_name[0:-1].strip()

                if class_name == "dnd-list" and ";" in value:
                    # Create HTML list element.
                    html_list = create_html_list(value)
                    html_element = f'<div class="{class_name}"><h3>{variable}</h3><p>{html_list}</p></div>'

                elif class_name == "dnd-table" and ";" in value:
                    # Create HTML table element.
                    html_table = create_html_table(value)
                    html_element = f'<div class="{class_name}"><h3>{variable}</h3><p>{html_table}</p></div>'

                elif class_name == "dnd-image" and ";" in value:
                    # Create HTML image element.
                    html_img, image_files = create_html_img(value)
                    image_name = value.split(';')[0].strip()
                    output_images.append(image_name)
                    for img in image_files:
                        output_images.append(img)
                    print(f"Processing {image_name}.")
                    html_element = f'<div class="{class_name}"><h3>{variable}</h3><p>{html_img}</p></div>'

                elif class_name == "dnd-info":
                    html_info = create_html_info(value)
                    if ";" in value:
                        # Create HTML info element.
                        html_element = f'<div class="{class_name}"><h3>{variable}</h3>{html_info}</div>'
                    else:
                        html_element = f'<div class="{class_name}"><h3>{variable}</h3><p class=\"first-paragraph\">{value}</p></div>'

                elif class_name == "dnd-music":
                    html_music = self.create_html_music(value)
                    html_element = f'<div class="{class_name}"><h3>{variable}</h3><p>{html_music}</p></div>'

                else:
                    # Create generic HTML element.
                    html_element = f'<div class="{class_name}"><h3>{variable}</h3><p>{value}</p></div>'

                html_element += '<hr>'

                # write HTML element to file
                f.write(html_element)

            # close HTML file
            f.write('</body>\n</html>')

            print(f'HTML file created: {output_file}')

        # copy images to correct location.
        if len(output_images) > 0:
            for image in output_images:
                if os.path.isfile(image):
                    output_image_dir = global_vars.output_file_folder + "/img"

                    # trash image if needed.
                    if self.trash_checkbox_value.get():
                        move_file_to_directory(image, output_image_dir)
                        if os.path.isfile(image):
                            global_vars.trash_file(image)
                    else:
                        copy_file_to_directory(image, output_image_dir)

                else:
                    print(f'Image file does not exist: {image}')

                    output_image_file = global_vars.output_file_folder + "/img/" + image
                    if os.path.isfile(output_image_file):
                        print(f'Image file exists in target directory: {output_image_file}')

        # move the files to the trash if this option is selected.
        if self.trash_checkbox_value.get():
            global_vars.trash_file(file)

    def checkbox_changed(self):
        """
        This method is called when checkboxes are checked or unchecked.
        It retrieves the values of the checkboxes and prints a message indicating whether they are enabled or disabled.
        """
        trash_files = self.trash_checkbox_value.get()
        download_files = self.download_checkbox_value.get()

        if trash_files:
            print("trash_files Checkbox enabled")
        else:
            print("trash_files Checkbox disabled")

        if download_files:
            print("download_files Checkbox enabled")
        else:
            print("download_files Checkbox disabled")

    def generate_char(self, file=global_vars.current_file):
        """
        Generate a character file based on the provided input file.

        This method updates the input file, checks if it has the correct file type (.char),
        generates character statistics and fields if they are not defined, replaces the fields
        in the template file with the character information, and writes the new character file.

        The process involves the following steps:
        1. Verifies if the input file has the correct file type (.char). If not, it displays an error message and exits.
        2. Retrieves the character fields from the input file.
        3. Determines the character class and level.
        4. If any fields are missing, generates default values for certain attributes and displays them.
        5. Calculates the character's hit points (hp) if not already defined.
        6. Generates the character file path and filename based on the character's name.
        7. Reads the character template file.
        8. Processes and replaces the fields in the template with the character information.
           - Replaces general character fields.
           - Calculates and inserts modifier values for certain attributes.
           - Handles proficiencies and adds proficiency bonus to corresponding skills.
           - Populates information, notes, and image blocks.
           - Updates abilities and equipment lists.
        9. Writes the new character file at the specified filepath.
        10. If the option is selected, moves the input file to the trash.

        Returns:
            None
        """
        if not file.endswith(".char"):
            self.output_text(f"Wrong input file type: {file}")
            self.output_text(f"File should end with '.char'")
            return

        # Define the fields to replace in the template file
        char_fields = get_character_fields(file)

        global_vars.output_file_folder = '.'  # used for testing mainly

        if "folder" in char_fields:
            folder = char_fields['folder'].strip()
            last_folder = folder.split('/')[-1]
            print(last_folder)

            print(f"Destination folder detected as {folder}")

            for dirpath, dirnames, filenames in os.walk("../"):

                # Check if we are looking at a file in our exclude list.
                if any(exclude in dirnames for exclude in global_vars.directories_to_exclude):
                    continue
                # Check if we are looking at a file in our exclude list.
                if any(exclude in dirpath for exclude in global_vars.directories_to_exclude):
                    continue

                if folder in dirpath:
                    global_vars.output_file_folder = dirpath + "/"
                    break

            print(f"Output file folder set to: {global_vars.output_file_folder}")

        char_class = char_fields['class']

        # Default to level 1 if none defined.
        if "level" not in char_fields:
            char_level = 1
        else:
            char_level = extract_first_integer(char_fields['level'])

        # Create character stats to fill in if none are defined.
        char_stats = generate_character_stats(char_class, char_level)
        attributes = ["strength", "constitution", "wisdom", "charisma", "dexterity", "intelligence"]
        for attribute in attributes:
            if attribute not in char_fields:
                self.output_text(f"Generated value for {attribute} as {char_stats[attribute]}")
                char_fields[attribute] = str(char_stats[attribute])

        if "hp" not in char_fields:
            hp = calculate_hp(char_class, int(char_fields['level']), int(char_fields['constitution']))
            self.output_text(f"Calculated hp as {hp}.")

        # Generate the character file path
        char_name = char_fields['name']
        filename = f'{char_name.lower().replace(" ", "_")}.html'
        filepath = os.path.join(global_vars.output_file_folder, filename)

        # Read the template file and replace the fields with the character information
        with open(global_vars.character_template_file, 'r') as f:
            template = f.read()

        proficiencies = char_fields['proficiencies'].strip().split(', ')
        proficiency_bonus = calculate_proficiency_bonus(char_level)
        self.output_text("Proficiency bonus for level {0} is {1}".format(char_level, proficiency_bonus))

        # Replace the appropriate fields.
        for field, value in char_fields.items():
            temp_field = '[' + field + ']'
            if "senses" in field:
                if char_fields['senses'].strip() != "" and "None" not in char_fields['senses']:
                    value += ", Passive Perception: {0}".format(10 + calculate_modifier(int(char_fields['wisdom'])))
                else:
                    value = "Passive Perception = {0}".format(10 + calculate_modifier(int(char_fields['wisdom'])))
            template = template.replace(temp_field, value)
            if value.isdigit():
                temp_field_modifier = '[' + field + " modifier]"
                modifier_value = calculate_modifier(int(value))
                if "level" not in field:
                    self.output_text("Modifier for {0} is {1}".format(field, modifier_value))

                # Add the proficiency bonus to the modifier.
                if field in proficiencies:
                    modifier_value += proficiency_bonus

                # Update the proficiency bonus to have a +.
                if modifier_value >= 0:
                    modifier_value_str = "+" + str(modifier_value)
                else:
                    modifier_value_str = str(modifier_value)
                template = template.replace(temp_field_modifier, modifier_value_str)

        for prof in proficiencies:
            temp_field_proficient = '[' + prof + " proficiency]"
            template = template.replace(temp_field_proficient, "<i class=\"fas fa-check\"></i>")

        pattern = r'\[(.*?) modifier\]'
        matches = re.findall(pattern, template)
        for match in matches:
            mod_val = 0
            if "arcana" in match or "history" in match or "investigation" in match or "nature" in match or "religion" in match:
                mod_val = calculate_modifier(int(char_fields['intelligence']))
            elif "animal handling" in match or "insight" in match or "medicine" in match or "perception" in match or "survival" in match:
                mod_val = calculate_modifier(int(char_fields['wisdom']))
            elif "deception" in match or "intimidation" in match or "performance" in match or "persuasion" in match:
                mod_val = calculate_modifier(int(char_fields['charisma']))
            elif "athletics" in match:
                mod_val = calculate_modifier(int(char_fields['strength']))
            elif "acrobatics" in match or "sleight of hand" in match or "stealth" in match:
                mod_val = calculate_modifier(int(char_fields['dexterity']))

            # Add the proficiency bonus if appropriate
            if match in proficiencies:
                mod_val += proficiency_bonus
                self.output_text("Adding proficiency bonus {0} to skill {1}".format(proficiency_bonus, match))

            # Set the values as string formatted.
            if mod_val >= 0:
                skill_modifier = '+' + str(mod_val)
            else:
                skill_modifier = str(mod_val)

            # Update the template.
            template = template.replace(f'[{match} modifier]', skill_modifier)

        pattern_prof = r'\[(.*?) proficiency\]'
        matches = re.findall(pattern_prof, template)
        for match in matches:
            empty_prof_modifier = "-"
            template = template.replace(f'[{match} proficiency]', empty_prof_modifier)

        # Replace the information block.
        info = char_fields['information']
        template = template.replace("[background information]", info)

        # Replace the notes block.
        if "notes" in char_fields:
            notes = char_fields['notes']
            template = template.replace("[notes]", notes)

        # Replace the image block.
        img_src = "img/" + char_fields['image']
        img_dir = global_vars.output_file_folder + "/img"
        img_desc = img_src.split('/')[1].split('.')[0] + "-image"
        template = template.replace("[image-description]", img_desc)
        template = template.replace("[image-url]", img_src)

        try:
            copy_file_to_directory(img_src, img_dir)
            if self.trash_checkbox_value.get():
                global_vars.trash_file(img_src)
        except ValueError as e:
            print(f"An error occurred: {e}")

        # Update abilities
        abilities = char_fields['abilities'].split(';')
        abilities_output = ""
        for ability in abilities:
            abilities_output += "<li><strong>"
            if ":" in ability:
                abilities_output += ability.split(':')[0].strip()
                ability_desc = ability.split(':')[1].strip()
                abilities_output += ":</strong>"
                abilities_output += ability_desc
                abilities_output += "</li>"
            else:
                abilities_output += ability.strip()
                abilities_output += ":</strong> ["
                abilities_output += ability.strip()
                abilities_output += " description]</li>"
        template = template.replace("[abilities list]", abilities_output)

        # Update equipment
        equipment = char_fields['equipment'].split(';')
        equipment_output = ""
        for equip in equipment:
            equipment_output += "<li><strong>"
            if ":" in equip:
                abilities_output += equip.split(':')[0].strip()
                equipment_desc = equip.split(':')[1].strip()
                equipment_output += ":</strong>"
                equipment_output += equipment_desc
                equipment_output += "</li>"
            else:
                equipment_output += equip.strip()
                equipment_output += ":</strong> ["
                equipment_output += remove_numbers_at_start(equip.strip())
                equipment_output += " description]</li>"
        template = template.replace("[equipment list]", equipment_output)

        # Write the new character file
        with open(filepath, 'w') as f:
            f.write(template)

        print(f'Character file created: {filepath}')

        # move the files to the trash if this option is selected.
        if self.trash_checkbox_value.get():
            global_vars.trash_file(file)

    def output_text(self, text):
        """
        Output the given text to the GUI window and the large_text widget.

        This method displays the provided text in the GUI window and appends it to the large_text widget.
        It also ensures that the text is visible by scrolling to the bottom of the widget and updates
        the GUI window to reflect the changes.

        Args:
            text (str): The text to be displayed and appended to the large_text widget.

        Example:
            gui_instance = MyGUI()
            gui_instance.output_text("Processing completed successfully.")
            # The text "Processing completed successfully." is displayed in the GUI window.
        """
        print(text)
        # Append the given text to the large_text widget
        self.large_text.config(state="normal")
        self.large_text.insert(tk.END, text + '\n')
        self.large_text.config(state="disabled")

        # Scroll to the bottom of the widget
        self.large_text.see("end")

        # Update the GUI window
        self.large_text.update_idletasks()

    def test(self):
        """
        Method for testing.

        Returns:
            None
        """
        self.output_text("test text")

    def get_user_choice(self):
        """
        Displays a graphical user interface with yes/no buttons and returns the user's choice.

        Args:
            None.

        Returns:
            bool: The user's choice. True represents "yes" and False represents "no".

        Raises:
            None.

        This method displays a graphical user interface (GUI) with "yes" and "no" buttons and waits for the user to make a choice.
        The GUI is implemented using a main event loop.

        The method performs the following steps:
        1. Enables the "yes" and "no" buttons.
        2. Creates a BooleanVar to store the user's choice.
        3. Defines the callback functions that will be called when the buttons are clicked. These functions call the appropriate
           methods (e.g., `self.yes()`, `self.no()`, `self.reset()`) and set the user_choice variable accordingly.
        4. Configures the buttons to call the respective callback functions.
        5. Starts the main event loop using `self.gui.mainloop()`.
        6. Disables the "yes" and "no" buttons after the user has made a choice.
        7. Returns the user's choice as a boolean value.

        Note: The specific details of the GUI implementation, such as the actual buttons and their configuration, may depend on
        the underlying GUI framework used.

        Example usage:
            get_user_choice()
        """
        # Disable the buttons
        self.yes_button.config(state=tk.ACTIVE)
        self.no_button.config(state=tk.ACTIVE)

        # Create a BooleanVar to store the user's choice
        user_choice = tk.BooleanVar()

        # Define the functions that will be called when the buttons are clicked
        def yes_button_callback():
            self.yes()
            nonlocal user_choice
            user_choice.set(True)
            self.gui.quit()

        def no_button_callback():
            self.no()
            nonlocal user_choice
            user_choice.set(False)
            self.gui.quit()

        def reset_button_callback():
            self.reset()
            nonlocal user_choice
            user_choice.set(False)
            self.gui.quit()

        # Configure the buttons to call the appropriate functions
        self.yes_button.config(command=yes_button_callback)
        self.no_button.config(command=no_button_callback)
        self.reset_button.config(command=reset_button_callback)

        # Start the main event loop
        self.gui.mainloop()

        self.yes_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)

        # Return the user's choice
        return user_choice.get()

    def yes(self):
        """
        Set last_user_input to "yes".

        This method updates the last_user_input attribute to "yes" and displays a message indicating the change.

        Example:
            gui_instance = MyGUI()
            gui_instance.yes()
            # The last_user_input attribute is updated to "yes".
        """
        self.last_user_input = "yes"
        print(f"last_user_input set to {self.last_user_input}")

    def no(self):
        """
        Set last_user_input to "no".

        This method updates the last_user_input attribute to "no" and displays a message indicating the change.

        Example:
            gui_instance = MyGUI()
            gui_instance.no()
            # The last_user_input attribute is updated to "no".
        """
        self.last_user_input = "no"
        print(f"last_user_input set to {self.last_user_input}")

    def reset(self):
        """
        Reset last_user_input and provide status.

        This method resets the last_user_input attribute to "reset", displays a reset message using the output_text
        method, and confirms the change with a print statement.

        Example:
            gui_instance = MyGUI()
            gui_instance.reset()
            # The last_user_input attribute is reset to "reset", and the GUI provides a reset status.
        """
        self.output_text("Resetting...")
        self.last_user_input = "reset"
        print(f"last_user_input set to {self.last_user_input}")

    def browse_files(self):
        """
        Open a file dialog to select a file path.

        This method opens a file dialog to allow the user to select a file path. The selected file path is then
        displayed in the editable box on the GUI.

        Example:
            gui_instance = MyGUI()
            gui_instance.browse_files()
            # The user selects a file path using the file dialog, and the selected path is displayed in the GUI.
        """
        # Use the file dialog to get a file path
        file_path = filedialog.askopenfilename()

        # Update the text in the editable box with the selected file path
        self.path_text.delete(0, tk.END)
        self.path_text.insert(0, file_path)

    def update_input_file(self):
        """
        Update the current input file and associated data.

        This method updates the current input file based on the path entered in the GUI. If no file path
        is provided, an appropriate message is displayed using the output_text method. If the provided
        file path is different from the current file path, the global_vars object is reset, and the new
        file path is set as the current file. Additionally, if the file's extension matches certain
        predefined extensions (such as '.char', '.names', or '.list'), the lines from the file are read
        and stored in the current_list attribute.

        Example:
            gui_instance = MyGUI()
            gui_instance.path_text.set("data.txt")
            gui_instance.update_input_file()
            # The current input file is updated to 'data.txt', and associated data is adjusted.
        """
        print("Updating input file.")
        if self.path_text.get() is None:
            self.output_text("No file input!")
        else:
            file = self.path_text.get()
            if file == global_vars.current_file:
                return
            else:
                global_vars.reset()
                global_vars.current_file = file
                self.output_text(f"Updated current work file to: {file}")
                if file.endswith(".char") or file.endswith(".names") or file.endswith(".list"):
                    global_vars.current_list = read_lines_from_file(file)

    def generate_word(self):
        """
        Generates a word based on a probability matrix and offers the option to append it to a file.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.

        This method generates a word using a probability matrix and prompts the user whether to append the generated word
        to a file.

        The method performs the following steps:
        1. Prints a message indicating that a word is being generated.
        2. Updates the input file.
        3. Generates a probability matrix based on the current list.
        4. Prints the generated probability matrix.
        5. Enters a loop that continues until the last user input is "reset".
            a. Generates a word using the current probability matrix.
            b. Outputs the generated word.
            c. Asks the user if they want to append the word to the file.
            d. Retrieves the user's choice.
            e. If the user chooses "yes", the word is appended to the file.
            f. If the user chooses "no", a message is outputted indicating that the word was not appended to the file.
            g. If the user's choice is neither "yes" nor "no", the loop continues.

        Note: The specific details of how the probability matrix is generated and how the word is outputted may depend on
        the implementation of the methods used within this method.

        Example usage:
            generate_word()
        """
        print("Generating word.")
        self.update_input_file()
        global_vars.current_prob_matrix = generate_prob_matrix(global_vars.current_list)
        shortest, longest = find_longest_and_shortest(global_vars.current_list)
        print_prob_matrix(global_vars.current_prob_matrix)
        while self.last_user_input != "reset":
            word = "{0}".format(generate_word(global_vars.current_prob_matrix, shortest, longest))
            self.output_text(f"Generated word: {word}")
            self.output_text("Do you want to append this word to the file? (y/n)")
            # Get the user's choice
            self.get_user_choice()
            if self.last_user_input == "yes":
                append_to_file(global_vars.current_file, word)
                self.output_text("Word appended to file.")
            elif self.last_user_input == "no":
                self.output_text("Word NOT appended to file.")
                continue
            else:
                continue

    def run(self):
        self.gui.mainloop()


if __name__ == '__main__':
    app = Creator()
    app.run()
