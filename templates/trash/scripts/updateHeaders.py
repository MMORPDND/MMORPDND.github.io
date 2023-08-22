import os
import re

# Define the template file paths
template_file = "templates/headerTemplate.html"
css_path = "css/mmorpdnd.css"

# Define the regular expression to match the header section
header_regex = re.compile(r"<head>.*?</head>", re.DOTALL)

# Define the regular expression to match the header section
title_regex = re.compile(r"<title>.*?</title>", re.DOTALL)

# Loop through all HTML files in the current directory and its subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html") and "Template" not in file:
            # Read the contents of the HTML file
            file_path = os.path.join(root, file)
            
            if ".git" in file_path or ".idea" in file_path:
                continue
                
            with open(file_path, "r") as f:
                contents = f.read()

            # Read the contents of the template file
            with open(template_file, "r") as f:
                template = f.read()

            # Replace the header section with the contents of the template
            contents = re.sub(header_regex, template, contents)
            
            title = "<title>" + file.split('.')[0].replace('_', ' ') + "</title>"
            print(title)
            
            # Replace the title section with the file name
            contents = re.sub(title_regex, title, contents)
                
            # Determine the relative path to the CSS file
            css_relative_path = os.path.relpath(css_path, start=root)
            
            # Determine the number of subdirectories between the HTML file and the CSS file
            num_subdirs = css_relative_path.count(os.sep) - 1
            
            # Create the correct link path for the CSS file
            link_path = "../" * num_subdirs + css_path
            
            # Replace the placeholder with the link to the CSS file
            contents = contents.replace("%OPENAICSS%", f'<link href="{link_path}" rel="stylesheet"/>')
            
            # Overwrite the HTML file with the updated contents 
            with open(file_path, "w") as f:
                f.write(contents)
            
            print(f"Updated head and css in {file_path}")  # Print progress update
