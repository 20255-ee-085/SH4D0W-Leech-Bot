#!/bin/bash

# Create required directories
mkdir -p downloads/{pdfs,videos,documents}

# Install dependencies
pip install -r requirements.txt

# Run the bot
python -u main.py