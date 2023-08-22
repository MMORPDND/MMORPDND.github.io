#!/bin/python3
import os

# Define the directory structure
structure = {
    "campaign": {
        "locations": {
            "regions": {},
            "dungeons": {},
            "cities": {},
            "landmarks": {},
            "towns": {}
        },
        "items": {
            "consumables": {
                "potions": {},
                "food": {},
                "drink": {}
            },
            "magic": {},
            "weapons": {},
            "armor": {},
            "trinkets": {}
        },
        "notes": {},
        "creatures": {
            "animals": {},
            "monsters": {}
        },
        "lore": {
            "history": {},
            "factions": {},
            "races": {},
            "classes": {},
            "backgrounds": {},
            "deities": {}
        },
        "quests": {},
        "characters": {
            "player": {},
            "non-player": {}
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
        }
    }
}

# Define the root directory
root_dir = "."

# Define a function to create directories recursively
def create_dirs(path: str, structure: dict) -> None:
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
            create_dirs(os.path.join(path, key), structure[key])

# Call the function to create the directories
create_dirs(root_dir, structure)

