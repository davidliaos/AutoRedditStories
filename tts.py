import requests
import base64
import random
import os
#This file refuses to work, need to use the ttstester file instead to manually create the mp3.
def createTTS(title, body, author, post_id,input_text):
    # Set the input and output file paths
    output_file = os.path.join('posts', f"{post_id}.mp3")
    input_filename = os.path.join (f"{post_id}_input.txt")
    input_path = os.path.join("posts", input_filename)
    with open(input_path, "w") as file:
        file.write(input_text)
    print(f"Saved input text for post with ID {post_id} to {input_path}")


    # Set the speaker ID
    speaker_id = "en_us_010"

    # Set the API endpoint and headers
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={speaker_id}&req_text={input_text}&speaker_map_type=0&aid=1233"
    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': 'sessionid=f958b30a3fc8aaea5689737429d9bc05'
    }

    # Send the request and get the response
    try:
        r = requests.post(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return

    # Check for errors
    if r.json()["message"] == "Couldn't load speech. Try again.":
        print("Session ID was not correct, or the service is unavailable")
        return
    elif r.json()["message"] == "This voice is unavailable now":
        print("Voice ID entered does not exist or was entered incorrectly.")
        return
    elif "data" not in r.json() or "v_str" not in r.json()["data"]:
        print("No audio data found in the response.")
        return

    # Extract the audio data from the response
    try:
        audio_data = base64.b64decode(r.json()["data"]["v_str"])
    except Exception as err:
        print(f"Error decoding audio data: {err}")
        return

    # Write the audio data to file
    try:
        with open(output_file, "wb") as f:
            f.write(audio_data)
    except Exception as err:
        print(f"Error writing audio data to file: {err}")
        return

    print(f"Conversion complete. MP3 file saved as {output_file}.")
