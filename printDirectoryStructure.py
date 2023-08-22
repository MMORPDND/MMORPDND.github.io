#!/bin/python3
import os

def print_directory_contents(path):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print('{}{}'.format(sub_indent, file))

# Get the current working directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))
# Print the contents of the current working directory
print_directory_contents(dir_path)
