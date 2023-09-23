from PIL import Image, ImageTk, ImageDraw
import random
from tools.image_processor import ImageProcessor

class Genetic():
    def __init__(self):
        self.image_processor = ImageProcessor()

    def draw_image(self):
        imagen = Image.new("RGB", (400, 400))

        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(imagen)

        # Llena la imagen con colores aleatorios
        for x in range(400):
            for y in range(400):
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
        pixels_image = imagen

        self.image_processor.process_image(pixels_image)
        return self.image_processor.decompose_image()

#ImageTk.PhotoImage(pixels_image)