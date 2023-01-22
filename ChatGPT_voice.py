#pip install SpeechRecognition openai gtts playsound

from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import openai
import gtts
from playsound import playsound

# Use the API key
#openai.api_key = "YOUR_API_KEY"

# initialize the recognizer
r = sr.Recognizer()

# read the audio file
with sr.Microphone() as source:
    print("Speak: ")
    audio = r.listen(source)

# recognize the speech
text = r.recognize_google(audio)

# Send a request to the API
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=text,
    max_tokens=2048
)

# Use gTTS to convert text to speech
tts = gtts.gTTS(response["choices"][0]["text"])

# Save the speech to a file
tts.save("response.mp3")

audio = AudioSegment.from_file("response.mp3")
play(audio)
# Play the audio file
playsound("response.mp3")
