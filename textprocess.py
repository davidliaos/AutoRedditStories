import os
import re
from pathlib import Path

def preprocessText(post_id):
    
    file_path = os.path.abspath(f'posts/{post_id}.txt')

    with open(file_path, 'r', encoding='utf-8') as f:
        file_contents = f.read()
    file_contents = removeUnicode(file_contents)
    # Replace all asterisks with empty string
    file_contents = file_contents.replace('*', '')
    
    # Replace all parentheses with empty string
    file_contents = file_contents.replace('(', '')
    file_contents = file_contents.replace(')', '')

    # Replaces European single quotes with American ones, this ruins the TTS.
    file_contents = file_contents.replace("’","'")
    file_contents = file_contents.replace("‘","'")
    file_contents = file_contents.replace(';', '.')
    file_contents = file_contents.replace('“', '"')
    file_contents = file_contents.replace(',', ',')
    file_contents = file_contents.replace('“', '"')
    file_contents = file_contents.replace('”', '"')
    file_contents = file_contents.replace('_', ' ')
    file_contents = file_contents.replace('…', '"')
    file_contents = file_contents.replace('TIFU', 'T.I.F.U')
    file_contents = file_contents.replace('AITA', 'A.I.T.A')
    file_contents = file_contents.replace('A-I-T-A ', 'A.I.T.A')
    file_contents = file_contents.replace('WIBTA', 'W.I.B.T.A')
    #removes links 
    file_contents = re.sub(r'http\S+', '', file_contents) # Remove any links starting with http
    file_contents = re.sub(r'www\.\S+', '', file_contents) # Remove any links starting with www
    #removes silly unicode emojis
    file_contents = file_contents.replace('♥️', ' ')
    file_contents = file_contents.replace('😂', ' ')
    # Write the updated contents back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_contents)

def preprocessString(text):
    # Replace all asterisks with empty string
    text = text.replace('*', '')
    text = re.sub(r'http\S+', '', text) # Remove any links starting with http
    text = re.sub(r'www\.\S+', '', text) # Remove any links starting with www
    
    # Replace all parentheses with empty string
    text = text.replace('(', '')
    text = text.replace(')', '')

    # Replaces European single quotes with American ones, this ruins the TTS.
    text = text.replace("’","'")
    text = text.replace("‘","'")
    text = text.replace(';', '.')
    text = text.replace('.', '.')
    text = text.replace(',', ',')
    
    # Replace words for TTS to process easier and more consistently.
    text = text.replace('TIFU', 'T.I.F.U')
    text = text.replace('AITA', 'A.I.T.A')
    text = text.replace('A-A-T-A', 'A.I.T.A')

    return text

def removeUnicode(text):
    # Create an empty list to store the individual characters of the new text
    new_text_chars = []
    
    # Iterate over each character in the text
    for char in text:
        # Check if the character is a Unicode character
        if ord(char) > 127:
            # If the character is a Unicode character, skip it
            continue
        # If the character is not a Unicode character, add it to the new text
        new_text_chars.append(char)
    
    # Combine the characters of the new text into a single string and return it
    new_text = "".join(new_text_chars)
    return new_text


def processSRT(post_id):
    file_path = os.path.abspath(f'srt/{post_id}.srt')

    with open(file_path, 'r', encoding='utf-8') as f:
        file_contents = f.read()

    # Replace all asterisks with empty string
    file_contents = file_contents.replace('aita', 'AITA')
    file_contents = file_contents.replace('aida', 'AITA')
    file_contents = file_contents.replace('Wipta', 'WIBTA')
    file_contents = file_contents.replace('Ida', 'AITA')
    file_contents = file_contents.replace('A-A-T-A ', 'AITA')
    file_contents = file_contents.replace('AATA', 'AITA')
    file_contents = file_contents.replace('Typhoo', 'TIFU')
    file_contents = file_contents.replace('A-T-A ', 'AITA')
    file_contents = file_contents.replace('I.T.A.', 'AITA')
    file_contents = file_contents.replace('A-I-T-A ', 'AITA')
    # Replace all parentheses with empty string
    file_contents = file_contents.replace('(', '')
    file_contents = file_contents.replace(')', '')

    # Replaces European single quotes with American ones, this ruins the TTS.
    file_contents = file_contents.replace("’","'")
    file_contents = file_contents.replace("‘","'")
    file_contents = file_contents.replace(';', '.')
    file_contents = file_contents.replace('“', '"')
    file_contents = file_contents.replace(',', ',')
    file_contents = file_contents.replace('“', '"')
    file_contents = file_contents.replace('”', '"')
        

    # Write the updated contents back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_contents)


def createPostTextFile(title, body, author, post_id, input_text):
    """
    Creates a text file with post information for text-to-speech processing.
    """
    
    filename = f"{post_id}.txt"
    path = Path("posts") / filename
    preprocessString(body)
    if os.path.exists(os.path.join("posts", filename)):
        print(f"{post_id} - Skipping TXT creation for {post_id}. File already exists.")
        return None

    with open(path, "w") as file:
        file.write(input_text)

    print(f"Saved post with ID {post_id} to {path}")

def identifyUnicode(text):
    removeUnicode(text)
    text = removeUnicode(text)
    # Create an empty dictionary to store the count of each Unicode character
    char_counts = {}
    
    # Iterate over each character in the text
    for char in text:
        # Ignore letters (capital or lowercase)
        if char.isalpha():
            continue
        # Check if the character is a Unicode character
        if ord(char) > 127:
            # If the character is not already in the dictionary, add it with a count of 1
            if char not in char_counts:
                char_counts[char] = 1
            # If the character is already in the dictionary, increment its count
            else:
                char_counts[char] += 1
    
    # Output the Unicode characters and their counts in the desired format
    if char_counts:
        for char, count in char_counts.items():
            print(f"Unicode ({ord(char)}), {char}, shown ({count}) times")
    else:
        print("No Unicode characters were found outside of the ASCII range")

        