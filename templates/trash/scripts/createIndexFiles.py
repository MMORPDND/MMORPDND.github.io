import os

def create_index_files():
    # Loop through all directories and files starting from the current directory
    for root, dirs, files in os.walk("."):
        # Create index file in current directory
        index_file_path = os.path.join(root, "index.html")
        
        # Skip this directory if index.html already exists or if it's in a directory to exclude
        if os.path.exists(index_file_path) or "templates" in index_file_path or "css" in index_file_path or ".git" in index_file_path or ".idea" in index_file_path:
            continue

        directory_name = os.path.basename(root)
        # Create the index.html file and write the HTML content to it
        with open(index_file_path, 'w') as f:
            f.write(f"<html>\n<head>\n<title>Index of {directory_name}</title>\n</head>\n<body>\n")
            f.write(f"<h1>Index of {directory_name}</h1>\n</body>\n</html>\n")
        print(f"Created index file at {index_file_path}")

create_index_files()
