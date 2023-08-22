import os
import re
import shutil
import argparse
import random
import json


def print_prob_matrix(prob_matrix):
    # Convert the probability matrix to a JSON string with indentation and line breaks
    json_str = json.dumps(prob_matrix, indent=4, sort_keys=True)

    # Print the JSON string
    print(json_str)


def append_to_file(file_path, string_to_append):
    """
    Append a string to a file.
    
    :param file_path: The path to the file to append to.
    :param string_to_append: The string to append to the file.
    """
    with open(file_path, 'a') as file:
        file.write(string_to_append + '\n')


def read_names_from_file(filename):
    names = []
    with open(filename, 'r') as f:
        for line in f:
            name = line.strip()
            names.append(name)
    return names


def generate_prob_matrix(words):
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


# Testing

# names_file = "lists/dwarven.names"
# names_file = "lists/town.names"
names_file = "lists/elven.names"

names = read_names_from_file(names_file)

prob_matrix_names = generate_prob_matrix(names)
print_prob_matrix(prob_matrix_names)

# first_names = []
# last_names = []
# for name in names:
#    first_name = name.split(' ')[0].lower()
#    last_name = name.split(' ')[1].lower()
#    first_names.append(first_name)
#    last_names.append(last_name)     
# prob_matrix_first_name = generate_prob_matrix(first_names)
# prob_matrix_last_names = generate_prob_matrix(last_names)
# print_prob_matrix(prob_matrix_first_name)
# print_prob_matrix(prob_matrix_last_names)

for i in range(1000):
    # word = "{0} {1}".format(generate_word(prob_matrix_first_name), generate_word(prob_matrix_last_names))
    word = "{0}".format(generate_word(prob_matrix_names))
    print(word)
    user_input = input("Do you want to append this word to the file? (y/n)")
    if user_input.lower() == 'y':
        append_to_file(names_file, word)
    else:
        print("Word not appended to file.")
        continue

exit(1)

# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add an argument to the parser for the file name
parser.add_argument('-c', "--char_file", help="Name of the character input file.")
parser.add_argument('-p', "--pc",
                    help="This character is a player-character. Characters are considered npc by default.")

# parse the arguments
args = parser.parse_args()


def copy_file_to_directory(file_path, directory_path):
    """Copy a file to a directory.

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

    # Copy the file to the directory
    print(f"Copying {file_path} to {directory_path}")
    shutil.copy(file_path, directory_path)
    print(f"File {file_path} copied to {directory_path}")


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

    return assigned_stats


# Define the template file path and character directory
TEMPLATE_FILE = 'characterTemplate.html'

# Set's the character file parameter.
if args.char_file is not None:
    CHARACTER_FILE = args.char_file
else:
    CHARACTER_FILE = 'chars/template.char'

# Define the fields to replace in the template file
FIELDS = {}

with open(CHARACTER_FILE, 'r') as f:
    contents = f.readlines()

for line in contents:
    var = line.split('=')[0].strip()
    val = line.split('=')[1].strip()
    FIELDS[var] = val

CHAR_DIR = ""
for dirpath, dirnames, filenames in os.walk("../"):
    if 'characters' in dirnames:
        if args.pc:
            CHAR_DIR = os.path.join(dirpath, 'characters/player')
        else:
            CHAR_DIR = os.path.join(dirpath, 'characters/non-player')

# Generate the character file path
char_name = FIELDS['name']
filename = f'{char_name.lower().replace(" ", "_")}.html'
filepath = os.path.join(CHAR_DIR, filename)

# Read the template file and replace the fields with the character information
with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

proficiencies = FIELDS['proficiencies'].strip().split(', ')
level = int(FIELDS['level'])
proficiency_bonus = calculate_proficiency_bonus(level)
print("Proficiency bonus for level {0} is {1}".format(level, proficiency_bonus))

# Replace the appropriate fields.
for field, value in FIELDS.items():
    temp_field = '[' + field + ']'
    if "senses" in field:
        if FIELDS['senses'].strip() != "" and "None" not in FIELDS['senses']:
            value += ", Passive Perception: {0}".format(10 + calculate_modifier(int(FIELDS['wisdom'])))
        else:
            value = "Passive Perception = {0}".format(10 + calculate_modifier(int(FIELDS['wisdom'])))
    template = template.replace(temp_field, value)
    if value.isdigit():
        temp_field_modifier = '[' + field + " modifier]"
        modifier_value = calculate_modifier(int(value))
        if "level" not in field:
            print("Modifier for {0} is {1}".format(field, modifier_value))

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
        mod_val = calculate_modifier(int(FIELDS['intelligence']))
    elif "animal handling" in match or "insight" in match or "medicine" in match or "perception" in match or "survival" in match:
        mod_val = calculate_modifier(int(FIELDS['wisdom']))
    elif "deception" in match or "intimidation" in match or "performance" in match or "persuasion" in match:
        mod_val = calculate_modifier(int(FIELDS['charisma']))
    elif "athletics" in match:
        mod_val = calculate_modifier(int(FIELDS['strength']))
    elif "acrobatics" in match or "sleight of hand" in match or "stealth" in match:
        mod_val = calculate_modifier(int(FIELDS['dexterity']))

    # Add the proficiency bonus if appropriate
    if match in proficiencies:
        mod_val += proficiency_bonus
        print("Adding proficiency bonus {0} to skill {1}".format(proficiency_bonus, match))

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

info = FIELDS['information']
template = template.replace("[background information]", info)

notes = FIELDS['notes']
template = template.replace("[notes]", notes)

img_src = "img/" + FIELDS['image']
img_filepath = os.path.join(CHAR_DIR, img_src)
img_dir = CHAR_DIR + "/img"
img_desc = img_src.split('/')[1].split('.')[0] + "-image"
template = template.replace("[image-description]", img_desc)
template = template.replace("[image-url]", img_src)

copy_file_to_directory(img_src, img_dir)

# Update abilities
abilities = FIELDS['abilities'].split(',')
abilities_output = ""
for ability in abilities:
    abilities_output += "<li><strong>"
    abilities_output += ability.strip()
    abilities_output += ":</strong>["
    abilities_output += ability.strip()
    abilities_output += " description]</li>"
template = template.replace("[abilities list]", abilities_output)

# Update equipment
equipment = FIELDS['equipment'].split(',')
equipment_output = ""
for equip in equipment:
    equipment_output += "<li><strong>"
    equipment_output += equip.strip()
    equipment_output += ":</strong>["
    equipment_output += equip.strip()
    equipment_output += " description]</li>"
template = template.replace("[equipment list]", equipment_output)

# Write the new character file
with open(filepath, 'w') as f:
    f.write(template)

print(f'Character file created: {filepath}')
