from __future__ import print_function
import praw
import os
import base64
import requests
import random
import os
import sys
import moviepy
import speech_recognition as sr
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

if not os.path.exists("srt"):
    os.makedirs("srt")

if not os.path.exists("posts"):
    os.makedirs("posts")

if not os.path.exists("mp3"):
    os.makedirs("mp3")

if not os.path.exists("mp4"):
    os.makedirs("mp4")


# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id="wsEcf3im17zm6vibQBkOfg",
    client_secret="D3Bpg1bt6z-H8NmqlWOby3OpWiRxUw",
    password="%z9rVMhC_qDtH.P",
    user_agent="Reddit Bot V1.0",
    username="dliaos",
)

# Define subreddit to search and get top posts from past day
subreddit_name = "Confessions" #Confessions #ProRevenge #AmITheAsshole
posts = reddit.subreddit(subreddit_name).top(time_filter="month", limit=10)

# Define functions

def createTTS(post_id):
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

    path = Path("mp3") / output_file
    with open(path, "wb") as f:
        f.write(concatenated_audio_data)
    #upload_to_drive(output_file,"1w4IUHvVJ2S_qJRCceSokCMu9IrDc5a9P")
    print(f"Conversion complete. MP3 file saved as {output_file}.")

    return concatenated_audio_data

def createVideo(post_id):
    mp3_file = os.path.join("mp3", f"{post_id}.mp3")
    video_files = [file for file in os.listdir("videos") if file.endswith(".mov")]
    random.shuffle(video_files)
    output_file = f"{post_id}.mp4"
    
    for mp4_file in video_files:
        audio_clip = AudioFileClip(mp3_file)
        video_clip = VideoFileClip(os.path.join("videos", mp4_file))
        
        if audio_clip.duration <= video_clip.duration:
            video_clip = video_clip.set_duration(audio_clip.duration)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(os.path.join("mp4", f"{post_id}.mp4"), fps=24,codec = 'libx264',bitrate='5000k',threads=2)
            #upload_to_drive(output_file,"1FOsmjDwtzOem37SqfjfPFr2LEL4PErxL")
            return
        
    print("No video found for the given audio duration.")

def createVideoMov(post_id):
    mp3_file = os.path.join("mp3", f"{post_id}.mp3")
    video_files = [file for file in os.listdir("videos") if file.endswith(".mov")]
    random.shuffle(video_files)

    for mov_file in video_files:
        audio_clip = AudioFileClip(mp3_file)
        video_clip = VideoFileClip(os.path.join("videos", mov_file))

        if audio_clip.duration <= video_clip.duration:
            video_clip = video_clip.set_duration(audio_clip.duration)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(os.path.join("mov", f"{post_id}.mov"), fps=24, codec='png', bitrate='5000k')
            return

    print("No video found for the given audio duration.")



def createPostTextFile(title, body, author, post_id, input_text):
    """
    Creates a text file with post information for text-to-speech processing.
    """
    
    filename = f"{post_id}.txt"
    path = Path("posts") / filename

    with open(path, "w") as file:
        file.write(input_text)

    print(f"Saved post with ID {post_id} to {path}")

def create_srt_file(post_id):
    # Initialize the SpeechRecognition recognizer
    r = sr.Recognizer()
    input_file = os.path.join("mp4", f"{post_id}.mp4")
    output_file = f"{post_id}.srt"
    # Load the video and audio
    video = VideoFileClip(input_file)
    audio = video.audio

    # Create a WAV audio file
    audio_file = f"{post_id}.wav"
    audio.write_audiofile(audio_file)

    # Recognize the speech in the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        transcript = r.recognize_google(audio_data)

    # Divide the transcript into subtitle-sized chunks
    duration = video.duration
    num_subtitles = 50  # Change this to adjust the number of subtitles
    subtitle_duration = duration / num_subtitles
    subtitle_chunks = [transcript[int(i*len(transcript)/num_subtitles):int((i+1)*len(transcript)/num_subtitles)] for i in range(num_subtitles)]

    # Write the SRT file
    with open(os.path.join("srt", f'{post_id}.srt'), 'w') as f:
        for i, chunk in enumerate(subtitle_chunks):
            start_time = i * subtitle_duration
            end_time = (i+1) * subtitle_duration
            subtitle_text = chunk.replace('\n', ' ')
            subtitle_text = ' '.join(subtitle_text.split())
            f.write(f"{i+1}\n{format_time(start_time)} --> {format_time(end_time)}\n{subtitle_text}\n\n")

    #upload_to_drive(output_file,"1FOsmjDwtzOem37SqfjfPFr2LEL4PErxL")


def format_time(seconds):
    h, m, s = 0, 0, 0
    ms = int(seconds * 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(int(h), int(m), int(s), int(ms))

def add_subtitles(post_id):
    #mp4_file_path = f"mov/{post_id}.mov"
    mp4_file_path = f"mp4/{post_id}.mp4"
    srt_file_path = f"srt/{post_id}.srt"
    output_file = f"{post_id}.mp4"
    # Load the video file
    video_clip = VideoFileClip(mp4_file_path)

    # Load the subtitle file
    subtitle_generator = lambda txt: TextClip(txt, fontsize=74, font='Arial', color='white')
    subtitles = SubtitlesClip(srt_file_path, subtitle_generator)

    # Set the subtitles position and duration
    subtitles = subtitles.set_position(("center", "center")).set_duration(video_clip.duration)

    # Combine the video clip and subtitles clip
    final_clip = CompositeVideoClip([video_clip, subtitles])

    # Save the final clip
    if not os.path.exists("results"):
        os.makedirs("results")
    #final_clip.write_videofile(f"results/subtitled{post_id}.mov")
    final_clip.write_videofile(f"results/subtitled{post_id}.mp4")
    #upload_to_drive(output_file,"1JDtzqDe--FNVBFMM2D8D7JH2k3nWiQGY")

def checkPostId(post_id):
    with open('post_ids.txt', 'r') as f:
        if post_id in f.read():
            return True
    return False

def addPostId(post_id):
    with open('post_ids.txt', 'a') as f:
        f.write(post_id + '\n')

def upload_to_drive(file_name,folder_id):
    """Uploads the specified file to Google Drive.

    Args:
        file_name (str): The name of the file to be uploaded.

    Returns:
        None
    """
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    arguments = ["-f", "-fs"]

    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        # build the Drive API client
        service = build("drive", "v3", credentials=creds)

        # create a MediaFileUpload object for the file
        file = MediaFileUpload(file_name, mimetype="image/jpg", resumable=True)

        # create a file resource with metadata
        file_metadata = {"name": file_name, "parents": [folder_id]}

        # send a request to upload the file
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=file, fields="id")
            .execute()
        )

        print(
            f'File {file_name} uploaded 😎 to Google Drive with 🆔: {uploaded_file.get("id")} ✨'
        )

    except HttpError as error:
        print(f"An error occurred: {error}")


# Iterate through each post and create TTS audio and text files
for post in posts:
    title = post.title
    body = post.selftext
    author = post.author
    post_id = post.id

    # Define input text for TTS
    input_text = f"{title} by {author}  {body}"

    # Check if post_id already exists
    if not checkPostId(post_id):
        # Call function to create text file for the post
        createPostTextFile(title, body, author, post_id,input_text)
        createTTS(post_id)
        createVideo(post_id)
        #createVideoMov(post_id)
        create_srt_file(post_id)
        #add_subtitles(post_id)
        addPostId(post_id)