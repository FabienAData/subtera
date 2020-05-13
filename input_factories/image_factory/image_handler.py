"""
ImageHandler class to handle image loading, processing,
encoding and decoding.
"""
import base64
import os
from typing import Optional, Tuple

from PIL import Image, ImageOps, ImageDraw

from modules.config.configuration import Configuration


class ImageHandler(object):
    """
    """
    def __init__(self, image_name: str, image_extension: str, state: Optional[str], config: Configuration):
        self.image_name = image_name
        self.image_extension = image_extension
        self._state = state
        self._config = config
        self.image_path = self._get_image_path()
        self.image = None
    
    def _get_image_path(self) -> str:
        image_path = None
        if self._state is None:
            pass
        else:
            image_file = '.'.join([self.image_name, self.image_extension])
            if self._state == 'raw':
                image_path = os.path.join(
                    self._config.raw_images_path, image_file
                )
            else:
                image_path = os.path.join(
                    self._config.processed_images_path, self._state, image_file
                )
        return image_path

    def load(self) -> None:
        self.image = Image.open(self.image_path)
    
    def save(self) -> None:
        if self.image_extension in ['jpeg', 'JPEG']:
            self.image.save(self.image_path, 'JPEG', optimize=True)
        else:
            self.image.save(self.image_path, optimize=True)

    def resize(self, size: Tuple[int, int] = (200, 200)):
        self.image.thumbnail(size, Image.ANTIALIAS)
        self.image = self.image.convert('L')
        self._state = 'resized'
        self.image_path = self._get_image_path()

    def circle(self, size: Tuple[int, int] = (200, 200)):
        self.image.thumbnail(size, Image.ANTIALIAS)
        self.image = self.image.convert('L')

        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(self.image, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        self.image = output

        self._state = 'circled'
        self.image_path = self._get_image_path()

    def get_decoded_base64_png(self) -> None:
        encoded = base64.b64encode(open(self.image_path, 'rb').read())
        decoded = encoded.decode('UTF-8')
        return decoded

