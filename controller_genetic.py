from tools.image_processor import ImageProcessor

class ControllerGenetic():
    def __init__(self):
        self.image = None
        self.pixels_image = None
        self.artistic_image = None

        #instance of ImageProcessor
        self.image_processor = ImageProcessor()

    def proccess_pixels(self, image):
        self.image = image
        self.image_processor.process_image(image)

        self.pixels_image = self.image_processor.decompose_image()

        print(self.pixels_image)
        print(len(self.pixels_image))

    def pixelate_image(self):
        self.artistic_image = self.image_processor.pixelate(self.image)