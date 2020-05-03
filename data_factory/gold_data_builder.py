""""""

from data_factory.datasets.dataset import Dataset
from data_factory.datasets.localizations import Localizations
from modules.config.configuration import Configuration



class GoldDataBuilder(object):
    """
    """
    def __init__(self, subject_data: Dataset, localizations: Localizations, config: Configuration):
        self.subject_data = subject_data
        self.localizations = localizations
        self._config = config
    
    def add_locations(self):
        located_data = self.subject_data.data.merge(
            self.localizations.data,
            left_on=self.subject_data.place_col,
            right_on=self.localizations.place_col,
            how='left'
        )
        self.located_data = located_data