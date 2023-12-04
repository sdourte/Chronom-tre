from tkinter import *
import tkinter as tk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class ChronometerApp:
    def __init__(self, master):
        self.master = master
        master.title("Chronomètre")

        self.image_path = "images/Affiche VIva pour chrono.png"
        self.load_background_image()

        self.master.bind('<Configure>', self._resize_image)

        self.max_duration = timedelta(hours=24)
        self.start_time = datetime.now()
        self.running = False
        self.remaining_time = datetime.now()

        self.create_widgets()

    def load_background_image(self):
        self.image = Image.open(self.image_path)
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background_label = Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def _resize_image(self, event):
        if event.widget is self.master:
            # resize background image to fit the frame size
            image = self.image.resize((event.width, event.height))
            self.background_image = ImageTk.PhotoImage(image)
            self.background_label.configure(image=self.background_image)

    def create_widgets(self):
        input_wanted = input("Voulez-vous choisir le temps (oui/non) ? ")
        if input_wanted == "oui":
            self.input_timer()
        else:
            self.max_duration = timedelta(hours=24)

        title = tk.Label(self.master, text="Chronomètre", font=('Helvetica', 20))
        title.pack()

        self.timer_label = tk.Label(self.master, font=('Helvetica', 150))
        self.timer_label.pack()

        self.update_timer_display()

        start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        start_button.pack(pady=10)

        stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer)
        stop_button.pack(pady=10)

        reset_button = tk.Button(self.master, text="Reset", command=self.reset_timer)
        reset_button.pack(pady=10)

        reprendre_button = tk.Button(self.master, text="Reprendre", command=self.reprendre_timer)
        reprendre_button.pack(pady=10)

    def update_timer_display(self):
        elapsed_time = datetime.now() - self.start_time
        self.remaining_time = max(self.max_duration - elapsed_time, timedelta())
        formatted_time = self.format_timedelta(self.remaining_time)
        self.timer_label.config(text=formatted_time)

        if self.remaining_time > timedelta() and self.running:
            self.master.after(1000, self.update_timer_display)
        elif not self.running:
            self.master

    def format_timedelta(self, delta):
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

    def start_timer(self):
        if not self.running:
            self.start_time = datetime.now()
            self.running = True
            self.update_timer_display()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.update_timer_display()

    def reset_timer(self):
        if self.start_time != datetime.now():
            self.start_time = datetime.now()
            self.running = False
            self.update_timer_display()

    def reprendre_timer(self):
        if not self.running:
            elapsed_pause_time = datetime.now() - self.start_time
            self.start_time = datetime.now() - elapsed_pause_time
            self.running = True
            self.update_timer_display()

    def input_timer(self):
        input_time = input("Entrez le nombre de temps à chronométrer (xx:xx:xx): ")
        input_time = input_time.split(":")
        self.max_duration = timedelta(hours=int(input_time[0]), minutes=int(input_time[1]), seconds=int(input_time[2]))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("960x540")
    app = ChronometerApp(root)
    root.mainloop()
