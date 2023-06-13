import praw
import os
import random
import time
from uploader import uploadVideo
from texttospeech import createTTS, wcreateTTS
from subtitles import createsrt, format_time, get_screen_size, subtitle_generator, add_subtitles
from videocreation import createVideo, createVideoMov
from textprocess import createPostTextFile, preprocessText

#choices for randomlym selected captions
TITLES = ["thoughts?", "opinions?", "what do you think?", "let's discuss"]
#randomizes the choices
TITLE = random.choice(TITLES)
#list of hashtags for the post
TAGS = ["aita", "askreddit", "redditstories","tifu","redditreadings"]
#randomizes the order of the hashtags to seem more human
random.shuffle(TAGS)
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

if not os.path.exists('post_ids.txt'):
    with open('post_ids.txt', 'w') as file:
        # Optionally, you can write an initial content to the file here
        pass
    print("'post_ids.txt' does not exist, creating.")
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

def checkPostId(post_id):
    """
    Checks if a given post ID has already been logged in the text file.

    Returns:
        True if the post ID is already logged, False otherwise.
    """
    with open('post_ids.txt', 'r') as f:
        for line in f:
            if post_id in line:
                return True
    return False


def addPostId(post_id):
    """
    Adds a post ID to the text file to mark it as processed.
    If the file doesn't exist, it will be created.
    """
    try:
        with open('post_ids.txt', 'a') as f:
            f.write(post_id + '\n')
    except FileNotFoundError:
        with open('post_ids.txt', 'w') as f:
            f.write(post_id + '\n')

# Iterate through each post and create TTS audio and text files
for post in posts:
    #tracks runtime for iterations
    start_time = time.time()

    title = post.title
    body = post.selftext
    author = post.author
    post_id = post.id
    post_url = post.url


    # Define input text for TTS
    input_text = f"{title} {body}"
    
    # Check if post_id already exists
    if not checkPostId(post_id):
        file = 'results/' + 'subtitled' + f'{post_id}.mp4'
        # Call function to create text file for the post
            # Print the post link
        print(f"{post_id} - Post link:", post_url)
        createPostTextFile(title, body, author, post_id,input_text)

        preprocessText(post_id)
        wcreateTTS(post_id,input_text)
        createVideo(post_id)
        createsrt("mp4",post_id) # can swap to createsrt("mp4",post_id), both are equally as efficient, but if use mp3 you can create srt first.
        #createVideoMov(post_id)
        add_subtitles(post_id)
        print(f"{post_id} - Post created successfully")
        print("******Post Completed Successfully*****")
        # need to wait for tiktok uploading to be fixed.
        #uploadVideo(SESSION_ID, file, TITLE, TAGS, USERS,url_prefix = "us")
        addPostId(post_id)
        # record the end time
        #end_time = time.time()
        # calculate the elapsed time and print it
        #elapsed_time = end_time - start_time
        #print(f"Elapsed time: {elapsed_time:.2f} seconds")
        #print("----------------------------Post created successfully----------------------------")
        # wait for a random interval of 1-3 minutes to seem more human
        #interval = random.randint(300, 600)
        #print(f"Waiting {interval} seconds...")
        #time.sleep(interval)
    else:
        print("Post ID", post_id, "has already been processed.")