import os
import re

nav_file = "templates/navTemplate.html"

# loop through all files in directory and subdirectories
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith(".html") and "Template" not in filename:                
            # open the file and read the contents
            filepath = os.path.join(root, filename)
            
            if ".git" in filepath and ".idea" not in filepath:
                continue
                        
            print(f"Processing file: {filepath}")
            with open(filepath, "r") as file:
                contents = file.read()

            # open the nav file and read the contents
            with open(nav_file, "r") as file:
                nav_contents = file.read()
                
            # Find the navigation block in the original HTML file
            navRegex = re.compile(r'<div class="navigation">(.*?)</div>', re.DOTALL)
            navMatch = navRegex.search(contents)
            
            if navMatch:
                print(" -- Found navigation block")
                # Replace the navigation block with the contents of the template
                contents = contents.replace(navMatch.group(0), nav_contents)

                # Write the modified HTML back to the file
                with open(filepath, 'w') as f:
                    f.write(contents)
                    
                print(" -- Replaced navigation block")
            else:
                print(" -- Navigation block not found")
                
                # insert the nav contents at the start of the body tag
                new_contents = contents.replace("<body>", f"<body>\n{nav_contents}")

                # overwrite the file with the new contents
                with open(filepath, "w") as file:
                    file.write(new_contents)
                    
                print(" -- Inserted nav contents at the start of the body tag")
