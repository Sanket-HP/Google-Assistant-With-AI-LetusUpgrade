from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

app = Flask(__name__)

# Set up OpenAI API key
client = OpenAI(api_key='sk-proj-aI2xnzhdFad3CUyFzLcRT3BlbkFJvXBMGstu5NKThVQKs9c0')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.get_json()['userInput']
    response = askGPT(user_input)
    return
