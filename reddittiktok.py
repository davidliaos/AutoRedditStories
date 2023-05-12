import praw
import os
from texttospeech import createTTS, wcreateTTS
from subtitles import createsrt, format_time, get_screen_size, subtitle_generator, add_subtitles
from videocreation import createVideo, createVideoMov
from textprocess import createPostTextFile, preprocessText

if not os.path.exists("srt"):
    os.makedirs("srt")
    print("srt does not exist, creating.")
if not os.path.exists("posts"):
    os.makedirs("posts")
    print("post does not exist, creating.")

if not os.path.exists("mp3"):
    os.makedirs("mp3")
    print("mp3 does not exist, creating.")

if not os.path.exists("mp4"):
    os.makedirs("mp4")
    print("mp4 does not exist, creating.")

if not os.path.exists("wav"):
    os.makedirs("wav")
    print("wav does not exist, creating.")

if not os.path.exists("results"):
    os.makedirs("results")
# Allows user to just straight up delete the folders when done without the hassle of deleting each file.
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
posts = reddit.subreddit(subreddit_name).top(time_filter="day", limit=5)

# Define functions

def checkPostId(post_id):
    with open('post_ids.txt', 'r') as f:
        if post_id in f.read():
            return True
    return False

def addPostId(post_id):
    with open('post_ids.txt', 'a') as f:
        f.write(post_id + '\n')


# Iterate through each post and create TTS audio and text files
for post in posts:
    title = post.title
    body = post.selftext
    author = post.author
    post_id = post.id
    post_url = post.url


    # Define input text for TTS
    input_text = f"{title} by {author}  {body}"
    
    # Check if post_id already exists
    if not checkPostId(post_id):
        # Call function to create text file for the post
            # Print the post link
        print("Post link:", post_url)
        createPostTextFile(title, body, author, post_id,input_text)
        preprocessText(post_id)
        wcreateTTS(post_id,input_text)
        createVideo(post_id,input_text)
        #createVideoMov(post_id)
        createsrt("mp4",post_id)
        add_subtitles(post_id)
        addPostId(post_id)
        print("----------------------------Post created successfully----------------------------")