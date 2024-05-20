#!/bin/bash

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "Successfully installed Python dependencies."
else
    echo "Failed to install Python dependencies." >&2
    exit 1
fi

# Install Playwright and its browsers
python -m playwright install
if [ $? -eq 0 ]; then
    echo "Successfully installed Playwright and its browsers."
else
    echo "Failed to install Playwright and its browsers." >&2
    exit 1
fi
