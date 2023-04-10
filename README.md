# Reddit Text-to-Speech Bot

This script uses the Reddit API and a third-party text-to-speech service to create audio files from the top posts of a specified subreddit.

## Requirements

- Python 3.x
- PRAW (Python Reddit API Wrapper)
- requests

## Setup

1. Clone the repository or download the files.
2. Install the required packages using pip: `pip install -r requirements.txt`
3. Create a Reddit app and obtain API credentials. See [these instructions](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) for more information.
4. Set the `client_id`, `client_secret`, `password`, `user_agent`, and `username` variables in the `main.py` file to your own API credentials.
5. Set the `subreddit_name` variable to the name of the subreddit you want to search.
6. (Optional) Adjust the `time_filter` and `limit` parameters in the `posts` variable to change the search criteria.
7. Run the script using `python main.py`

## Usage

1. The script will search the specified subreddit for top posts based on the `time_filter` and `limit` parameters.
2. For each post, the script will create a text file and a corresponding audio file using the post's title, body, and author information.
3. The audio files will be saved in the `posts` directory.

## Code Description

The script uses the PRAW package to interact with the Reddit API and the requests package to make HTTP requests to a third-party text-to-speech service. The script defines two functions:

### `createPostTextFile`

This function creates a text file with post information for text-to-speech processing. It takes the following parameters:

- `title`: The title of the post.
- `body`: The body of the post.
- `author`: The name of the post's author.
- `post_id`: The unique ID of the post.
- `input_text`: The text to be used for text-to-speech processing.

### `createTTS`

This function generates a text-to-speech audio file using a third-party service. It takes the following parameters:

- `title`: The title of the post.
- `body`: The body of the post.
- `author`: The name of the post's author.
- `post_id`: The unique ID of the post.
- `input_text`: The text to be used for text-to-speech processing.

The function sends an HTTP request to the text-to-speech service with the input text and speaker ID. The response is then decoded and written to an audio file.

## Acknowledgments

- [PRAW documentation](https://praw.readthedocs.io/en/stable/)
- [Requests documentation](https://docs.python-requests.org/en/master/)
- [How to Generate Speech from Text with Python](https://www.twilio.com/blog/generate-speech-from-text-with-python)
