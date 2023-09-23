import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import random

from controller_genetic import ControllerGenetic
from genetic import Genetic
from genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from color_obtainer import ColorObtainer

class Menu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#252525")
        self.controller = controller

        self.controller_genetic = ControllerGenetic()
        self.first_gen = Genetic()

        label1 = tk.Label(self, text="").grid(row=0, column=0,padx=1000,pady=1000)

        font_frame = ctk.CTkFont(size=18)

        # Create a button to load an image
        load_button = ctk.CTkButton(self, text="Cargar imagen", command=self.load_image, font=font_frame)
        load_button.place(x=150, y=20)

        # Create a label to display the loaded image
        self.image_label = tk.Label(self)
        self.image_label.place(x=20, y=60)

        # photo = self.draw_image()

        # self.image_label.configure(image=photo)
        # self.image_label.image = photo

        #Generations input
        label_generations = ctk.CTkLabel(self, text="Cantidad de generaciones", fg_color="transparent", font=font_frame, text_color="white")
        label_generations.place(x=520, y= 80)

        self.entry_generations = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_generations.focus()
        self.entry_generations.place(x=540, y=110)

        #Poblations input
        label_poblations = ctk.CTkLabel(self, text="Tamaño de poblaciones", fg_color="transparent", font=font_frame, text_color="white")
        label_poblations.place(x=520, y= 120+50)

        self.entry_poblations = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_poblations.focus()
        self.entry_poblations.place(x=540, y=150+50)

        exec_button = ctk.CTkButton(self, text="Iniciar algoritmo", font=font_frame)
        exec_button.place(x=540, y=250)

        self.image_genetic_label = tk.Label(self)
        self.image_genetic_label.place(x=780,y=60)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            imported_image = Image.open(file_path)
            image = imported_image.resize((400, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Update the label to display the loaded image
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            self.controller_genetic.proccess_pixels(imported_image)

            self.start_algorithm()

    def start_algorithm(self):
        population = 20
        image_objective = self.controller_genetic.pixels_image
        y = len(image_objective) 
        x = len(image_objective[0])
        noChange = True
        parents = 10
        max_generaion = 300
        mutation = 90
        crossover_num = 2
        color_obtainer = ColorObtainer()
        color_pallete = color_obtainer.generate_color_array(self.controller_genetic.artistic_image)

        algorithm = GeneticAlgorithm(population, x, y, image_objective, noChange, parents, max_generaion, mutation, crossover_num, color_pallete)
        algorithm.execute_genetic_algorithm()