#!/bin/python3
import requests
from bs4 import BeautifulSoup
import re

def extract_link_and_text(s):
    match = re.search(r'<a href="([^"]*)">(.*?)</a>', s)
    if match:
        link = match.group(1)
        text = match.group(2)
        return link, text
    else:
        return None, None

base_url = "https://roll20.net/compendium/dnd5e/"

filename = "templates/lists/scrape.txt"

monsters = []
count = 0

with open(filename, "r") as file:
    text = file.read()

    # Split text into individual entries
    entries = text.split("\n\n")

    for entry in entries:
        if count % 2 ==0:
            lines = entry.split("\n")
        else:            
            # Split entry into lines
            newlines = entry.split("\n")
            for line in newlines:
                lines.append(line.strip())
            print(lines)
            name = lines[0]
            size_type_alignment = lines[1].split(", ")
            size = size_type_alignment[0].split(' ')[0]
            monster_type = size_type_alignment[0].split(' ')[0]
            alignment = size_type_alignment[1] 
            hp = lines[3].split("Armor Class:")[0].strip()
            ac = lines[4].split("Speed:")[0].strip()
            speed = lines[5].split("Challenge Rating:")[0].strip()
            cr = lines[6].strip()
            
            # Create dictionary with parsed fields
            monster = {
                "name": name,
                "size": size,
                "type": monster_type,
                "alignment": alignment,
                "hp": hp,
                "ac": ac,
                "speed": speed,
                "cr": cr
            }
            
            monsters.append(monster)
        count += 1

for monster in monsters:
    print(monster)
    print("-------------------------")
    
for monster in monsters:
    name = monster['name']
    link = base_url + name.replace(' ', "%20")
    print(name + ", " + link)
