# Reddit Video Creator
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
3. Open `reddit_video_creator.py` and enter your `client_id`, `client_secret`, `username`, `password`, and `user_agent` in the appropriate fields.
4. Define the subreddit you want to get posts from by changing the `subreddit_name` variable.
5. Run the script using the following command:


This will create a video for each of the top posts on the subreddit, using a random video from the videos directory as a background.

How it works
The script uses the PRAW (Python Reddit API Wrapper) library to access Reddit's API and retrieve the top posts from a subreddit. For each post, it performs the following steps:

Use text-to-speech to convert the post's text into an MP3 file.
Choose a random video from the videos directory and concatenate it with the MP3 file using the moviepy library.
Save the resulting video as an MP4 file.
Limitations
The script only works with subreddits that allow text posts.
The script uses a fixed set of voice and video files, so the output videos may not be very diverse. You can add your own voice and video files to the voices and videos directories, respectively, to increase the variety.
The quality of the text-to-speech output may not be very good, especially for longer posts. You can experiment with different text-to-speech services to get better results.

## Limitations
- The script only works with subreddits that allow text posts.
- The script uses a fixed set of voice and video files, so the output videos may not be very diverse. You can add your own voice and video files to the `voices` and `videos` directories, respectively, to increase the variety.
- The quality of the text-to-speech output may not be very good, especially for longer posts. You can experiment with different text-to-speech services to get better results.

## Disclaimer
This script is for educational purposes only. Please respect Reddit's API rules and do not use this script to spam or harass Reddit users.
