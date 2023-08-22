#!/bin/bash

if [[ $(uname) == CYGWIN* ]]; then
    echo "Running in Cygwin"
    rm -vrf campaign
	rm -vrf *.html
	py createDirs.py
	py createDummyHTMLFiles.py
	py createIndexFiles.py
	py updateHeaders.py
	py updateNavigation.py
	py updateIndexLinks.py
	#py updateLinks.py
	py prettyHTML.py
else
    echo "Running in Linux terminal"
    rm -vrf campaign
	rm -vrf *.html
	python3 createDirs.py
	python3 createDummyHTMLFiles.py
	python3 createIndexFiles.py
	python3 updateHeaders.py
	python3 updateNavigation.py
	python3 updateIndexLinks.py
	python3 updateLinks.py
	python3 prettyHTML.py
fi
