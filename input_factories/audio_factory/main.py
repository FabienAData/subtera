import os
import re

from modules.config.configuration import Configuration
from input_factories.audio_factory.audio_handler import AudioHandler
from input_factories.data_factory.datasets.artists import Artists


def main():
    config = Configuration()
    artists_data = Artists('clean', config).data

    for artist_id in artists_data['artist_id'].sort_values():
        print(artist_id)
        if artist_id + '.mp3' in os.listdir(
            os.path.join(config.raw_audios_path, 'artists'
            )):
            pass
        else:
            audio_handler = AudioHandler(audio_name=artist_id, audio_extension='mp3', category='artists', state='raw', config=config)
            audio_handler.download_youtube_mp3()


if __name__ == "__main__":
    main()
