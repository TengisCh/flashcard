from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    to_learn = pandas.read_csv("data/french_words.csv")
    to_learn = to_learn.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_canvas, text="French", fill="black")
    canvas.itemconfig(word_canvas, text=current_card["French"], fill="black")
    canvas.itemconfig(background_image, image=card_front_photo)
    flip_timer = window.after(3000, func=flip)


def flip():
    canvas.itemconfig(title_canvas, text="English", fill="white")
    canvas.itemconfig(word_canvas, text=current_card["English"], fill="white")
    canvas.itemconfig(background_image, image=card_back_photo)


def is_known():
    to_learn.remove(current_card)
    updated_data = pandas.DataFrame(to_learn)
    updated_data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_photo = PhotoImage(file="images/card_front.png")
card_back_photo = PhotoImage(file="images/card_back.png")
background_image = canvas.create_image(400, 263, image=card_front_photo)
title_canvas = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_canvas = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=next_word)
cross_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=1)
next_word()

mainloop()
