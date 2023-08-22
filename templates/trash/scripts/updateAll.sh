#!/bin/bash

if [[ $(uname) == CYGWIN* ]]; then
    echo "Running in Cygwin"
	py createIndexFiles.py
	py updateHeaders.py
	py updateNavigation.py
	py updateIndexLinks.py
	py updateLinks.py
	py prettyHTML.py
else
    echo "Running in Linux terminal"
	python3 createIndexFiles.py
	python3 updateHeaders.py
	python3 updateNavigation.py
	python3 updateIndexLinks.py
	python3 updateLinks.py
	python3 prettyHTML.py
fi
