"""
AudioWavDownloader class to handle audio downloading from Youtube.
"""
from __future__ import unicode_literals
import youtube_dl

import os, sys

from modules.config.configuration import Configuration
from input_factories.common import mapping_category_to_class
from input_factories.data_factory.datasets.artists import Artists
from input_factories.data_factory.datasets.collaboration_songs import CollaborationSongs


class AudioWavDownloader(object):
    """
    """
    def __init__(
        self,
        audio_name: str,
        audio_category: str,
        audio_name_col: str,
        config: Configuration,
    ) -> None:
        self.audio_name = audio_name
        self.audio_category = audio_category
        self.audio_name_col = audio_name_col
        self._config = config
        self.audio_path = self._get_audio_path()
    
    def _get_audio_path(self) -> str:
        audio_file = '.'.join([self.audio_name, 'wav'])
        audio_path = os.path.join(
            self._config.raw_audios_path, self.audio_category, audio_file
        )
        return audio_path
    
    def download_wav(self) -> None:
        youtube_url = self._get_youtube_url()
        ydl_opts = {
            'outtmpl': self.audio_path,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    
    def _get_youtube_url(self) -> str:
        data_category_class = mapping_category_to_class[self.audio_category]
        youtube_urls_data = data_category_class('youtube_urls', self._config).data
        url = youtube_urls_data.loc[
            youtube_urls_data[self.audio_name_col] == self.audio_name,
            'youtube_url'
        ].values[0]
        return url


def download_all_collaboration_songs(config: Configuration) -> None:
    collab_songs_data = CollaborationSongs('youtube_urls', config).data
    for song in collab_songs_data['song_name'].sort_values():
        print(song)
        if song + '.wav' in os.listdir(
            os.path.join(config.raw_audios_path, 'collaboration_songs')
        ):
            pass
        else:
            audio_wav_downloader = AudioWavDownloader(audio_name=song, audio_category='collaboration_songs', audio_name_col='song_name', config=config)
            audio_wav_downloader.download_wav()


if __name__ == '__main__':
    config = Configuration()
    if sys.argv[1] == 'collaboration_songs':
        download_all_collaboration_songs(config)
