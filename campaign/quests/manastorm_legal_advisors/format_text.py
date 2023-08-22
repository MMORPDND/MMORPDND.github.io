#!/bin/python3
import argparse
import re

def format_single_line(text):
    """
    Formats the input text into a single line with proper spacings.

    Args:
        text (str): The input text to format.

    Returns:
        str: The formatted text in a single line.
    """
    # Remove newline characters and tabs
    text = text.replace('\n', ' ').replace('\t', ' ')

    # Add spaces after punctuations
    punctuations = ['.', ',', ';', ':', '!', '?']
    for punctuation in punctuations:
        text = text.replace(punctuation, punctuation + ' ')

    # Replace multiple consecutive spaces with a single space
    text = re.sub(' +', ' ', text)

    # Remove extra spaces before and after the text
    text = text.strip()

    return text


# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Specify the input file', required=True)
args = parser.parse_args()

# Read input file
file_path = args.file
with open(file_path, 'r') as file:
    input_text = file.read()

# Format input text to a single line
formatted_text = format_single_line(input_text)
print(formatted_text)
