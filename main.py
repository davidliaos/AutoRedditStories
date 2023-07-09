import praw
import os
import random
import time
from uploader import uploadVideo
from texttospeech import createTTS, wcreateTTS
from subtitles import createsrt, format_time, get_screen_size, subtitle_generator, add_subtitles
from videocreation import createVideo, createVideoMov
from textprocess import createPostTextFile, preprocessText
from dotenv import load_dotenv

#choices for randomlym selected captions
TITLES = ["thoughts?", "opinions?", "what do you think?", "let's discuss"]
#randomizes the choices
TITLE = random.choice(TITLES)
#list of hashtags for the post
TAGS = ["aita", "askreddit", "redditstories","tifu","redditreadings"]
#randomizes the order of the hashtags to seem more human
random.shuffle(TAGS)
USERS = []
SESSION_ID = os.getenv('SESSION_ID')
url_prefix = "us"
schedule_time = 1800 # uploads every 30 minutes to not get shadowbanned, you can change it but its not gonna be my problem if you do

# create directories if they do not exist
directories = ["srt", "posts", "mp3", "mp4", "wav", "results"]
for dir in directories:
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"{dir} directory does not exist, creating.")

# create text files if they do not exist
text_files = ['post_ids.txt', 'uploaded_ids.txt']
for text_file in text_files:
    if not os.path.exists(text_file):
        with open(text_file, 'w') as file:
            pass
        print(f"'{text_file}' does not exist, creating.")

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    password=os.environ["REDDIT_PASSWORD"],
    user_agent=os.environ["REDDIT_USER_AGENT"],
    username=os.environ["REDDIT_USERNAME"],
)

subreddit_name = os.environ["SUBREDDIT_NAME"]
post_limit = int(os.environ["POST_LIMIT"])
time_filter = os.environ["TIME_FILTER"]

posts = reddit.subreddit(subreddit_name).top(time_filter=time_filter, limit=post_limit)

# Define functions
def checkPostId(post_id):
    with open('post_ids.txt', 'r') as f:
        if post_id in f.read():
            return True
    return False

def addPostId(post_id):
    try:
        with open('post_ids.txt', 'a') as f:
            f.write(post_id + '\n')
    except FileNotFoundError:
        with open('post_ids.txt', 'w') as f:
            f.write(post_id + '\n')

def checkUploadId(post_id):
    with open('uploaded_ids.txt', 'r') as f:
        if post_id in f.read():
            return True
    return False

def addUploadId(post_id):
    try:
        with open('uploaded_ids.txt', 'a') as f:
            f.write(post_id + '\n')
    except FileNotFoundError:
        with open('uploaded_ids.txt', 'w') as f:
            f.write(post_id + '\n')

def check_files_exist(post_id):
    filenames = [
        os.path.join("posts", f"{post_id}.txt"),
        os.path.join("srt", f"{post_id}.srt"),
        os.path.join("results", f'subtitled{post_id}.mp4'),
        os.path.join("mp3", f"{post_id}.mp3"),
    ]
    
    for filename in filenames:
        if not os.path.exists(filename):
            print(f"{post_id} - File {filename} does not exist.")
            return False

    print(f"All required files for post ID {post_id} exist.")
    return True

# Iterate through each post and create TTS audio and text files
for post in posts:
    start_time = time.time()

    title = post.title
    body = post.selftext
    author = post.author
    post_id = post.id
    post_url = post.url

    input_text = f"{title} {body}"
    
    if checkUploadId(post_id):
        print("Post ID", post_id, "has already been processed and uploaded.")
        continue  # Skip to next post

    if checkPostId(post_id):
        print("Post ID", post_id, "has already been processed.")

    file = 'results/' + 'subtitled' + f'{post_id}.mp4'

    if not check_files_exist(post_id):
        print(f"{post_id} - Post link:", post_url)

        createPostTextFile(title, body, author, post_id,input_text)
        preprocessText(post_id)
        wcreateTTS(post_id,input_text)
        createVideo(post_id)
        createsrt("mp4",post_id)
        add_subtitles(post_id)
        print(f"{post_id} - Post created successfully")
        print("******Post Completed Successfully*****")
        addPostId(post_id) 

    schedule_time  = schedule_time + 600
    uploadVideo(SESSION_ID, file, TITLE, TAGS, USERS, url_prefix, schedule_time)
    addUploadId(post_id)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken for post ID {post_id}: {elapsed_time} seconds")
