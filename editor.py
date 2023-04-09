from moviepy.editor import *

# Set the paths for the input audio file, captions file, and output video file
audio_path = "input.mp3"
captions_path = "input.txt"
video_path = "output.mp4"

# Load the audio file and generate a VideoFileClip
audio_clip = AudioFileClip(audio_path)
video_clip = audio_clip.to_videofile(video_path, fps=25, audio=False)

# Load the captions from the file and format them for SubtitlesClip
captions = []
with open(captions_path, "r") as f:
    for line in f:
        start, end, text = line.split("\t")
        start = float(start)
        end = float(end)
        captions.append((start, end, text.strip()))

# Generate a SubtitlesClip with the captions and add it to the video clip
subtitles = SubtitlesClip(captions, fontsize=24)
subtitles = subtitles.set_pos(('center', 'bottom'))
final_clip = CompositeVideoClip([video_clip, subtitles])

# Write the final video clip to file
final_clip.write_videofile(video_path, audio_codec="aac")
