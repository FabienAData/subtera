import pandas as pd
from typing import Optional

from input_factories.data_factory.datasets.dataset import Dataset
from input_factories.data_factory.datasets.artists import Artists
from input_factories.data_factory.datasets.scientists import Scientists
from modules.config.configuration import Configuration

from modules.data_factory.geodata import get_geolocalized_df

class Localizations(Dataset):
    def __init__(self, state: Optional[str], config: Configuration) -> None:
        """
        Initialize the Localizations class.

        Parameters
        ----------
        state : Optional[str]
            Optional string corresponding to the state of the data.
        config : Configuration
            Configuration used to get the paths.
        """
        super().__init__("localizations", state, config)
        self.api_key = self._data_config['api_key']
        self.place_col = "place"

    def clean(self) -> None:
        """
        Clean DataFrame if _state == "raw" and change _state to "clean".
        """
        if self._state == 'raw':
            self._clean_column_names()
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'

    def add_new_places(self, dataset: Dataset) -> None:
        place_col = dataset.place_col
        localizations_place_col = self.place_col
        places = dataset.data[[place_col]]
        places = places.merge(
            self.data,
            left_on=place_col,
            right_on=localizations_place_col,
            how='left'
            )
        new_places = places.loc[places[localizations_place_col].isnull(), [place_col]]
        new_places = get_geolocalized_df(new_places, place_col, self.api_key)
        new_places = new_places.rename(columns={place_col: localizations_place_col})
        self.data = pd.concat([self.data, new_places])
        self.data = self.data.reset_index(drop=True)

def main():
    config = Configuration()
    dataset = Localizations('raw', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)
    scientists = Scientists('clean', config)
    dataset.add_new_places(scientists)
    artists = Artists('clean', config)
    dataset.add_new_places(artists)
    dataset.save('clean', overwrite=True)

if __name__ == '__main__':
    main()
