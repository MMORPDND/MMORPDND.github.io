import os
import re

def update_index_files():
    # Get list of all HTML files in directory and subdirectories
    html_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith("index.html") and "Template" not in file and ".git" not in root and ".idea" not in root:
                html_files.append(os.path.join(root, file))

    # Loop through each HTML file found
    for file in html_files:
        with open(file, 'r+') as f:
            file_data = f.read()

            # Find all HTML files in same directory as current file
            dir_path = os.path.dirname(file)
            html_files_in_dir = []
            for f_name in os.listdir(dir_path):
                if f_name.endswith(".html"):
                    html_files_in_dir.append(f_name)

            # Create index links div section if it does not exist
            index_links_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*>.*?</div>'
            index_links_match = re.search(index_links_pattern, file_data, re.DOTALL)
            if not index_links_match:
                index_links_div = '<div class="indexLinks"><ul></ul></div>'
                file_data = re.sub(r'</body>', index_links_div + '\n</body>', file_data)

            # Update index links
            index_links_div_pattern = r'<div\s+class\s*=\s*["\']indexLinks["\']\s*><ul>'
            index_links_div_match = re.search(index_links_div_pattern, file_data, re.DOTALL)
            index_links_div = index_links_div_match.group(0) if index_links_div_match else '<div class="indexLinks"><ul>'
            index_links = ''
            for html_file in html_files_in_dir:
                if html_file != 'index.html':
                    link_text = html_file.replace('.html', '')
                    link = f'<li><a href="{html_file}">{link_text}</a></li>'
                    index_links += f'{link}\n'

            # Replace index links in file
            updated_data = re.sub(index_links_pattern, index_links_div + '\n' + index_links + '</ul></div>', file_data, flags=re.DOTALL)
            
            # Write updated file data to file
            f.seek(0)
            f.write(updated_data)
            f.truncate()

update_index_files()
