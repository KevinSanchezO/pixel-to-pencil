import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from menu import Menu

# Supported modes : Light, Dark, System
ctk.set_appearance_mode("System")
 
# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("blue")   

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the geometry of the main window
        self.geometry("1040x680")

        self.title("Libreria Universo")

        # Create the container frame
        self.container = tk.Frame(self, bg="#252525")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            "Menu": Menu
        }

        for name, F in self.frames.items():
            frame = F(self.container, self)
            self.frames[name] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        # Show the first frame
        self.show_frame("Menu")

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = Main()
    app.mainloop()