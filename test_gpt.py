import tkinter as tk
from tkinter import scrolledtext, filedialog
import openai
import speech_recognition as sr
import pyttsx3
import os

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def chatbot_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Error: Unable to connect to OpenAI API."

def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        chat_box.insert(tk.END, "You: " + user_input + "\n")
        bot_response = chatbot_response(user_input)
        chat_box.insert(tk.END, "Bot: " + bot_response + "\n\n")
        speak(bot_response)
        user_entry.delete(0, tk.END)

def clear_chat():
    chat_box.delete(1.0, tk.END)

def save_chat():
    chat_history = chat_box.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(chat_history)

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_box.insert(tk.END, "Listening...\n")
        try:
            audio = recognizer.listen(source)
            user_text = recognizer.recognize_google(audio)
            user_entry.delete(0, tk.END)
            user_entry.insert(0, user_text)
            send_message()
        except sr.UnknownValueError:
            chat_box.insert(tk.END, "Could not understand audio\n")
        except sr.RequestError:
            chat_box.insert(tk.END, "Error connecting to speech recognition service\n")

def speak(text):
    engine.say(text)
    engine.runAndWait()

# GUI Setup
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("500x600")

# Chat Display
chat_box = scrolledtext.ScrolledText(root, width=60, height=20)
chat_box.pack(pady=10)
chat_box.config(state=tk.NORMAL)

# User Input
user_entry = tk.Entry(root, width=50)
user_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()

send_button = tk.Button(button_frame, text="Send", command=send_message)
send_button.grid(row=0, column=0, padx=5)

voice_button = tk.Button(button_frame, text="🎤 Voice Input", command=voice_input)
voice_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(button_frame, text="Clear Chat", command=clear_chat)
clear_button.grid(row=0, column=2, padx=5)

save_button = tk.Button(button_frame, text="Save Chat", command=save_chat)
save_button.grid(row=0, column=3, padx=5)

root.mainloop()
