import os
import moviepy
import random
from googledrive import upload_to_drive
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def createVideo(post_id):
    mp3_file = os.path.join("mp3", f"{post_id}.mp3")
    video_files = [file for file in os.listdir("videos") if file.endswith(".mp4")]
    random.shuffle(video_files)
    output_file = f"{post_id}.mp4"

    if os.path.exists(os.path.join("mp4", output_file)):
        print(f"{post_id} - Skipping MP4 creation for {post_id}. File already exists.")
        return None
    
    audio_clip = AudioFileClip(mp3_file)
    
    video_clips = []
    total_video_duration = 0
    
    for mp4_file in video_files:
        video_clip = VideoFileClip(os.path.join("videos", mp4_file))
        video_clips.append(video_clip)
        total_video_duration += video_clip.duration
        
        if total_video_duration >= audio_clip.duration:
            break
    
    if total_video_duration < audio_clip.duration:
        print("Not enough video found for the given audio duration.")
        return
    
    final_video = concatenate_videoclips(video_clips)
    final_video = final_video.set_duration(audio_clip.duration)
    
    final_clip = final_video.set_audio(audio_clip)
    final_clip.write_videofile(os.path.join("mp4", f"{post_id}.mp4"),verbose = True, fps=24,codec = 'libx264',bitrate='5000k',threads=2)
    #upload_to_drive(output_file)
    return

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
            final_clip.write_videofile(os.path.join("mov", f"{post_id}.mov"),verbose = True, fps=24, codec='png', bitrate='5000k')
            return

    print("No video found for the given audio duration.")