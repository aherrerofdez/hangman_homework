import random as r
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

filename = "words.txt"


def get_words(file):
    words_list = []
    with open(file) as f:
        for line in f:
            line = line.split()
            for word in line:
                word.strip()
                words_list.append(word)

    random_word = words_list[r.randint(0, len(words_list) - 1)]

    return random_word.upper()


class GUI(object):
    def __init__(self, window, word, stage=0, game_over=False):
        self.window = window
        self.word = word
        self.stage = stage
        self.game_over = game_over
        bg_color = "#7AA52B"

        # Adding window's properties
        self.window.title("Hangman Game")
        self.window.geometry("900x600")
        self.window.resizable(0, 0)

        # Creating the main frame
        self.frame = tk.Frame(master=window, bg=bg_color)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # Create Secret Word Label
        self.sec_word = "_ "*len(self.word)
        self.sec_word.rstrip()
        self.secret_lb = tk.Label(self.frame, text=self.sec_word, bg="#7AA52B", fg="black")
        self.secret_lb.config(font=("Arial", 30), width=18)
        self.secret_lb.grid(row=1, column=1, columnspan=7)

        # Create Letter Buttons
        self.alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                         "T", "U", "V", "W", "X", "Y", "Z"]
        self.letter_buttons = []
        for i in range(len(self.alphabet)):
            self.btn = tk.Button(self.frame, text=self.alphabet[i], command=self.check_letter, bg="#00338D", fg="white")
            self.btn.config(font=("Arial", 20), width=3,
                            command=lambda text=self.alphabet[i], btn=self.btn: self.check_letter(text, btn))
            self.letter_buttons.append(self.btn)
            if i < 7:
                self.btn.grid(row=2, column=i + 1, padx=2, pady=30)
            elif 7 <= i < 14:
                self.btn.grid(row=3, column=i - 6, padx=2)
            elif 14 <= i < 21:
                self.btn.grid(row=4, column=i - 13, padx=2, pady=30)
            else:
                self.btn.grid(row=5, column=i - 19, padx=2)

        # Creating Hint Button
        self.hint_btn = tk.Button(self.frame, text="Hint", command=self.get_hint, bg="#00338d", fg="white")
        self.hint_btn.config(font=("Arial", 16), width=20)
        self.hint_btn.grid(row=0, column=0, padx=100, pady=40)

        # Create Drawing Canvas
        self.canvas = tk.Canvas(master=self.frame, width=275, height=350, bg="#0097dc", highlightthickness=5)
        self.canvas.grid(row=2, column=0, rowspan=5)

    def get_hint(self):
        temp_word = list(self.secret_lb["text"].replace(" ", ""))
        secret_word_chars = list(self.word)
        index = 26
        while True:
            rand_letter = secret_word_chars[r.randint(0, len(secret_word_chars) - 1)]
            if rand_letter in temp_word:
                continue
            for i in range(0, len(secret_word_chars)):
                if secret_word_chars[i] == rand_letter:
                    temp_word[i] = rand_letter
                    index = self.alphabet.index(rand_letter)
            break
        temp_word = " ".join(temp_word)
        self.secret_lb["text"] = temp_word
        self.letter_buttons[index].config(state="disabled", bg="#e6e6e6")
        self.check_game_ended()

    def check_letter(self, char, btn):
        btn.config(state="disabled", bg="#e6e6e6")
        temp_word = list(self.secret_lb["text"].replace(" ", ""))
        secret_word_chars = list(self.word)
        for i in range(0, len(secret_word_chars)):
            if secret_word_chars[i] == char:
                temp_word[i] = char
        temp_word = " ".join(temp_word)
        if temp_word == self.secret_lb["text"]:
            size = 250, 325
            self.stage += 1
            im = Image.open("stages/" + str(self.stage) + ".png")
            im.thumbnail(size)
            self.canvas.image = ImageTk.PhotoImage(im)
            self.canvas.create_image(140, 180, image=self.canvas.image)
            if self.stage == 6:
                self.game_over = True
                self.check_game_ended()
        else:
            self.secret_lb["text"] = temp_word
            self.check_game_ended()

    def check_game_ended(self):
        if "_" not in self.secret_lb["text"] or self.game_over:
            msg_box = messagebox.askyesno(message="Do you want to play again?")
            if msg_box:
                self.frame.destroy()
                new_secret_word = get_words(filename)
                GUI(self.window, new_secret_word)
            else:
                exit()


secret_word = get_words(filename)
new_window = tk.Tk()
GUI(new_window, secret_word)
new_window.mainloop()
