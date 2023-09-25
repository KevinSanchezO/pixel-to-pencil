from PIL import Image
import numpy as np
import re
import cv2

class ImageProcessor():
    def __init__(self):
        self.image = None

    def process_image(self, image):
        self.image = image

    def decompose_image(self):
        if self.image is not None:
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')

            pixel_values = np.array(self.image)

            return pixel_values
        else:
            print("Error, an image hasn't been loaded")

    def pixelate(self, image, pixel_size):
        width, height = image.size
        small_image = image.resize(
            (width // pixel_size, height // pixel_size),
            resample=Image.NEAREST
        )
        result_image = small_image.resize(
            (width, height),
            Image.NEAREST
        )
        result_image = result_image.convert('RGB')
        return result_image
    
    def inked(self, image):
        img = cv2.imread(image)

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicar un efecto de cómic a la imagen
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)

        color = cv2.bilateralFilter(img, 9, 300, 300)

        cartoon = cv2.bitwise_and(color, color, mask=edges)

        # Convertir la imagen resultante a formato RGB (necesario para Pillow)
        cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

        # Crear una imagen PIL desde la matriz de píxeles
        pil_image = Image.fromarray(cartoon_rgb)

        return pil_image

    
    def convert_list_image(self, rgb_list):
        height = len(rgb_list)
        width = len(rgb_list[0])

        # Convertir la lista de píxeles en un array NumPy
        rgb_array = np.array(rgb_list, dtype=np.uint8)

        # Asegurar que el array tiene el formato adecuado (alto x ancho x 3 para una imagen en RGB)
        expected_shape = (height, width, 3)
        if rgb_array.shape != expected_shape:
            raise ValueError(f"El formato del array no es compatible con una imagen RGB de {expected_shape} píxeles")

        # Crear la imagen a partir del array
        imagen = Image.fromarray(rgb_array)
        return imagen

    def convert_array_image(self, rgb_array):
        imagen = Image.fromarray(rgb_array)
        return imagen