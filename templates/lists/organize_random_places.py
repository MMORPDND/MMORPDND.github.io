#!/bin/python3

def sort_locations_by_last_word(file_path):
    """
    Sorts the location names in the file based on the last word in each item.

    Args:
        file_path (str): The path to the file containing the location names.

    Returns:
        dict: A dictionary where the keys are the last words and the values are lists of location names.
    """
    location_groups = {}

    # Read the file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            location = line.strip()
            last_word = location.split()[-1]

            # Add the location to the corresponding group based on the last word
            if last_word in location_groups:
                location_groups[last_word].append(location)
            else:
                location_groups[last_word] = [location]

    return location_groups


input_file_path = "./random_place.names"

result = sort_locations_by_last_word(input_file_path)

output_file_path = "./random_place_sorted.names"

with open(output_file_path, 'w') as f:
    # Print the sorted location groups
    for last_word, locations in result.items():
        f.write(f"'{last_word}' Locations\n")
        f.write(f"-----------------------\n")
        for location in locations:
            f.write(location + '\n')
        f.write('\n')

