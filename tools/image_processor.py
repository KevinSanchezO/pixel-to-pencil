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