"""
ImageHandler class to handle image loading, processing,
encoding and decoding.
"""
import base64
import os
from typing import Optional, Tuple

from PIL import Image

from modules.config.configuration import Configuration


class ImageHandler(object):
    """
    """
    def __init__(self, image_file: str, state: Optional[str], config: Configuration):
        self._image_name = image_file
        self._state = state
        self._config = config
        self.image_path = self._get_image_path()
        self.image = None
    
    def _get_image_path(self) -> str:
        image_path = None
        if self._state is None:
            pass
        else:
            if self._state == 'raw':
                image_path = os.path.join(
                    self._config.raw_images_path, self._image_name
                )
            else:
                image_path = os.path.join(
                    self._config.processed_images_path, self._state, self._image_name
                )
        return image_path

    def load(self) -> None:
        self.image = Image.open(self.image_path)
    
    def save(self) -> None:
        self.image.save(self.image_path, optimize=True)

    def resize(self, size: Tuple[int, int] = (200, 200)):
        self.image.thumbnail(size, Image.ANTIALIAS)
        self.image = self.image.convert('L')
        self._state = 'resized'
        self.image_path = self._get_image_path()

    def get_decoded_base64_png(self) -> None:
        encoded = base64.b64encode(open(self.image_path, 'rb').read())
        decoded = encoded.decode('UTF-8')
        return decoded
