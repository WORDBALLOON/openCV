<<<<<<< HEAD
import moviepy.editor as mp
import sys

title = sys.argv[1]
mp4_title = title+".mp4"
mp3_title = title+".mp3"

clip = mp.VideoFileClip("./upload/"+mp4_title)
clip.audio.write_audiofile("./upload/"+mp3_title)
=======
import moviepy.editor as mp
import sys

title = sys.argv[1]
mp4_title = title+".mp4"
mp3_title = title+".mp3"

clip = mp.VideoFileClip("./upload/"+mp4_title)
clip.audio.write_audiofile("./upload/"+mp3_title)
>>>>>>> 7a3a5464af2e2b8583c66c8deec25528fdf6e532
