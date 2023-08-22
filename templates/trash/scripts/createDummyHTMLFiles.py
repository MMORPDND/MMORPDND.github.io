import os
import random

# Define the number of HTML files to create in each subdirectory
num_files_per_subdirectory = 3

# Get the current directory
current_dir = os.getcwd()
script_directory = os.path.dirname(os.path.abspath(__file__))

# Stores all files created so far.
all_files = []

# Create an index.html file in the current directory
with open(os.path.join(current_dir, "index.html"), "w") as f:
    f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")

# Recursively walk through the directory structure and create HTML files in each subdirectory
for dirpath, dirnames, filenames in os.walk(current_dir):
    for dirname in dirnames:
        if "templates" in dirpath or "css" in dirpath or ".git" in dirpath or ".idea" in dirpath or "templates" in dirname or "css" in dirname or ".git" in dirname or ".idea" in dirname:
        	continue
        # Create an index.html file in each subdirectory
        with open(os.path.join(dirpath, dirname, "index.html"), "w") as f:
            f.write("<html><head></head><body><h1>Welcome to the index page!</h1></body></html>")
        for i in range(num_files_per_subdirectory):
            # Use the current directory name as part of the filename
            filename = f"{dirname}_{i}.html"
            all_files.append(filename.split('.html')[0])  
            random_one = random.choice(all_files)
            random_two = random.choice(all_files)
            with open(os.path.join(dirpath, dirname, filename), "w") as f:
                f.write(f"<html><head></head><body><h1>This is {filename} in {dirname} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")

# Create additional HTML files in the script directory
for i in range(num_files_per_subdirectory):
    # Use the script directory name as part of the filename
    filename = f"{os.path.basename(current_dir)}_{i}.html"
    all_files.append(filename.split('.html')[0])
    random_one = random.choice(all_files)
    random_two = random.choice(all_files)
    with open(os.path.join(current_dir, filename), "w") as f:
        f.write(f"<html><head></head><body><h1>This is {filename} in {current_dir} directory!</h1>Here is a link to {random_one} and {random_two}.</body></html>")

print("HTML files created successfully!")
