import re
from google.cloud import speech
from os.path import split
import io
import os

#GOOGLE_APPLICATION_CREDENTIALS = "wordballoon0-0c992ebc3d08.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "wordballoon0-0c992ebc3d08.json"


path = 'video/video_eng2.mp3'

s = os.path.splitext(path)
s = os.path.split(s[0])
f_name = "output_(" + str(s[1]) + ").txt"
print("*********" + f_name)

client = speech.SpeechClient()

with io.open(path, 'rb') as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)
config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    sample_rate_hertz=8000,
    language_code='en-US',
    # Enable automatic punctuation
    enable_automatic_punctuation=True)

response = client.recognize(config, audio)
tmp = []

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print('-' * 20)
    print('First alternative of result {}'.format(i))
    print('Transcript: {}'.format(alternative.transcript))
    output = re.split('([.,?!])', alternative.transcript)
    del output[-1]
    tmp.append(output)

answer = sum(tmp, [])

final = []
for i in range(len(answer)):
    if i % 2 == 1:
        text1 = answer[i-1]+answer[i]
        final.append(text1)


s = os.path.splitext(path)
s = os.path.split(s[0])
f_name = "output_(" + str(s[1]) + ").txt"
f = open(f_name, 'a')

for i in final:
    print("**"+i)
    f.write(i+"\n")
# f.writelines(output)
f.close()
