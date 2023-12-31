import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import random
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import io

from controller_genetic import ControllerGenetic
from genetic import Genetic
from genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from color_obtainer import ColorObtainer
from tools.image_processor import ImageProcessor

import threading
import time
from queue import Queue

class Menu(tk.Frame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, bg="#252525")
        self.controller = controller
        self.root = root

        self.controller_genetic = ControllerGenetic()
        self.first_gen = Genetic()
        self.geneticA = None
        self.queue = Queue()
        self.image_processor = ImageProcessor()
        self.file_path = None

        fig = plt.figure()
        fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
        fig.set_size_inches(5, 3)
        fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack()
        self.canvas.get_tk_widget().place(x=350, y=500)

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
        self.entry_generations.configure(validate="key", validatecommand=(self.register(self.validate_int), "%P"))

        #Poblations input
        label_poblations = ctk.CTkLabel(self, text="Tamaño de poblaciones", fg_color="transparent", font=font_frame, text_color="white")
        label_poblations.place(x=520+40, y= 90)

        self.entry_population = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_population.focus()
        self.entry_population.place(x=540+40, y=120) 
        self.entry_population.configure(validate="key", validatecommand=(self.register(self.validate_int), "%P"))


        #Parents input
        label_parents = ctk.CTkLabel(self, text="Padres a seleccionar", fg_color="transparent", font=font_frame, text_color="white")
        label_parents.place(x=520+40, y= 160)

        self.entry_parents = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_parents.focus()
        self.entry_parents.place(x=540+40, y=190)
        self.entry_parents.configure(validate="key", validatecommand=(self.register(self.validate_int), "%P"))


        #Mutation percent input
        label_mutation = ctk.CTkLabel(self, text="Porcentaje de mutación", fg_color="transparent", font=font_frame, text_color="white")
        label_mutation.place(x=520+40, y= 230)

        self.entry_mutation_percent = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_mutation_percent.focus()
        self.entry_mutation_percent.place(x=540+40, y=260)
        self.entry_mutation_percent.configure(validate="key", validatecommand=(self.register(self.validate_int), "%P"))

        #Crossover input
        label_crossover = ctk.CTkLabel(self, text="Cantidad de cruces", fg_color="transparent", font=font_frame, text_color="white")
        label_crossover.place(x=520+40, y= 300)

        self.entry_crossover = ctk.CTkEntry(self, width=150, height=30, font=font_frame, border_width=2)
        self.entry_crossover.focus()
        self.entry_crossover.place(x=540+40, y=330)
        self.entry_crossover.configure(validate="key", validatecommand=(self.register(self.validate_int), "%P"))

        #noChange input
        self.no_change_entry_switch_var = ctk.BooleanVar(value=True)
        switch_no_change = ctk.CTkSwitch(self, text="Permitir el cambio de los genes iguales al objetivo", variable=self.no_change_entry_switch_var, onvalue=True, offvalue=False)
        switch_no_change.place(x=450+40, y= 360)


        #withPallete input
        self.pallete_entry_var = ctk.BooleanVar(value=True)
        switch_pallete = ctk.CTkSwitch(self, text="Permitir usar la paleta de colores", variable=self.pallete_entry_var, onvalue=True, offvalue=False)
        switch_pallete.place(x=450+40, y= 390)


        exec_button = ctk.CTkButton(self, text="Iniciar algoritmo",  command=self.set_parameters_algorithm, font=font_frame)
        exec_button.place(x=540+40, y=350+80)


        #drop down menu to select the art filter of the image
        self.filter = ctk.StringVar(value="Pixel-art")
        self.option_menu = ctk.CTkOptionMenu(self, values=["Pixel-art", "Entintado"], command=self.change_filter, variable=self.filter)
        self.option_menu.place(x=20+70, y=350+80)


        label_objective = ctk.CTkLabel(self, text="Imagen objetivo", fg_color="transparent", font=font_frame, text_color="white")
        label_objective.place(x=780+120+90, y=20)

        self.objective_image_label = tk.Label(self)
        self.objective_image_label.place(x=780+50+90,y=60)


        # These widgets will display the data of the algorithm during excecution
        # These widgets will display the data of the algorithm during excecution

        label_current_individual = ctk.CTkLabel(self, text="Mejor individuo actual", fg_color="transparent", font=font_frame, text_color="white")
        label_current_individual.place(x=990, y=360+20)

        self.current_individual_image_label = tk.Label(self)
        self.current_individual_image_label.place(x=920,y=390+20)


        #Poblations fitness
        self.label_fitness = ctk.CTkLabel(self, text="Mejor Fitness: 0", fg_color="transparent", font=font_frame, text_color="white")
        self.label_fitness.place(x=20+50, y= 450+80)

        #Current gen
        self.label_gen = ctk.CTkLabel(self, text="Generacion actual: 0", fg_color="transparent", font=font_frame, text_color="white")
        self.label_gen.place(x=20+50, y= 450+80+30)

        #Represents the current gen in repetition
        self.label_gen_repetition = ctk.CTkLabel(self, text="Generacion mostrada en la repeticion: 0", fg_color="transparent", font=font_frame, text_color="white")
        self.label_gen_repetition.place(x=920, y=780)

    def change_filter(self, *args):
        self.apply_filter()

    def validate_int(self, value):
        # Utiliza una expresión regular para verificar si el valor es un entero
        return re.match("^[0-9]*$", value) is not None

    def load_image(self):
        self.reset_to_initial_state()

        file_path = filedialog.askopenfilename(filetypes=[("", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.file_path = file_path
            self.apply_filter()

    def apply_filter(self):
        imported_image = Image.open(self.file_path)
        image = imported_image.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Update the label to display the loaded image
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        if (self.filter.get() == "Pixel-art"):
            self.controller_genetic.proccess_pixels(imported_image)
        elif(self.filter.get() == "Entintado"):
            self.controller_genetic.proccess_pixels_inked(self.file_path)

        objective_image = self.controller_genetic.artistic_image.resize((300, 300), Image.LANCZOS)
        photo_objective = ImageTk.PhotoImage(objective_image)
            
        self.objective_image_label.configure(image=photo_objective)
        self.objective_image_label.image = photo_objective
        

    def set_parameters_algorithm(self):
        population = int(self.entry_population.get())    #se selecciona de la pantalla  [x]
        image_objective = self.controller_genetic.pixels_image #es automática
        y = len(image_objective)      #es automatico de la imagen
        x = len(image_objective[0])     #es automatico de la imagen
        noChange = self.no_change_entry_switch_var.get() #se selecciona de la pantalla [x]
        parents = int(self.entry_parents.get()) #se selecciona de la pantalla [x]
        max_generaion = int(self.entry_generations.get()) #se selecciona de la pantalla [x]
        mutation = int(self.entry_mutation_percent.get()) #se selecciona de la pantalla de 0 a 100 [x]
        crossover_num = int(self.entry_crossover.get()) #se selecciona de la pantalla [x]
        color_obtainer = ColorObtainer()    #se crea automaticamente con la imagen 
        color_pallete = color_obtainer.generate_color_array(self.controller_genetic.artistic_image)
        with_pallete = self.pallete_entry_var.get()  #se selecciona de la pantalla [x]
        
        algorithm = GeneticAlgorithm(population, x, y, image_objective, noChange, parents, max_generaion, mutation, crossover_num, color_pallete, with_pallete, self.queue)
        self.geneticA = algorithm

        self.iniciar_algoritmo()

    def iniciar_algoritmo(self):
        print(self.entry_population.get())
        print(self.no_change_entry_switch_var.get())
        print(self.entry_parents.get())
        print(self.entry_generations.get())
        print(self.entry_mutation_percent.get())
        print(self.entry_crossover.get())
        print(self.pallete_entry_var.get())

        self.label_fitness.configure(text="Mejor Fitness: 0")
        self.label_gen.configure(text="Generacion actual: 0")
        self.label_gen_repetition.configure(text="Generacion mostrada en la repeticion: 0")

        print("entra")
        self.thread1 = threading.Thread(target=self.geneticA.execute_genetic_algorithm)
        self.thread1.daemon = True
        self.thread1.start()
        self.update_gui()

    def update_gui(self):
        if not self.queue.empty():
            parameter_values = self.queue.get()
            nuevo_texto_fitness = f"Mejor Fitness: {parameter_values['fitness'][-1]}"
            nuevo_texto_gen = f"Generacion actual: {parameter_values['gen_actual']-1}"
            imagen_individuo = None
            if (parameter_values['gen_actual'] < 3):
                imagen_individuo=self.image_processor.convert_array_image(parameter_values['mejor_individuo'][-1])
            else:
                imagen_individuo=self.image_processor.convert_list_image(parameter_values['mejor_individuo'][-1])
            imagen_mejor_actual = imagen_individuo.resize((300, 300), Image.LANCZOS)
            photo_individuo = ImageTk.PhotoImage(imagen_mejor_actual)

            buffer = parameter_values["grafico"]
            fig = plt.figure()
            fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
            fig.set_size_inches(5, 3)
            fig.add_subplot(111)
            fig.figimage(plt.imread(buffer), 10, 10, zorder=10)

            # Establecer la nueva imagen en el widget de lienzo
            self.canvas.figure = fig
            self.canvas.draw()

            # Posicionar la imagen utilizando el método place
            self.canvas.get_tk_widget().place(x=350, y=500)


            # Actualiza el texto del label en el hilo principal utilizando configure
            self.label_fitness.configure(text=nuevo_texto_fitness)
            self.label_gen.configure(text=nuevo_texto_gen)
            self.current_individual_image_label.configure(image=photo_individuo)
            self.current_individual_image_label.image = photo_individuo

            if (parameter_values['gen_actual'] > self.geneticA.max_generation or self.geneticA.completed):
                self.start_image_update_thread(parameter_values['mejor_individuo'])

        self.root.after(100, self.update_gui)

    def start_image_update_thread(self, images):
        # Función para iniciar un hilo que mostrará las imágenes cada segundo
        self.image_update_thread = threading.Thread(target=self.update_image_thread, args=(images,))
        self.image_update_thread.start()

    def update_image_thread(self, images):
        current_image_index = 0

        # Función que se ejecutará en el hilo para mostrar imágenes cada segundo
        while current_image_index < len(images):
            image_data = images[current_image_index]

            imagen_individuo = None
            if (current_image_index == 0):
                imagen_individuo=self.image_processor.convert_array_image(image_data)
            else:
                imagen_individuo=self.image_processor.convert_list_image(image_data)

            
            imagen_mejor_actual = imagen_individuo.resize((300, 300), Image.LANCZOS)
            photo_individuo = ImageTk.PhotoImage(imagen_mejor_actual)

            # Actualiza la imagen en la etiqueta
            self.current_individual_image_label.configure(image=photo_individuo)
            self.current_individual_image_label.image = photo_individuo

            # Incrementa el índice para la próxima imagen
            current_image_index += 1
            nuevo_texto_gen = f"Generacion mostrada en la repeticion: {current_image_index}"
            self.label_gen_repetition.configure(text=nuevo_texto_gen)

            time.sleep(1)

        # El hilo ha terminado
        self.image_update_thread = None

    def reset_to_initial_state(self):
        self.controller_genetic = ControllerGenetic()
        self.first_gen = Genetic()
        self.geneticA = None
        self.queue = Queue()
        self.image_processor = ImageProcessor()
        self.file_path = None
        self.geneticA = None
        self.no_change_entry_switch_var.set(True)
        self.pallete_entry_var.set(True)

        self.label_fitness.configure(text="Mejor Fitness: 0")
        self.label_gen.configure(text="Generacion actual: 0")
        self.label_gen_repetition.configure(text="Generacion mostrada en la repeticion: 0")
