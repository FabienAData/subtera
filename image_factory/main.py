import os
import re

from modules.config.configuration import Configuration
from image_factory.image_handler import ImageHandler


def main():
    config = Configuration()
    for img_file in os.listdir(config.raw_images_path):
        if img_file != '.gitkeep':
            image_name = re.sub(r'\..*$', '', img_file)
            img_extension = re.sub(r'^.*\.', '', img_file)
            img_handler = ImageHandler(
                image_name,
                img_extension,
                'raw',
                config
                )
            img_handler.load()
            img_handler.resize()
            img_handler.save()


if __name__ == "__main__":
    main()
