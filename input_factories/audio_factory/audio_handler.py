"""
AudioHandler class to handle audio loading, encoding and decoding.
"""
from __future__ import unicode_literals
import youtube_dl
import os

import base64


from modules.config.configuration import Configuration
from input_factories.common import mapping_category_to_class


class AudioHandler(object):
    """
    """
    def __init__(
        self,
        audio_name: str,
        audio_extension: str,
        category: str,
        state: str,
        config: Configuration
        ) -> None:
        self.audio_name = audio_name
        self.audio_extension = audio_extension
        self.category = category
        self.state = state
        self._config = config
        self.audio_path = self._get_audio_path()
    
    def _get_audio_path(self) -> str:
        audio_file = '.'.join([self.audio_name, self.audio_extension])
        if self.state == 'raw':
            audio_path = os.path.join(
                self._config.raw_audios_path, self.category, audio_file
            )
        elif self.state == 'processed':
            audio_path = os.path.join(
                self._config.processed_audios_path, self.category, audio_file
            )
        return audio_path
    
    def download_youtube_mp3(self) -> None:
        youtube_url = self._get_youtube_url()
        ydl_opts = {
            'outtmpl': self.audio_path,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    
    def _get_youtube_url(self) -> str:
        data_category_class = mapping_category_to_class[self.category]
        youtube_urls_data = data_category_class('youtube_urls', self._config).data
        url = youtube_urls_data.loc[
            youtube_urls_data['artist_id'] == self.audio_name,
            'youtube_url'
        ].values[0]
        return url

    def get_decoded_base64_str(self) -> str:
        encoded = base64.b64encode(open(self.audio_path, 'rb').read())
        decoded = encoded.decode('UTF-8')
        return decoded
