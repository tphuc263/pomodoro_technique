from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = NONE
remaining_time = 0
# ---------------------------- TIMER STOP ------------------------------- #
def stop():
    global timer, remaining_time
    if timer:
        window.after_cancel(timer)
        remaining_time = convert_time_to_second(canvas.itemcget(timer_text, "text"))


# ---------------------------- TIMER STOP ------------------------------- #
def continue_cur_pomodoro():
    global timer, remaining_time
    if remaining_time > 0:
        count_down(remaining_time)


# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global timer,reps,remaining_time
    window.after_cancel(timer)
    title_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    reps = 0
    remaining_time = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_count_down():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Break", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        title_label.config(text="WORK", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps, remaining_time
    remaining_time = count
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    if minutes < 10:
        minutes = f"{0}{minutes}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_count_down()
        mark = ""
        work_session = math.floor(reps/2)
        for _ in range(work_session):
            mark += "✔"
        check_marks.config(text=mark)


# ---------------------------- CONVERT TIME TO SECOND ------------------------------- #
def convert_time_to_second(timer_str):
    minutes, second = map(int, timer_str.split(":"))
    return minutes*60 + second

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# TITLE LABEL
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
title_label.grid(column=1, row=0)

# BACKGROUND TOMATO
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 33, "bold"))
canvas.grid(column=1, row=1)

# START BUTTON
start_button = Button(text="Start", highlightthickness=0, command=start_count_down)
start_button.grid(column=0, row=2)

# RESET BUTTON
reset_button = Button(text="Reset", highlightthickness=0, command=reset)
reset_button.grid(column=2, row=2)

# STOP BUTTON
stop_button = Button(text="Stop", command=stop)
stop_button.grid(column=0, row=3)

# CONTINUE BUTTON
continue_button = Button(text="Continue", command=continue_cur_pomodoro)
continue_button.grid(column=2,row=3)

# CHECK MARKS WHEN DONE A WORD SESSION
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)


window.mainloop()
