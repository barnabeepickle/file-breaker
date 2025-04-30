#!/bin/bash

echo "This script will build both the file-breaker library and the breaker_cli tool."

# First we build the library
echo "Building library..."
python3 -m pip install --upgrade build
python3 -m build
echo "...Library built"
# Now we need to push out our new build
echo "New build must now be published"
python3 -m pip install --upgrade twine
echo "You will be asked to provided a token"
python3 -m twine upload dist/*

# Now it comes time to build breaker_cli
echo "Now building breaker_cli"
pip install -U pyinstaller
pip install -r code/requirements.txt
pyinstaller code/breaker_cli.py --hiddenimport file-breaker
echo "Build complete"
echo "Exiting"