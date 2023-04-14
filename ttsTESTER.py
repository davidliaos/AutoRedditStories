import requests, base64, random, os

# Limit of 300 characters per request.
max_length = 300

# Set the input and output file paths
input_file = "11sv6o7.txt"
output_file = "11sv6o7.mp3"

# Read the input text from file
with open(input_file, "r") as f:
    input_text = f.read()

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

# Write the audio data to file
with open(output_file, "wb") as f:
    f.write(concatenated_audio_data)

print("Conversion complete.")