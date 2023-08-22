#!/bin/python3
import requests
from tqdm import tqdm

filename = "links.txt"

with open(filename, "r") as file:
    lines = file.read().splitlines()

for line in tqdm(lines, desc="Checking URLs", unit="line"):
    url = line.split(", ")[1]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pass
            #print(f"{url} exists.")
        else:
            print(f"{url} returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"{url} resulted in an error: {e}")

