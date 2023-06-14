# READ 
.gitignore didn't gitignore. Currently Uploading does not work, which is why it's commented out.
# Auto Reddit Stories
This Python script allows you to create videos from top posts on a subreddit, using text-to-speech and a collection of videos in a directory. The resulting video will contain the text from the post, spoken by a virtual assistant, with a background video.

## Requirements
You need to have Python 3.x installed on your system to run this script. Additionally, you need to install the following Python modules:

- PRAW
- requests
- moviepy
- speech_recognition

To install them, use the following command:

pip install praw requests moviepy SpeechRecognition


## Usage
1. Clone this repository to your local machine.
2. Create a Reddit app on the Reddit website. This will give you a client_id and a client_secret.
3. Go to TikTok and get your session ID from the applications tab.
4. Fill in your info in the .env file.
6. Run the script


This will create a video for each of the top posts on the subreddit, using a random video from the videos directory as a background.

## How it works
The script uses the PRAW (Python Reddit API Wrapper) library to access Reddit's API and retrieve the top posts from a subreddit. For each post, it performs the following steps:

Use text-to-speech to convert the post's text into an MP3 file.
Choose a random video from the videos directory and concatenate it with the MP3 file using the moviepy library.
Save the resulting video as an MP4 file.
Use Speech to Text to generate subtitles, not sure if we can use the prior script to make this more accurate.

# Limitations
This is obviously exclusively for text posts.

The quality of the TTS is quite inconsistant, and occasionally varies in speed(?) 

## To-Do
1. Limit size/length of finalized file, and split it up for TikTok
2. Threading since transcription takes a while

## Acknowledgements 
https://github.com/abdeladim-s/subsai
https://github.com/546200350/TikTokUploder
https://github.com/Weilbyte/tiktok-tts
