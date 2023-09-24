import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import random

from controller_genetic import ControllerGenetic
from genetic import Genetic
from genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from color_obtainer import ColorObtainer

import threading
import time

class Menu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#252525")
        self.controller = controller

        self.controller_genetic = ControllerGenetic()
        self.first_gen = Genetic()
        self.geneticA = None

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
        label_poblations.place(x=510, y= 120+50)

        

        self.entry_poblations = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_poblations.focus()
        self.entry_poblations.place(x=540, y=150+50)

        exec_button = ctk.CTkButton(self, text="Iniciar algoritmo",  command=self.hilo1, font=font_frame)
        exec_button.place(x=540, y=250)

        #Poblations fitness
        self.label_fitness = ctk.CTkLabel(self, text="BestFitness: ", fg_color="transparent", font=font_frame, text_color="white")
        self.label_fitness.place(x=520, y= 250+50)

        self.image_genetic_label = tk.Label(self)
        self.image_genetic_label.place(x=780,y=60)

        self.thread1 = threading.Thread(target=self.actualizar_texto_asincronamente)
        self.thread1.daemon = True
        self.thread1.start()

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
        population = 100    #se selecciona de la pantalla
        image_objective = self.controller_genetic.pixels_image #es automática
        y = len(image_objective)      #es automatico de la imagen
        x = len(image_objective[0])     #es automatico de la imagen
        noChange = True                    #se selecciona de la pantalla
        parents = 25                        #se selecciona de la pantalla
        max_generaion = 300                 #se selecciona de la pantalla
        mutation = 100                      #se selecciona de la pantalla de 0 a 100
        crossover_num = 2                   #se selecciona de la pantalla
        color_obtainer = ColorObtainer()    #se crea automaticamente con la imagen 
        color_pallete = color_obtainer.generate_color_array(self.controller_genetic.artistic_image) 
        color_pallete2 = [sublist[:-1] for sublist in color_pallete] #se crea automaticamente
        with_pallete = True  #se selecciona de la pantalla
        print(color_pallete2)
        algorithm = GeneticAlgorithm(population, x, y, image_objective, noChange, parents, max_generaion, mutation, crossover_num, color_pallete2, with_pallete)
        self.geneticA = algorithm


    def iniciar_algoritmo(self):
    # Coloca aquí la lógica de tu algoritmo
        print("entra")
        self.geneticA.execute_genetic_algorithm()

# Función para configurar el evento del botón
    def hilo1(self):
    # Crea un nuevo hilo y configura la función a ejecutar en ese hilo
        thread = threading.Thread(target=self.iniciar_algoritmo)
    # Inicia el hilo
        thread.start()
        

    def actualizar_texto_asincronamente(self):
        contador = 0
        while True:
            time.sleep(1)  # Espera 1 segundo (en otro hilo)
            contador += 1
            nuevo_texto = f"BestFitness: {contador}"  #bestFitness[-1] dl algoritmo genético, la imagen está en best[-1]

            # Actualiza el texto del label en el hilo principal utilizando configure
            self.label_fitness.configure(text=nuevo_texto)