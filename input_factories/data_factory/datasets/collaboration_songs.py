from typing import Optional
from input_factories.data_factory.datasets.dataset import Dataset
from modules.config.configuration import Configuration
from modules.data_factory.clean import convert_to_datetime, group_years


class CollaborationSongs(Dataset):

    def __init__(self, state: Optional[str], config: Configuration) -> None:
        """
        Initialize the CollaborationSongs class.

        Parameters
        ----------
        state : Optional[str]
            Optional string corresponding to the state of the data.
        config : Configuration
            Configuration used to get the paths.
        """
        super().__init__('collaboration_songs', state, config)

    def clean(self) -> None:
        """
        Clean DataFrame if _state == "raw" and change _state to "clean".
        """
        if self._state == 'raw':
            self._clean_column_names()
            
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'
    
    def keep_only_youtube_urls(self) -> None:
        """
        """
        self.data = self.data[['song_name', 'youtube_url']]
        self.data = self.data[self.data['youtube_url'].notnull()]


def main():
    config = Configuration()
    dataset = CollaborationSongs('raw', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)
    dataset.keep_only_youtube_urls()
    dataset.save('youtube_urls', overwrite=True)

if __name__ == '__main__':
    main()
