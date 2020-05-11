from typing import Optional
from input_factories.data_factory.datasets.dataset import Dataset
from modules.config.configuration import Configuration
from modules.data_factory.clean import convert_to_datetime, group_years


class Artists(Dataset):

    def __init__(self, state: Optional[str], config: Configuration) -> None:
        """
        Initialize the Artists class.

        Parameters
        ----------
        state : Optional[str]
            Optional string corresponding to the state of the data.
        config : Configuration
            Configuration used to get the paths.
        """
        super().__init__("artists", state, config)
        self.place_col = "birth_place"

    def clean(self) -> None:
        """
        Clean DataFrame if _state == "raw" and change _state to "clean".
        """
        if self._state == 'raw':
            self._clean_column_names()
            self.data['birth_date'] = convert_to_datetime(self.data['birth_date'])
            self.data['death_date'] = convert_to_datetime(self.data['death_date'])
            self.data['birth_year'] = self.data['birth_date'].dt.year
            self.data['birth_half_decade'] = self.data['birth_year'].apply(
                lambda x: group_years(x, 5)
                )
            
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'
    
    def keep_only_youtube_urls(self) -> None:
        """
        """
        self.data = self.data[['artist_id', 'youtube_url']]
        self.data = self.data[self.data['youtube_url'].notnull()]


def main():
    config = Configuration()
    dataset = Artists('raw', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)
    dataset.keep_only_youtube_urls()
    dataset.save('youtube_urls', overwrite=True)

if __name__ == '__main__':
    main()
