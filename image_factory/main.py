import os

from modules.config.configuration import Configuration
from image_factory.image_handler import ImageHandler


def main():
    config = Configuration()
    for img_file in os.listdir(config.raw_images_path):
        if img_file != '.gitkeep':
            img_handler = ImageHandler(img_file, 'raw', config)
            img_handler.load()
            img_handler.resize()
            img_handler.save()


if __name__ == "__main__":
    main()
