#!/bin/python3
import argparse
import glob

def remove_duplicate_lines(file_name):
    print(f"Processing file: {file_name}")
    # Read the contents of the file
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Find duplicate lines
    seen_lines = set()
    duplicate_lines = []
    for line in lines:
        if line in seen_lines:
            duplicate_lines.append(line)
        else:
            seen_lines.add(line)

    # Remove duplicate lines
    unique_lines = list(set(lines))

    # Write the unique lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(unique_lines)

    print(f"Duplicate lines removed from {file_name} successfully.")

    # Print duplicate lines found
    if duplicate_lines:
        print("Duplicate lines found:")
        for line in duplicate_lines:
            print(line.strip())
            
    print("-------------------------------\n")


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Remove duplicate lines from files')

    # Add the file name argument
    parser.add_argument('-f', '--file', type=str, help='Path to the file')

    # Add the all files option
    parser.add_argument('-a', '--all', action='store_true', help='Run against all files in the current folder')

    # Parse the arguments
    args = parser.parse_args()

    # Check if the all files option is provided
    if args.all:
        file_patterns = ['*.names', '*.list']
        files = []
        for pattern in file_patterns:
            files.extend(glob.glob(pattern))
        
        for file in files:
            remove_duplicate_lines(file)
    elif args.file:
        remove_duplicate_lines(args.file)
    else:
        print("Please provide a file name using the -f or --file option, or use the -a or --all option to run against all files in the current folder.")

