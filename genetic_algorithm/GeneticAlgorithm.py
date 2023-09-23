import random
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import random

class GeneticAlgorithm:
    def __init__(self, population_size, genes_sizeX, genes_sizeY, objective):
        self.population_size = population_size
        self.genes_sizeX = genes_sizeX
        self.genes_sizeY = genes_sizeY
        self.objective = objective
        self.population = []
        self.generation = 1

    def population_init(self):
        for _ in range(self.poblacion_size/2):
            self.population  += self.decompose_image(self.draw_pixel_image())
        for _ in range(self.poblacion_size/2):
            self.population += self.decompose_image(self.draw_blank_image())

    def fitness_calculation(self, genes):
        return 

    def select_parents(self):
        return 

    def crossover(self, parent1, parent2):
        return 

    def mutate(self, hijo):
        return

    def evolve(self):
        return
        # nueva_generacion = []

        # for _ in range(self.poblacion_size):
        #     padre1, padre2 = self.seleccionar_padres()
        #     hijo = self.cruzar(padre1, padre2)

        #     if random.random() < 0.1:  # Probabilidad de mutación
        #         self.mutar(hijo)

        #     nueva_generacion.append(hijo)

        # self.poblacion = nueva_generacion
        # self.generation += 1

    def decompose_image(self, image):
        if image is not None:
            if image.mode != 'RGB':
                image = image.convert('RGB')

            pixel_values = np.array(image)

            return pixel_values
        else:
            print("Error, an image hasn't been loaded")

    #Dibuja una imagen pixeleada de colores randoms del tamaño de la imagen objetivo    
    def draw_pixel_image(self):
        imagen = Image.new("RGB", (self.genes_sizeX, self.genes_sizeY))

        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(imagen)

        # Llena la imagen con colores aleatorios
        for x in range(self.genes_sizeY):
            for y in range(self.genes_sizeX):
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
        pixels_image = imagen

        return ImageTk.PhotoImage(pixels_image)
    
    #Dibuja una imagen completamente en blanco
    def draw_blank_image(self):
        imagen_blanca = Image.new("RGB", (self.genes_sizeX, self.genes_sizeY), (255, 255, 255))
        return ImageTk.PhotoImage(imagen_blanca)
    
