"""Mother class for other "datasets" class"""

import json
import os
import pickle
import logging

from typing import Any, Callable, Optional, Dict

from modules.config.configuration import Configuration
from modules.data_factory.clean import clean_df_column_names
from modules.data_factory.load_data import load_raw_data
from modules.exceptions.exceptions import MissingConfigKeyException


class Dataset(object):
    """
    Mother class of other "datasets" class.
    """

    def __init__(self, data_name: str, state: Optional[str], config: Configuration):
        self._data_name = data_name
        self._state = state
        self._config = config
        self._save_data_path = os.path.join(
            self._config.processed_data_path, self._data_name
        )
        self._data_config_path = os.path.join(
            self._config.application_root, "data_factory/config/data_config.json",
        )
        self._data_config = self._get_data_config()
        self.data = None
        self._raw_path = None
        self.load()

    def _get_data_config(self) -> Dict[str, Any]:
        """
        Load configuration to load and treat data sources from a .json file.

        Returns
        -------
            Dict[str, Any]
                Dictionary of arguments to load and treat data sources
        """
        with open(self._data_config_path, "r") as file:
            config_unparsed = file.read()
        config_dict = json.loads(config_unparsed)
        data_loading_config = config_dict.get(self._data_name)
        if data_loading_config is None:
            raise Exception(
                f"There is no '{self._data_name}' key in the data loading config file"
                f" ({self._data_config_path})."
            )

        return data_loading_config

    def load(self, custom_raw_data_loading_func: Optional[Callable] = None) -> None:
        """
        Load data from files and assign it to `data` attribute.
        The loading modalities must be specified in the datafactory.config.data_config.json file.

        The loading method depend on the `_state` attribute.

        Parameters
        ----------
        custom_raw_data_loading_func: Optional[Callable]
            If specified, `custom_raw_data_loading_func` is called instead of `load_raw_data`
            when `_state` attribute value is "raw".
            It can be specified in a child class.
        """
        if self._state is None:
            pass
        elif self._state == "raw":
            raw_path = self._data_config.get("raw_path")
            if raw_path:
                raw_path = os.path.join(self._config.raw_data_path, raw_path)
                raw_file_type = self._data_config.get("file_type")
                if raw_file_type:
                    if raw_file_type == "no_raw":
                        raise Exception("No raw data are available for this source. Please select another state.")
                    else:
                        raw_kwargs = self._data_config.get("kwargs")
                        if raw_kwargs is None:
                            raise MissingConfigKeyException(
                                "kwargs", self._data_config_path, config_section=self._data_name,
                                additional_message="It must exist. Its value must be the kwargs to read "
                                "the raw data file(s) or an empty dictionary if no kwargs is needed."
                                )
                        else:
                            if custom_raw_data_loading_func:
                                self.data = custom_raw_data_loading_func(raw_path, **raw_kwargs)
                            else:
                                self.data = load_raw_data(raw_path, raw_file_type, **raw_kwargs)
                else:
                    raise MissingConfigKeyException(
                        "file_type", self._data_config_path, config_section=self._data_name,
                        additional_message="It must exist and its value must be the type of raw data file(s) to load."
                        )
            else:
                raise MissingConfigKeyException(
                    "raw_path", self._data_config_path, config_section=self._data_name,
                    additional_message="It must exist and be the path to the raw data to load."
                    )
        else:
            with open(
                os.path.join(self._save_data_path, self._state + ".pickle"), "rb"
            ) as read_file:
                self.data = pickle.load(read_file)

    def save(self, state: Optional[str], overwrite: bool = False) -> None:
        """
        TODO: docstring

        :return:
        """
        file_name = os.path.join(self._save_data_path, state + ".pickle")
        if state == "raw":
            raise Exception("state must be different of raw")
        elif os.path.exists(file_name) & (not overwrite):
            raise Exception(
                f"The file {file_name} already exists but the parameter `overwrite` is set to False"
            )
        else:
            if not os.path.exists(self._save_data_path):
                os.makedirs(self._save_data_path)
            with open(file_name, "wb") as written_file:
                pickle.dump(self.data, written_file)
            self._state = state

    def clean(self):
        """
        This base class method should never be called
        """
        raise Exception("Sub class must implement clean method")

    def _clean_column_names(self) -> None:
        """
        Clean `data` attribute columns names (for instance, remove and lower special character)
        """
        self.data.columns = clean_df_column_names(self.data.columns)

    def _keep_only_useful_columns(self) -> None:
        """
        1. Among `data` attribute columns, only keep the ones used in later feature engineering or analysis.
            The columns to keep must be set in the data config file.
        2. Log the shape of the resulting `data` attribute.
        """
        cols_to_keep = self._data_config["cols_to_keep"]
        self.data = self.data[cols_to_keep]
        self._log_shape(f"Keep only useful columns.")

    def _log_shape(self, message: Optional[str] = None):
        """
        Log the shape of the data attribute.
        """
        logging.info(f"{message}\nDataframe shape: {self.data.shape}")


if __name__ == "__main__":
    pass
