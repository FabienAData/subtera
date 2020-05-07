"""
AudioHandler class to handle audio loading, encoding and decoding.
"""
import base64
import os

from modules.config.configuration import Configuration


class AudioHandler(object):
    """
    """
    def __init__(self, audio_name: str, audio_extension: str, config: Configuration):
        self.audio_name = audio_name
        self.audio_extension = audio_extension
        self._config = config
        self.audio_path = self._get_audio_path()
    
    def _get_audio_path(self) -> str:
        audio_file = '.'.join([self.audio_name, self.audio_extension])
        audio_path = os.path.join(
            self._config.audios_path, audio_file
        )
        return audio_path

    def get_decoded_base64_str(self) -> str:
        encoded = base64.b64encode(open(self.audio_path, 'rb').read())
        decoded = encoded.decode('UTF-8')
        return decoded
