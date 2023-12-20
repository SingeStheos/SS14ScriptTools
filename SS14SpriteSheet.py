# Created by SingeStheos
# Licensed under MIT
# Distribute verbatim, 
# including license.

import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse

# Customize these variables to control the behavior of the program
IGNORE_FILES = False  # Set to True to ignore files with specific text in their name
IGNORE_TEXTS = ["inhand"]  # Specify the texts to ignore in file names. Add more by adding a comma, then an additional text in quotation marks.

#Example: ["inhand", "example"]

def convert_to_api_url(github_url):
    # If it's already an API URL, return as-is
    if "api.github.com" in github_url:
        return github_url

    # Parse the GitHub web URL to extract the repository and path
    parsed_url = urlparse(github_url)
    path_parts = parsed_url.path.split("/")

    # Extract username and repository
    username = path_parts[1]
    repo_name = path_parts[2]

    # Extract branch or default to "main"
    branch = path_parts[4] if len(path_parts) > 4 else "main"

    # Extract the path
    path = "/".join(path_parts[5:])

    # Construct the API URL
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}?ref={branch}"

    return api_url

def should_ignore_file(file_name):
    return any(ignore_text in file_name for ignore_text in IGNORE_TEXTS)

def download_and_combine_spritesheet(github_url, save_path):
    # Convert GitHub web URL to API URL if needed
    github_api_url = convert_to_api_url(github_url)

    try:
        # Fetch PNG files directly over HTTP
        response = requests.get(github_api_url)

        if response.status_code == 200:
            files = response.json()

            # Filter out files based on IGNORE_FILES and IGNORE_TEXTS
            if IGNORE_FILES:
                files = [file for file in files if file['name'].endswith('.png') and not should_ignore_file(file['name'])]
            else:
                files = [file for file in files if file['name'].endswith('.png')]

            if files:
                images = [Image.open(BytesIO(requests.get(file['download_url']).content)) for file in files]

                # Find the maximum dimensions among all images
                max_width = max(img.width for img in images)
                max_height = max(img.height for img in images)

                # Arrange PNGs in a grid based on a square or nearly square layout
                num_files = len(images)
                cols = int(num_files**0.5)
                rows = (num_files + cols - 1) // cols

                spritesheet = Image.new('RGBA', (max_width * cols, max_height * rows))

                for i, img in enumerate(images):
                    row = i // cols
                    col = i % cols
                    spritesheet.paste(img, (col * max_width, row * max_height))

                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                filename = f'spritesheet_{timestamp}.png'
                save_path = os.path.join(save_path, filename)

                # Ensure the directory exists before saving
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                spritesheet.save(save_path)
                print(f'Spritesheet created successfully. Saved to {save_path}')
            else:
                print('No PNG files found in the specified directory.')
        else:
            print(f'Failed to fetch GitHub content. Status code: {response.status_code}')

    except Exception as e:
        print(f'Error: {e}')

# Example usage:
github_url = input('This file contains options you may change. Open the file in a text editor to see.\nInsert GitHub link: ')
# Use the directory of the Python script as the save_path
save_path = os.path.dirname(os.path.realpath(__file__))
download_and_combine_spritesheet(github_url, save_path)
