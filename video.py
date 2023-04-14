from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Load the pre-transcribed text
with open('input.txt', 'r') as file:
    text = file.read()

# Load the video file
video_file = VideoFileClip('input.mp4', duration=180)


# Add the captions to the video
txt_clip = TextClip(text, fontsize=70, color='white', bg_color='black').set_position('bottom')
video_with_caption = CompositeVideoClip([video_file, txt_clip])

# Export the final video as an MP4 file
video_with_caption.write_videofile('output.mp4')
