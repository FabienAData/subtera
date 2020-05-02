from typing import Optional
from data_factory.datasets.dataset import Dataset
from modules.config.configuration import Configuration
from modules.data_factory.clean import clean_df_column_names


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
        super().__init__("activities", state, config)

    def clean(self) -> None:
        """
        Clean DataFrame if _state == "raw" and change _state to "clean".
        """
        if self._state == 'raw':
            self.data.columns = clean_df_column_names(self.data.columns)
        else:
            raise Exception("Initial state is not raw")
        self._state = 'clean'


def main():
    config = Configuration()
    dataset = Localizations('raw', config)
    dataset.clean()
    dataset.save('clean', overwrite=True)


if __name__ == '__main__':
    main()
