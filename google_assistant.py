# -*- coding: utf-8 -*-
"""Google Assistant with Speech Recognition and Text-to-Speech.ipynb

This code provides a basic Google Assistant like experience by combining
speech recognition, OpenAI's ChatGPT for natural language processing, and text-to-speech. 
"""

import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from gtts import gTTS
from IPython.display import Audio
from google.colab import userdata
import wave 

# Set up OpenAI API key (replace with your actual API key)
client = OpenAI(
  api_key=userdata.get('api_key')
)

# Function to convert text to speech
def speakNow(text):
  tts = gTTS(text, lang='en')  # Provide the string to convert to speech
  tts.save('output.wav')  # save the string converted to speech as a .wav file
  sound_file = 'output.wav'
  Audio(sound_file, autoplay=True)

# Function to get user input using speech recognition
def getVoiceInput():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Speak now...")
    audio = r.listen(source)
  
  try:
    text = r.recognize_google(audio)
    print("You said: " + text)
    return text
  except sr.UnknownValueError:
    print("Could not understand audio")
  except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
  return None

# Function to ask ChatGPT
def askGPT(user_text):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a friendly and helpful chatbot."},
      {"role": "user", "content": user_text}
    ]
  )
  response_from_chatGPT = completion.choices[0].message.content
  return response_from_chatGPT

# Function to process audio bytes
def bytes_to_audio_simple(byte_data, output_file):
    with wave.open(output_file, 'wb') as wave_file:
        wave_file.setnchannels(1)  # Mono audio
        wave_file.setsampwidth(2)  # 2 bytes per sample
        wave_file.setframerate(44100)  # Standard audio sample rate

        wave_file.writeframes(byte_data)

# Main loop
while True:
    user_input = getVoiceInput()
    if user_input is not None:
        response = askGPT(user_input)
        speakNow(response)
    
    # Ask if the user wants to continue
    should_continue = input("Want to ask another question? (y/n): ").lower()
    if should_continue != 'y':
        break
