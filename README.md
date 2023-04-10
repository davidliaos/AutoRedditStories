Reddit Text-to-Speech Bot
This script is a Reddit bot that utilizes the PRAW library to retrieve top posts from a specified subreddit and convert the post's text into an MP3 file using TikTok's text-to-speech API. The bot then saves both the MP3 file and the post's information in a text file for later use.

Setup
Before running the script, make sure to have the following installed:

Python 3
PRAW
Requests
pathlib
You will also need to have a Reddit API client ID and secret key and a TikTok session ID (cookie) to use the text-to-speech API.

How to use
Clone or download the repository.
Install the required libraries listed above.
Enter your Reddit API credentials, TikTok session ID, and the subreddit to search in the script.
Run the script using python script.py.
The script will retrieve the top posts from the specified subreddit and convert their text into MP3 files using TikTok's text-to-speech API.
The MP3 files and post information text files will be saved in a folder named "posts".
Notes
The createTTS() function is commented out by default to prevent excessive requests to TikTok's API. Uncomment it to generate the TTS audio files.
This script is just a proof of concept and should not be used for any commercial purposes.
Be sure to follow Reddit's API guidelines and TikTok's Terms of Service when using their APIs.
