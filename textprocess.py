import os
from pathlib import Path

def preprocessText(post_id):
    file_path = os.path.abspath(f'posts/{post_id}.txt')

    with open(file_path, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    # Replace all asterisks with empty string
    file_contents = file_contents.replace('*', '')

    # Replace all parentheses with empty string
    file_contents = file_contents.replace('(', '')
    file_contents = file_contents.replace(')', '')

    # Replaces European single quotes with American ones, this ruins the TTS.
    file_contents = file_contents.replace("’","'")


    # Write the updated contents back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_contents)

def createPostTextFile(title, body, author, post_id, input_text):
    """
    Creates a text file with post information for text-to-speech processing.
    """
    
    filename = f"{post_id}.txt"
    path = Path("posts") / filename

    if os.path.exists(os.path.join("posts", filename)):
        print(f"Skipping TXT creation for {post_id}. File already exists.")
        return None

    with open(path, "w") as file:
        file.write(input_text)

    print(f"Saved post with ID {post_id} to {path}")