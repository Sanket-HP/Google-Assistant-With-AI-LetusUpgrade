import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import openai

# Initialize OpenAI API client
openai.api_key = 'sk-proj-xzsdFyYDLc6Lo7S4pfgLT3BlbkFJ8b89jhqUVXQaTb5Mim6F'

# Function to convert text to speech using pyttsx3
def speakNow(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to get user input using speech recognition
def getVoiceInput():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# Function to ask ChatGPT
def askGPT(user_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly and helpful chatbot."},
            {"role": "user", "content": user_text}
        ]
    )
    response_from_chatGPT = response.choices[0].message['content']
    return response_from_chatGPT

# GUI Application
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")

        self.label = tk.Label(root, text="Press the button and speak", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.speak_button = tk.Button(root, text="Speak", command=self.process_speech, font=("Helvetica", 14))
        self.speak_button.pack(pady=20)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Helvetica", 14))
        self.quit_button.pack(pady=20)

    def process_speech(self):
        user_input = getVoiceInput()
        if user_input:
            response = askGPT(user_input)
            speakNow(response)
            messagebox.showinfo("Assistant Response", response)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
