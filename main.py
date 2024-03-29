from styles import *
from models.mbart import mbart_translator
from models.helsinki import helsinki_translator
from models.google import googletrans_translator
from models.nllb import nllb_translator

import tkinter as tk
from tkinter import scrolledtext, ttk
from transformers import pipeline
from gtts import gTTS
import os

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

selected_translator = 0
selected_funcionality = 0
icon_path = "icon/szop.ico"


def send_message():
    user_input = user_input_box.get()
    if user_input:
        user_input = user_input.replace("\n", "")
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"{YOUR_NAME}: " + user_input + "\n", YOUR_NAME)
        chat_history.config(state=tk.DISABLED)

        if selected_translator == 0:
            response_str = googletrans_translator(user_input)

        elif selected_translator == 1:
            response_str = mbart_translator(user_input)

        elif selected_translator == 2:
            response_str = helsinki_translator(user_input)

        elif selected_translator == 3:
            response_str = nllb_translator(f"{user_input}")

        else:
            response_str = "Nieudało się znaleźć modelu"

        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"{CHAT_NAME}: " + response_str + "\n", CHAT_NAME)

        if selected_funcionality == 1:
            output = gTTS(text=response_str, lang="en", slow=False)
            output.save("output.mp3")

            chat_history.insert(tk.END, f"Audio: ", CHAT_NAME)
            chat_history.insert(tk.END, "Play" + "\n", "play_audio")
            chat_history.tag_config("play_audio", foreground=CHAT_TEXT_COLOR, underline=1)
            chat_history.tag_bind("play_audio", "<Button-1>", play_audio)
            chat_history.insert(tk.END, "\n")

        if selected_funcionality == 2:
            sentences = [response_str]
            simulated_response = classifier(sentences)
            chat_history.insert(tk.END, f"Emotions: ", CHAT_NAME)

            for emotion in (simulated_response[0]):
                if emotion['score'] > 0.1:
                    chat_history.insert(tk.END, f"{emotion['label']}, ", CHAT_NAME)

            chat_history.insert(tk.END, "\n\n", CHAT_NAME)

        if selected_funcionality == 3:
            sumup = summarizer(response_str, max_length=10000, min_length=1, do_sample=False)
            chat_history.insert(tk.END, f"Summary: {sumup[0]['summary_text']} \n\n", CHAT_NAME)

        chat_history.config(state=tk.DISABLED)

        user_input_box.delete(0, tk.END)
        user_input_box.focus_set()


def reset_chat():
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    chat_history.config(state=tk.DISABLED)


def select_functions(model_number):
    global selected_funcionality
    selected_funcionality = model_number

    first_button.config(bg=SIDEBAR_BUTTON_COLOR)
    second_button.config(bg=SIDEBAR_BUTTON_COLOR)
    third_button.config(bg=SIDEBAR_BUTTON_COLOR)

    if model_number == 1:
        first_button.config(bg=CHOOSEN_BUTTON_COLOR)
    elif model_number == 2:
        second_button.config(bg=CHOOSEN_BUTTON_COLOR)
    elif model_number == 3:
        third_button.config(bg=CHOOSEN_BUTTON_COLOR)


def select_translator(another_model_number):
    global selected_translator
    selected_translator = another_model_number

    fourth_button.config(bg=SIDEBAR_BUTTON_COLOR)
    fifth_button.config(bg=SIDEBAR_BUTTON_COLOR)
    sixth_button.config(bg=SIDEBAR_BUTTON_COLOR)
    seventh_button.config(bg=SIDEBAR_BUTTON_COLOR)

    if selected_translator == 1:
        fifth_button.config(bg=CHOOSEN_BUTTON_COLOR)
    elif selected_translator == 2:
        sixth_button.config(bg=CHOOSEN_BUTTON_COLOR)
    elif selected_translator == 3:
        seventh_button.config(bg=CHOOSEN_BUTTON_COLOR)
    else:
        fourth_button.config(bg=CHOOSEN_BUTTON_COLOR)


def play_audio(event=None):
    os.system("start output.mp3")  # Dla systemów Windows


app = tk.Tk()
app.title(APP_TITLE)
app.configure(bg=BG_COLOR)
app.iconbitmap(default=icon_path)

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Główny kontener
app_width = 900
app_height = 800 - 90

x_position = (screen_width - app_width) // 2
y_position = (screen_height - app_height) // 2

app.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")

main_frame = tk.Frame(app, bg=BG_COLOR)
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Panel boczny
sidebar = tk.Frame(app, width=200, bg=SIDEBAR_COLOR)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Przyciski wybierające funkcje
first_button = tk.Button(sidebar, text="Text to Speech", command=lambda: select_functions(1), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
first_button.pack(pady=10, padx=10, fill=tk.X)

second_button = tk.Button(sidebar, text="Emotions", command=lambda: select_functions(2), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
second_button.pack(pady=10, padx=10, fill=tk.X)

third_button = tk.Button(sidebar, text="Summary", command=lambda: select_functions(3), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
third_button.pack(pady=10, padx=10, fill=tk.X)

# Separator
separator = ttk.Separator(sidebar, orient='horizontal')
separator.pack(pady=5, padx=10, fill=tk.X)

# Przyciski wybierające model
fourth_button = tk.Button(sidebar, text="Model Def", command=lambda: select_translator(0), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
fourth_button.pack(pady=10, padx=10, fill=tk.X)

fifth_button = tk.Button(sidebar, text="Model 2", command=lambda: select_translator(1), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
fifth_button.pack(pady=10, padx=10, fill=tk.X)

sixth_button = tk.Button(sidebar, text="Model 3", command=lambda: select_translator(2), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
sixth_button.pack(pady=10, padx=10, fill=tk.X)

seventh_button = tk.Button(sidebar, text="Model 4", command=lambda: select_translator(3), bg=SIDEBAR_BUTTON_COLOR, font=FONT, fg=TEXT_COLOR)
seventh_button.pack(pady=10, padx=10, fill=tk.X)

# Treść czatu
chat_frame = tk.Frame(main_frame, bg=BG_COLOR)
chat_frame.pack(expand=True, fill=tk.BOTH)

chat_history = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
chat_history.pack(expand=True, fill=tk.BOTH)
chat_history.tag_config(YOUR_NAME, foreground=YOUR_TEXT_COLOR, font=DIALOGUE_FONT)
chat_history.tag_config(CHAT_NAME, foreground=CHAT_TEXT_COLOR, font=DIALOGUE_FONT)

# Pole wprowadzania
input_frame = tk.Frame(main_frame, bg=BG_COLOR)
input_frame.pack(fill=tk.X)

user_input_box = tk.Entry(input_frame, bg=BG_COLOR, fg=TEXT_COLOR, font=USER_INPUT_FONT)
user_input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
user_input_box.focus_set()

send_button = tk.Button(input_frame, text="Send", command=send_message, bg=BG_COLOR, font=DIALOGUE_FONT, fg=TEXT_COLOR)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)
app.bind('<Return>', lambda event=None: send_button.invoke())

app.mainloop()
