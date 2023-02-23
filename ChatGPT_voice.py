import os
import sys
import time
import openai
import pyaudio
import logging
import speech_recognition as sr

from gtts			import gTTS
from functools		import wraps
from pydub			import AudioSegment
from pydub.playback import play

how_can_I_help = 'How can I help'

def handle_exception(func):
	"""Decorator to handle exceptions."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			logging.error("Error: %s", e, exc_info=True)
			sys.exit(1)
	return wrapper

@handle_exception
def check_audio_devices():
	"""Check if the audio input and output devices are properly configured."""
	p = pyaudio.PyAudio()
	input_device  = p.get_default_input_device_info()
	output_device = p.get_default_output_device_info()

	if input_device is None:
		logging.error("No audio input device found.")
		sys.exit(1)

	if output_device is None:
		logging.error("No audio output device found.")
		sys.exit(1)

	logging.info("Audio input device: %s", input_device['name'])
	logging.info("Audio output device: %s", output_device['name'])

@handle_exception
def voice_ChatGPT():
	"""The main function for the voice interface."""

	log_file = f"_{sys._getframe().f_code.co_name}_{time.strftime('%Y%m%d-%H%M%S')}.log"

	logging.basicConfig(filename=log_file,
						level=logging.DEBUG,
						format='%(asctime)s %(levelname)s %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S')

	# Set logging level to only display INFO messages inside the loop
	logging.getLogger().setLevel(logging.INFO)

	check_audio_devices()

	# Initialize the speech recognizer and microphone
	recognizer = sr.Recognizer()
	microphone = sr.Microphone()
	openai.api_key = os.getenv("OPENAI_API_KEY")
	if openai.api_key is None:
		logging.error("API key not found.")
		return

	while True:
		try:
			# Prompt the user for voice input
			text_to_speech (how_can_I_help)
			logging.info   (how_can_I_help)
			with microphone as source:
				audio = recognizer.listen(source)
			# Convert the audio to text
			command = recognizer.recognize_google(audio, language="en-US")
			logging.info("Command: %s", command)

			if command.lower() in ["goodbye", "exit", "end program" ]:
				text_to_speech ("Are you sure? to exit say yes")
				with microphone as source:
					audio = recognizer.listen(source)
				if recognizer.recognize_google(audio, language="en-US").lower() == 'yes' :
					logging.info("Goodbye!")
					break

			# Generate the response from OpenAI
			response = openai.Completion.create(
				engine="text-davinci-002",
				prompt='You said: ' + command,
				max_tokens=2048,
				n=1,
				stop=None,
				temperature=0.5
			)

			response = response.choices[0].text
			logging.info("Response: %s", response)
			text_to_speech(response)

		except sr.UnknownValueError:
			logging.error("Sorry, I did not understand what you said.")
		except sr.RequestError as e:
			logging.error("Error while requesting results: %s", e)
		finally :
			# Set logging level back to original level outside the loop
			logging.getLogger().setLevel(logging.DEBUG)

	return log_file

@handle_exception
def text_to_speech(text):
	"""Convert the text to speech."""
	tts = gTTS(text=text, lang='en')
	tts.save("tmp.mp3")

	audio = AudioSegment.from_file("tmp.mp3")
	play(audio)


if __name__ == '__main__':
	log_file = voice_ChatGPT()

	if os.path.exists(log_file) :
		os.remove(log_file)
		pass
	else:
		print(f"{log_file} file does not exist")
