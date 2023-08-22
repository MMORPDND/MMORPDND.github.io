#!/bin/bash

# This script will run the setup needed for the mmorpdnd package!
if [[ $(uname) == Linux ]]; then
    echo "Running setup for Linux!"
    sudo apt-get install python3
    sudo apt-get install python3-pip
    sudo apt-get install python3-tk
    pip3 install bs4
    pip3 install regex
    pip3 install BeautifulSoup
    pip3 install cssbeautifier
    pip3 install tqdm

else
    echo "Setup not yet configured for your system!"
fi
