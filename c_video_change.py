# moviepy 모듈 설치
# pip install moviepy

# 모듈 로딩 후 오디오 추출
import moviepy.editor as mp

clip = mp.VideoFileClip("video/video_eng00.mp4")
clip.audio.write_audiofile("video/video_eng00.mp3")
