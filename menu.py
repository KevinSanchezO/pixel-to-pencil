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
        self.image_label.place(x=20+50, y=60)


        #Generations input
        label_generations = ctk.CTkLabel(self, text="Cantidad de generaciones", fg_color="transparent", font=font_frame, text_color="white")
        label_generations.place(x=520+40, y= 20)

        self.entry_generations = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_generations.focus()
        self.entry_generations.place(x=540+40, y=50)


        #Poblations input
        label_poblations = ctk.CTkLabel(self, text="Tamaño de poblaciones", fg_color="transparent", font=font_frame, text_color="white")
        label_poblations.place(x=520+40, y= 90)

        self.entry_poblations = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_poblations.focus()
        self.entry_poblations.place(x=540+40, y=120) 


        #Parents input
        label_parents = ctk.CTkLabel(self, text="Padres a seleccionar", fg_color="transparent", font=font_frame, text_color="white")
        label_parents.place(x=520+40, y= 160)

        self.entry_parents = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_parents.focus()
        self.entry_parents.place(x=540+40, y=190)


        #Mutation percent input
        label_mutation = ctk.CTkLabel(self, text="Porcentaje de mutación", fg_color="transparent", font=font_frame, text_color="white")
        label_mutation.place(x=520+40, y= 230)

        self.entry_mutation_percent = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_mutation_percent.focus()
        self.entry_mutation_percent.place(x=540+40, y=260)


        #Crossover input
        label_crossover = ctk.CTkLabel(self, text="Cantidad de cruces", fg_color="transparent", font=font_frame, text_color="white")
        label_crossover.place(x=520+40, y= 300)

        self.entry_crossover = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_crossover.focus()
        self.entry_crossover.place(x=540+40, y=330)


        #noChange input
        self.no_entry_switch_var = ctk.BooleanVar(value=True)
        switch_no_change = ctk.CTkSwitch(self, text="Permitir el cambio de los genes iguales al objetivo", variable=self.no_entry_switch_var, onvalue=True, offvalue=False)
        switch_no_change.place(x=450+40, y= 360)


        #withPallete input
        self.no_entry_pallete_var = ctk.BooleanVar(value=True)
        switch_pallete = ctk.CTkSwitch(self, text="Permitir usar la paleta de colores", variable=self.no_entry_pallete_var, onvalue=True, offvalue=False)
        switch_pallete.place(x=450+40, y= 390)


        exec_button = ctk.CTkButton(self, text="Iniciar algoritmo",  command=self.hilo1, font=font_frame)
        exec_button.place(x=540, y=550)

        #Poblations fitness
        self.label_fitness = ctk.CTkLabel(self, text="Mejor Fitness: ", fg_color="transparent", font=font_frame, text_color="white")
        self.label_fitness.place(x=520, y= 350+80)

        label_objective = ctk.CTkLabel(self, text="Imagen objetivo", fg_color="transparent", font=font_frame, text_color="white")
        label_objective.place(x=780+120+90, y=20)

        self.objective_image_label = tk.Label(self)
        self.objective_image_label.place(x=780+50+90,y=60)

        self.thread1 = threading.Thread(target=self.actualizar_texto_asincronamente)
        self.thread1.daemon = True
        self.thread1.start()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            imported_image = Image.open(file_path)
            image = imported_image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Update the label to display the loaded image
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            self.controller_genetic.proccess_pixels(imported_image)

            objective_image = self.controller_genetic.artistic_image.resize((300, 300), Image.LANCZOS)
            photo_objective = ImageTk.PhotoImage(objective_image)
            
            self.objective_image_label.configure(image=photo_objective)
            self.objective_image_label.image = photo_objective

    def start_algorithm(self):
        population = 100    #se selecciona de la pantalla  [x]
        image_objective = self.controller_genetic.pixels_image #es automática
        y = len(image_objective)      #es automatico de la imagen
        x = len(image_objective[0])     #es automatico de la imagen
        noChange = True                    #se selecciona de la pantalla [x]
        parents = 25                        #se selecciona de la pantalla [x]
        max_generaion = 300                 #se selecciona de la pantalla [x]
        mutation = 100                      #se selecciona de la pantalla de 0 a 100 [x]
        crossover_num = 2                   #se selecciona de la pantalla [x]
        color_obtainer = ColorObtainer()    #se crea automaticamente con la imagen 
        color_pallete = color_obtainer.generate_color_array(self.controller_genetic.artistic_image)
        #print(color_pallete) 
        #color_pallete2 = [sublist[:-1] for sublist in color_pallete] #se crea automaticamente
        with_pallete = True  #se selecciona de la pantalla []
        
        algorithm = GeneticAlgorithm(population, x, y, image_objective, noChange, parents, max_generaion, mutation, crossover_num, color_pallete, with_pallete)
        self.geneticA = algorithm


    def iniciar_algoritmo(self):
    # Coloca aquí la lógica de tu algoritmo
        print("entra")
        self.start_algorithm()
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