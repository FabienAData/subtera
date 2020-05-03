from typing import Optional
from data_factory.datasets.dataset import Dataset
from modules.config.configuration import Configuration
from modules.data_factory.clean import convert_to_datetime


class Artists(Dataset):

    def __init__(self, state: Optional[str], config: Configuration) -> None:
        """
        Initialize the Scientists class.

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
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'


def main():
    config = Configuration()
    dataset = Artists('raw', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)


if __name__ == '__main__':
    main()
