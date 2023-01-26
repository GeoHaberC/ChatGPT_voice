#pip install SpeechRecognition openai gtts playsound

from gtts import gTTS
import speech_recognition as sr
import openai
from pydub import AudioSegment
from pydub.playback import play

def voice_interface():
    # Initialize the speech recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    ## XXX:  Set the OpenAI API key
    openai.api_key = "YOUR_API_KEY"
    openai.api_key = "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"

    while True:
        try:
            ## XXX:  Prompt the user for voice input
            print("Please speak a command:")
            with microphone as source:
                audio = recognizer.listen(source)

            ## XXX:  Convert the audio to text
            command = recognizer.recognize_google(audio, language="en-US")
            print("Command: ", command)

            if command == "Ok goodbye":
                print("Goodbye!")
                break

            ## XXX:  Generate the response from ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt='You said: '+ command,
                max_tokens=2048,
                n = 1,
                stop=None,
                temperature=0.5
            )

            response = response.choices[0].text
            print("Response: ", response)
            text_to_speech ( response )

        except sr.UnknownValueError:
            print("Sorry, I did not understand what you said.")
        except sr.RequestError as e:
            print("Error while requesting results; {0}".format(e))
        except Exception as e:
            print("Error: {0}".format(e))
#function to convert the text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    audio = AudioSegment.from_file("response.mp3")
    play(audio)
    # Play the audio file
#    playsound("response.mp3")

if __name__ == '__main__':
    voice_interface()
