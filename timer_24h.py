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
        
        if input_wanted == "oui":
            self.input_timer()
        else:
            self.max_duration = timedelta(hours=24)
            
        global_frame = tk.Frame(self.master, bg="white", highlightthickness=8, highlightbackground="#2E338D", bd=10, padx=10, pady=10)

        global_canva = tk.Canvas(global_frame, bg="white", highlightbackground="white")

        #title = tk.Label(global_canva, bg="white", text="Chronomètre", font=('Courier', 20))
        #title.grid(row=0, column=0)

        self.timer_label = tk.Label(global_canva, bg="white", fg="#2E338D", font=('Helvetica', 150))
        self.timer_label.grid(row=1, column=0, pady=10)

        self.update_timer_display()
        
        button_canva = tk.Canvas(global_canva, bg="white", highlightbackground="white")

        start_button = tk.Button(button_canva, text="Start", command=self.start_timer, font=("Arial", 20), bg="#2E338D", fg="white")
        start_button.grid(row=0, column=0, padx=10)
        start_button.bind('<Enter>', lambda event, button=start_button: self.on_enter(event, button, "#2E338D", "#DE5B35"))
        start_button.bind('<Leave>', lambda event, button=start_button: self.on_leave(event, button, "#2E338D", "white"))

        stop_button = tk.Button(button_canva, text="Stop", command=self.stop_timer, font=("Arial", 20), bg="#2E338D", fg="white")
        stop_button.grid(row=0, column=1, padx=10)
        stop_button.bind('<Enter>', lambda event, button=stop_button: self.on_enter(event, button, "#2E338D", "#DE5B35"))
        stop_button.bind('<Leave>', lambda event, button=stop_button: self.on_leave(event, button, "#2E338D", "white"))

        reset_button = tk.Button(button_canva, text="Reset", command=self.reset_timer, font=("Arial", 20), bg="#2E338D", fg="white")
        reset_button.grid(row=0, column=2, padx=10)
        reset_button.bind('<Enter>', lambda event, button=reset_button: self.on_enter(event, button, "#2E338D", "#DE5B35"))
        reset_button.bind('<Leave>', lambda event, button=reset_button: self.on_leave(event, button, "#2E338D", "white"))

        reprendre_button = tk.Button(button_canva, text="Reprendre", command=self.reprendre_timer, font=("Arial", 20), bg="#2E338D", fg="white")
        reprendre_button.grid(row=0, column=3, padx=10)
        reprendre_button.bind('<Enter>', lambda event, button=reprendre_button: self.on_enter(event, button, "#2E338D", "#DE5B35"))
        reprendre_button.bind('<Leave>', lambda event, button=reprendre_button: self.on_leave(event, button, "#2E338D", "white"))
        
        global_frame.place(relx=0.09, rely=0.51)  # Placez la Frame en bas à gauche
        global_canva.grid(row=0, column=0)  # Placez le canva en bas à gauche
        button_canva.grid(row=2, column=0)

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

    def on_enter(self, event, button, bg_color, fg_color):
        button.config(bg=bg_color, fg=fg_color)

    def on_leave(self, event, button, bg_color, fg_color):
        button.config(bg=bg_color, fg=fg_color)

def toggle_fullscreen(event):
    # Vérifiez si la fenêtre est actuellement en mode plein écran
    if root.attributes('-fullscreen'):
        # Quittez le mode plein écran
        root.attributes('-fullscreen', False)
    else:
        # Mettez la fenêtre en mode plein écran
        root.attributes('-fullscreen', True)

if __name__ == "__main__":
    input_wanted = input("Voulez-vous choisir le temps (oui/non) ? ")
    root = tk.Tk()
    # Mettez la fenêtre en plein écran au départ
    root.attributes('-fullscreen', True)

    # Liez la touche "Échap" à la fonction toggle_fullscreen
    root.bind('<Escape>', toggle_fullscreen)
    
    root.geometry("960x540")
    app = ChronometerApp(root)
    root.mainloop()
