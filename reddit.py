import praw
import os
import base64
import requests
from pathlib import Path
if not os.path.exists("posts"):
    os.makedirs("posts")

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id="wsEcf3im17zm6vibQBkOfg",
    client_secret="D3Bpg1bt6z-H8NmqlWOby3OpWiRxUw",
    password="%z9rVMhC_qDtH.P",
    user_agent="Reddit Bot V1.0",
    username="dliaos",
)

# Define subreddit to search and get top posts from past day
subreddit_name = "AmITheAsshole"
posts = reddit.subreddit(subreddit_name).top(time_filter="month", limit=3)

# Define functions

def createTTS(post_id):
    # Limit of 300 characters per request.
    max_length = 300
    input_file = f"{post_id}.txt"
    output_file = f"{post_id}.mp3"
    path = Path("posts") / output_file
    # Split the input text into chunks of maximum length 300 characters
    input_chunks = [input_text[i:i+max_length] for i in range(0, len(input_text), max_length)]

    # Set the speaker ID
    speaker_id = "en_us_010"

    # Set the API endpoint and headers
    url = "https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': 'sessionid=f958b30a3fc8aaea5689737429d9bc05'
    }

    # Loop through the input chunks and make API requests for each chunk
    audio_data_list = []
    for input_chunk in input_chunks:
        # Set the request parameters
        params = {
            "text_speaker": speaker_id,
            "req_text": input_chunk,
            "speaker_map_type": "0",
            "aid": "1233"
        }

        # Send the request and get the response
        r = requests.post(url, headers=headers, params=params)

        # Check for errors
        if r.json()["message"] == "Couldn't load speech. Try again.":
            print("Session ID was not correct, or the service is unavailable")
            exit()
        if r.json()["message"] == "This voice is unavailable now":
            print("Voice ID entered does not exist or was entered incorrectly.")
            exit()

        # Extract the audio data from the response
        audio_data = base64.b64decode(r.json()["data"]["v_str"])
        audio_data_list.append(audio_data)

    # Concatenate the audio data from all the chunks
    concatenated_audio_data = b"".join(audio_data_list)

    with open(output_file, "wb") as f:
        f.write(concatenated_audio_data)

    print(f"Conversion complete. MP3 file saved as {output_file}.")

    return concatenated_audio_data


    

def createPostTextFile(title, body, author, post_id, input_text):
    """
    Creates a text file with post information for text-to-speech processing.
    """
    
    filename = f"{post_id}.txt"
    path = Path("posts") / filename

    with open(path, "w") as file:
        file.write(input_text)

    print(f"Saved post with ID {post_id} to {path}")

# Iterate through each post and create TTS audio and text files
for post in posts:
    title = post.title
    body = post.selftext
    author = post.author
    post_id = post.id

        # Define input text for TTS
    input_text = f"{title} by {author}  {body}"


    # Call function to create text file for the post
    createPostTextFile(title, body, author, post_id,input_text)
    createTTS(post_id)

    # Call function to generate TTS audio file
    #createTTS(title, body, author, post_id, input_text)
