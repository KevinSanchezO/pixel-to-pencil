from PIL import Image
import numpy as np

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
        return result_image
    
    def convert_array_image(self, rgb_array):
        imagen = Image.fromarray(rgb_array)
        return imagen