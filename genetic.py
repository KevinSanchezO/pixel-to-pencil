from PIL import Image, ImageTk, ImageDraw
import random
from tools.image_processor import ImageProcessor

class Genetic():
    def __init__(self):
        self.image_processor = ImageProcessor()

    def draw_image(self, xParam, yParam):
        imagen = Image.new("RGB", (xParam, yParam))

        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(imagen)

        # Llena la imagen con colores aleatorios
        for x in range(xParam):
            for y in range(yParam):
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
        pixels_image = imagen

        self.image_processor.process_image(pixels_image)
        return self.image_processor.decompose_image()
    
    #Dibuja una imagen completamente en blanco
    def draw_blank_image(self, xParam, yParam):
        imagen= Image.new("RGB", (xParam, yParam), (255, 255, 255))
        pixels_image = imagen

        self.image_processor.process_image(pixels_image)
        return self.image_processor.decompose_image()

#ImageTk.PhotoImage(pixels_image)