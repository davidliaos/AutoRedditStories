import praw
import os
from uploader import uploadVideo
from texttospeech import createTTS, wcreateTTS
from subtitles import createsrt, format_time, get_screen_size, subtitle_generator, add_subtitles
from videocreation import createVideo, createVideoMov
from textprocess import createPostTextFile, preprocessText



SESSION_ID = "98c156e53abe8c7c5452afc89a05ca18"
TITLE = "thoughts?"
TAGS = ["aita", "askreddit", "redditstories","tifu","redditreadings"]
USERS = []


if not os.path.exists("srt"):
    os.makedirs("srt")
    print("srt directory does not exist, creating.")
if not os.path.exists("posts"):
    os.makedirs("posts")
    print("post directory does not exist, creating.")

if not os.path.exists("mp3"):
    os.makedirs("mp3")
    print("mp3 directory does not exist, creating.")

if not os.path.exists("mp4"):
    os.makedirs("mp4")
    print("mp4 directory does not exist, creating.")

if not os.path.exists("wav"):
    os.makedirs("wav")
    print("wav directory does not exist, creating.")

if not os.path.exists("results"):
    os.makedirs("results")
    print("results directory does not exist, creating.")
# Allows user to just straight up delete the folders when done without the hassle of deleting each file.
# Set up Reddit API credentials

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
        file = 'results/' + 'subtitled' + f'{post_id}.mp4'
        # Call function to create text file for the post
            # Print the post link
        print("Post link:", post_url)
        createPostTextFile(title, body, author, post_id,input_text)

        preprocessText(post_id)
        wcreateTTS(post_id,input_text)
        createVideo(post_id)
        #createVideoMov(post_id)
        createsrt("mp4",post_id)
        add_subtitles(post_id)
        uploadVideo(SESSION_ID, file, TITLE, TAGS, USERS)
        addPostId(post_id)
        print("----------------------------Post created successfully----------------------------")