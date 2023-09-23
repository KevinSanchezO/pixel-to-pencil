from PIL import Image
import numpy as np

class ColorObtainer():
    def init(self):
        self.image = None
        self.color_array = None

    def generate_color_array(self, image):
        self.image = image
        pixel_values = np.array(self.image)
        height, width, _ = pixel_values.shape
        unique_colors = []

        for i in range(height):
            for j in range(width):
                rgb_color = tuple(pixel_values[i, j])
                if rgb_color not in unique_colors:
                    unique_colors.append(rgb_color)

        self.color_array = [list(color) for color in unique_colors]

        return self.color_array