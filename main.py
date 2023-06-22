from tkinter import *
import random

class TypingTest:
    def __init__(self):

        self.texts = open("essay.txt", "r").read().split("\n")
        self.window = Tk()
        self.window.title("Typing Speed Test - by Jonathan Shamwana")
        self.window.geometry("900x675")
        self.window.config(padx=20, pady=30)
        self.window.resizable(width=False, height=False)
        self.time_counter = 0
        self.running = False
        self.cpm = 0
        self.wpm = 0
        self.percentile = None
        self.name = None
        self.top_scores = []

        self.heading = Label(self.window, text="How quickly can you type?", font=("Helvetica", 18), width=35)
        self.heading.grid(row=0, column=0, columnspan=2)

        logo_image = PhotoImage(file="images/clock.png")
        self.logo_label = Label(self.window, image=logo_image)
        self.logo_label.grid(row=1, column=0, columnspan=2, pady=(15,30))

        self.name_label = Label(text="Enter your name:")
        self.name_label.grid(row=2, column=0, columnspan=2)

        self.name_entry = Entry(text="Enter your name:")
        self.name_entry.focus()
        self.name_entry.grid(row=3, column=0, columnspan=2, pady=(0,10))

        self.label_frame = LabelFrame(self.window)
        self.label_frame.grid(row=4, column=0, columnspan=2, pady=(10,30))

        self.instructions_title = Label(self.label_frame, text="Instructions:")
        self.instructions_title.grid(row=4, column=0, columnspan=2, pady=(10,0))

        self.instructions_label = Label(self.label_frame, text="1. You have 60 seconds to type as many words as you can.\n2. The timer starts as soon as you start typing.\n3. Correct all errors before proceeding.\n4. When you finish a sentence, a new one will appear.", justify="left")
        self.instructions_label.grid(row=5, column=0, columnspan=2, pady=(10,30), padx=10)

        self.copy_label = Label(self.window, text=random.choice(self.texts), font=("Helvetica", 15), justify="left")
        self.copy_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.entry = Entry(self.window, width=90)
        self.entry.grid(row=7, column=0, columnspan=2, pady=10)
        self.entry.bind("<KeyRelease>", self.start_test)

        self.restart_button = Button(self.window, text="Restart", command=self.reset)
        self.restart_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.window.mainloop()


    def start_test(self, event):

        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                self.timer()

        if not self.copy_label.cget("text").startswith(self.entry.get()):
            self.entry.config(fg="red")
        elif self.copy_label.cget("text") == self.entry.get():
            self.entry.config(fg="green")
            self.copy_label.config(text=random.choice(self.texts))
            self.entry.delete(0, END)
        else:
            self.entry.config(fg="white")

    def timer(self):
        if self.time_counter == 30:
            self.running = False
            self.show_results()
        else:
            self.time_counter += 1
            cps = len(self.entry.get()) / self.time_counter
            self.cpm = cps * 60
            wps = len(self.entry.get().split(" ")) / self.time_counter
            self.wpm = wps * 60
            self.window.after(1000, self.timer)

    def update_scoreboard(self):
        name = self.name_entry.get()
        with open("scoreboard.txt", "a") as file:
            file.write(f"\n{name},{self.wpm}")

        data = open("scoreboard.txt", "r").read().split("\n")
        score_dict = {}
        for line in data:
            if line != "":
                combo = line.split(",")
                score_dict[combo[0].title()] = float(combo[1])

        sorted_dict = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
        for key, value in sorted_dict[:3]:
            self.top_scores.append((key, value))

    def calculate_percentile(self):
        if self.wpm < 30:
            self.percentile = "10th"
        elif self.wpm < 40:
            self.percentile = "25th"
        elif self.wpm < 60:
            self.percentile = "50th"
        elif self.wpm < 80:
            self.percentile = "75th"
        elif self.wpm < 100:
            self.percentile = "90th"
        elif self.wpm < 120:
            self.percentile = "95th"
        else:
            self.percentile = "99th"

    def show_results(self):
        self.update_scoreboard()
        self.calculate_percentile()

        self.entry.config(state="disabled")
        self.entry.delete(0, END)

        results_window = Toplevel(self.window)
        results_window.title("Results")
        results_window.geometry("500x500")
        results_window.resizable(width=False, height=False)

        result_label = Label(results_window, text=f"WPM: {self.wpm:.2f}",
                             font=("Helvetica", 24), justify=CENTER)
        result_label.pack(pady=(50,10))

        percentile_label = Label(results_window, text=f"You're in the {self.percentile} percentile of typists.")
        percentile_label.pack(pady=(0,20))

        nerd_img = PhotoImage(file="images/nerd.png")
        nerd_label = Label(results_window, image=nerd_img)
        nerd_label.pack(pady=(0,20))

        table_heading = Label(results_window, text="Leaderboard")
        table_heading.pack()

        # The frame for the leaderboard table
        table_frame = Frame(results_window)
        table_frame.pack(pady=10)

        # Column headings for the leaderboard table
        header1 = Label(table_frame, text="Name", borderwidth=1, relief="solid", width=20)
        header1.grid(row=0, column=0)
        header2 = Label(table_frame, text="WPM", borderwidth=1, relief="solid", width=20)
        header2.grid(row=0, column=1)

        # Iterate over the top results dictionary to populate the leaderboard rows
        i = 0
        for value in self.top_scores:
            name = Label(table_frame, text=value[0], borderwidth=1, relief='solid', width=20)
            name.grid(row=i, column=0)
            score = Label(table_frame, text=value[1], borderwidth=1, relief="solid", width=20)
            score.grid(row=i, column=1)
            i += 1

        results_window.mainloop()

    def reset(self):
        self.top_scores.clear()
        self.running = False
        self.time_counter = 0
        self.cpm = 0
        self.wpm = 0
        self.copy_label.config(text=random.choice(self.texts))
        self.entry.config(state='normal')
        self.entry.delete(0, END)

TypingTest()