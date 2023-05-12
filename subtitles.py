import os
import moviepy
from subsai import SubsAI
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def createsrt(path, name):
    if os.path.exists(os.path.join("srt", f"{name}.mp4")):
        print(f"Skipping SRT creation for {name}. File already exists.")
        return None
    file = f'./{path}/{name}.mp4'
    subs_ai = SubsAI() 
    model = subs_ai.create_model('ggerganov/whisper.cpp', {'model_type': 'small', 'token_timestamps': True, 'max_len': 50})
    subs = subs_ai.transcribe(file, model)
    srt_folder = './srt'
    srt_path = os.path.join(srt_folder, f'{name}.srt')
    subs.save(srt_path)

def format_time(seconds):
    h, m, s = 0, 0, 0
    ms = int(seconds * 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(int(h), int(m), int(s), int(ms))

def get_screen_size():
    return (1920, 1080)  # Replace with the actual screen size

def subtitle_generator(txt):
    # Define the font, size, and color of the subtitle
    font = 'Proxima Nova Bold'
    size = 45
    color = 'white'
    stroke_width = 1
    stroke_color = 'black'

    # Split the text into words
    words = txt.split()

    # Initialize the resulting text
    result = ''

    # Set the maximum number of characters per line
    max_chars_per_line = 40

    # Add words one by one until the resulting text exceeds the max chars per line
    line_length = 0
    for word in words:
        word_length = len(word)
        if line_length + word_length + 1 <= max_chars_per_line:
            # If adding the word would not exceed the max chars per line, add it to the current line
            if result:
                result += ' '
            result += word
            line_length += word_length + 1
        else:
            # If adding the word would exceed the max chars per line, start a new line
            result += '\n'
            line_length = word_length
            result += word

    # Create and return the TextClip
    return TextClip(result, fontsize=size, font=font, color=color, stroke_width=stroke_width, stroke_color=stroke_color)

def add_subtitles(post_id):
    #mp4_file_path = f"mov/{post_id}.mov"
    mp4_file_path = f"mp4/{post_id}.mp4"
    srt_file_path = f"srt/{post_id}.srt"
    output_file = f"{post_id}.mp4"
    # Load the video file
    video_clip = VideoFileClip(mp4_file_path)

    # Load the subtitle file
    subtitles = SubtitlesClip(srt_file_path, subtitle_generator)

    # Set the subtitles position and duration
    subtitles = subtitles.set_position(("center", "center")).set_duration(video_clip.duration)

    # Combine the video clip and subtitles clip
    final_clip = CompositeVideoClip([video_clip, subtitles])

    # Save the final clip
    if not os.path.exists("results"):
        os.makedirs("results")
    
    final_clip.write_videofile(f"results/subtitled{post_id}.mp4")
    #upload_to_drive(output_file,"1JDtzqDe--FNVBFMM2D8D7JH2k3nWiQGY")
