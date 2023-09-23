from PIL import Image, ImageTk, ImageDraw
import random
from tools.image_processor import ImageProcessor

class Genetic():
    def __init__(self):
        self.image_processor = ImageProcessor()

    def draw_image(self, yParam, xParam):
        imagen = Image.new("RGB", (yParam, xParam))

        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(imagen)

        # Llena la imagen con colores aleatorios
        for x in range(yParam):
            for y in range(xParam):
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
        pixels_image = imagen

        self.image_processor.process_image(pixels_image)
        return self.image_processor.decompose_image()
    
    #Dibuja una imagen completamente en blanco
    def draw_blank_image(self, yParam, xParam):
        imagen= Image.new("RGB", (yParam, xParam), (255, 255, 255))
        pixels_image = imagen

        self.image_processor.process_image(pixels_image)
        return self.image_processor.decompose_image()

#ImageTk.PhotoImage(pixels_image)