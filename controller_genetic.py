from tools.image_processor import ImageProcessor
from PIL import ImageTk

class ControllerGenetic():
    def __init__(self):
        # original image
        self.image = None
        # array with all the rgb values of the objective image
        self.pixels_image = None
        # objective image
        self.artistic_image = None

        #instance of ImageProcessor
        self.image_processor = ImageProcessor()

    def proccess_pixels(self, image):
        self.image = image

        self.artistic_image = self.image_processor.pixelate(self.image, 8)

        self.image_processor.process_image(self.artistic_image)

        self.pixels_image = self.image_processor.decompose_image()