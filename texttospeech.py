import os
import base64
import requests
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def createTTS(post_id,input_text):
    # Limit of 300 characters per request.
    max_length = 300
    input_file = os.path.join("posts", f"{post_id}.txt")
    output_file = f"{post_id}.mp3"

    # Split the input text into chunks of maximum length 300 characters
    input_chunks = [input_text[i:i+max_length] for i in range(0, len(input_text), max_length)]

    # Set the speaker ID
    speaker_id = "en_us_010"

    # Set the API endpoint and headers
    url = "https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47'
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

    if os.path.exists(os.path.join("mp3", output_file)):
        print(f"Skipping MP4 creation for {post_id}. File already exists.")
        return None
    
    path = Path("mp3") / output_file
    with open(path, "wb") as f:
        f.write(concatenated_audio_data)
    #upload_to_drive(output_file,"1w4IUHvVJ2S_qJRCceSokCMu9IrDc5a9P")
    print(f"Conversion complete. MP3 file saved as {output_file}.")

    return concatenated_audio_data

def wcreateTTS(post_id):
    # Limit of 300 characters per request.
    max_length = 300
    input_file = os.path.join("posts", f"{post_id}.txt")
    output_file = f"{post_id}.mp3"

    # Load the input text
    with open(input_file, "r") as f:
        input_text = f.read()

    # Split the input text into chunks of maximum length 300 characters
    input_chunks = []
    current_chunk = ""
    for word in input_text.split():
        if len(current_chunk) + len(word) < max_length:
            current_chunk += word + " "
        elif current_chunk != "":
            if current_chunk[-1] in (".", " "):
                input_chunks.append(current_chunk.strip())
                current_chunk = word + " "
            else:
                last_space_index = max(current_chunk.rfind("."), current_chunk.rfind(" "))
                if last_space_index == -1:
                    input_chunks.append(current_chunk.strip())
                    current_chunk = word + " "
                else:
                    input_chunks.append(current_chunk[:last_space_index].strip())
                    current_chunk = current_chunk[last_space_index+1:] + word + " "

    if current_chunk != "":
        input_chunks.append(current_chunk.strip())

    # Set the speaker ID
    speaker_id = "en_us_001"

    # Set the API endpoint and headers
    url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
    headers = {
        'Content-Type': 'application/json'
    }

    # Loop through the input chunks and make API requests for each chunk
    audio_data_list = []
    for input_chunk in input_chunks:
        # Set the request body
        data = {
            "text": input_chunk,
            "voice": speaker_id
        }

        # Send the request and get the response
        r = requests.post(url, headers=headers, json=data)

        # Check for errors
        if r.status_code != 200:
            print(f"Error {r.status_code} occurred for input chunk: {input_chunk}")
            exit()

        # Extract the audio data from the response
        audio_data = base64.b64decode(r.json()["data"])
        audio_data_list.append(audio_data)

    # Concatenate the audio data from all the chunks
    concatenated_audio_data = b"".join(audio_data_list)

    if os.path.exists(os.path.join("mp3", output_file)):
        print(f"Skipping MP4 creation for {post_id}. File already exists.")
        return None
    
    path = Path("mp3") / output_file
    with open(path, "wb") as f:
        f.write(concatenated_audio_data)
    #upload_to_drive(output_file,"1w4IUHvVJ2S_qJRCceSokCMu9IrDc5a9P")
    print(f"Conversion complete. MP3 file saved as {output_file}.")

    return concatenated_audio_data
