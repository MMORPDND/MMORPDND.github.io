#!/usr/bin/env python3

import argparse
import re


def replace_newlines(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()

        modified_content = re.sub(r'(?<!\=)\n\n\s\s\s\s\*', ';*', content)
        modified_content = re.sub(r'(?<!\=)\n\n\s\s\s\s', ';-', modified_content)
        modified_content = re.sub(r'(?<!\=)\n\n', ';', modified_content)

        modified_lines = modified_content.split(';')
        finalized_content = ""

        for line in modified_lines:

            if "folder=" in line or "[dnd-image]=" in line:
                if finalized_content != "":
                    finalized_content += '\n\n'
                finalized_content += line
                continue

            if "[dnd-info]=" in line:
                if finalized_content != "":
                    finalized_content += '\n\n'
                finalized_content += line
                continue

            if "=" not in line:
                finalized_content += ';'
                finalized_content += line

        finalized_content.lstrip('\n')

        # Remove the last semicolon.
        if finalized_content.endswith(";"):
            finalized_content = finalized_content[:-1]

        print(finalized_content)

        with open(filename, 'w') as file:
            file.write(finalized_content)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")


# Create an argument parser
parser = argparse.ArgumentParser(description="Replace newlines in a file")

# Add the filename argument
parser.add_argument("-f", "--filename", required=True, help="The name of the file to process")

# Parse the command-line arguments
args = parser.parse_args()

# Call the function with the provided filename
replace_newlines(args.filename)
