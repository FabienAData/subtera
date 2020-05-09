from typing import Optional
from input_factories.data_factory.datasets.dataset import Dataset
from input_factories.data_factory.datasets.artists import Artists
from modules.config.configuration import Configuration
from modules.data_factory.clean import convert_to_datetime, group_years


class Albums(Dataset):

    def __init__(self, state: Optional[str], config: Configuration) -> None:
        """
        Initialize the Albums class.

        Parameters
        ----------
        state : Optional[str]
            Optional string corresponding to the state of the data.
        config : Configuration
            Configuration used to get the paths.
        """
        super().__init__("albums", state, config)

    def clean(self) -> None:
        """
        Clean DataFrame if _state == "raw" and change _state to "clean".
        """
        if self._state == 'raw':
            self._clean_column_names()
            self.data xxx
            self.data['birth_date'] = convert_to_datetime(self.data['birth_date'])
            self.data['death_date'] = convert_to_datetime(self.data['death_date'])
            self.data['birth_year'] = self.data['birth_date'].dt.year
            self.data['birth_half_decade'] = self.data['birth_year'].apply(
                lambda x: group_years(x, 5)
                )
            
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'


def main():
    config = Configuration()
    dataset = Albums('raw', config)
    dataset = Albums('clean', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)

if __name__ == '__main__':
    main()
