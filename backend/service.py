import os
import json

# Get the current directory and path to pictures.json
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

def get_data():
    """Load and return the list of pictures from pictures.json"""
    with open(json_url, 'r') as f:
        return json.load(f)