"""Defines a class for the configurations"""

import configparser
import logging
import os


class Configuration(object):
    """Instanciates objects containing configuration information and elements.
    Those elements are described in the __init__ method docstring.

    That ENV sets the paths to data and the logger settings."""

    def __init__(self) -> None:
        """Initialize the Configuration class.
        Set attributes value:
            - env (sourced from environment variable): which environment someone is in
            - conf_file_name: the path to the used .cfg file (configuration file)
            - logger: the logger that will be used
            - data_path: path to the folder containing the data
            - raw_data_path: path to the folder containing raw data
            - processed_data_path: path to the folder containing processed data
        """
        application_root = os.getenv("APPLICATION_ROOT", "")
        if not application_root:
            raise Exception("APPLICATION_ROOT environment variable is not defined.")
        self.application_root = application_root
        env = os.getenv("ENV", "")
        if not env:
            raise Exception("ENV environment variable is not defined.")
        self.env = env
        self.conf_file_name = self.env.lower() + ".cfg"
        config = self._get_config_parser(application_root)
        self.logger = self._get_logger(config)
        self.raw_data_path = self._get_raw_data_path(config)
        self.processed_data_path = self._get_processed_data_path(config)
        self.raw_images_path = self._get_raw_images_path(config)
        self.processed_images_path = self._get_processed_images_path(config)

    def _get_config_parser(self, application_root: str) -> configparser.ConfigParser:
        """
        - Source the environment variable 'APPLICATION_ROOT' value
        - Source the .cfg configuration file for a specific environment
            The .cfg file sourcing is operated with 'APPLICATION_ROOT' value injection

        :param application_root: complete path to the project root folder
        :return: config, configparser.ConfigParser
        """
        path_conf_file = os.path.join(application_root, "config", self.conf_file_name)
        config = configparser.ConfigParser({"APPLICATION_ROOT": application_root})
        config_list = config.read(path_conf_file)
        if config_list == []:
            raise Exception(
                f"{self.conf_file_name} file is not found or cannot be parsed. Path to file is: {path_conf_file}"
            )
        return config

    def _get_logger(self, config: configparser.ConfigParser) -> logging.RootLogger:
        """
        TODO: docstring
        :param config:
        :return:
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s :: %(levelname)s :: %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        log_file_path = config["LOG"]["LOG_FILE_PATH"]
        if os.path.exists(log_file_path):
            file_handler = logging.FileHandler(log_file_path, "a")
        else:
            raise Exception(f"Log file : {log_file_path} file doesn't exist.")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        if logging.FileHandler not in set(map(lambda x: type(x), logger.handlers)):
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_log_level = config["LOG"]["LOG_LEVEL"]
        if stream_log_level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            stream_handler.setLevel(stream_log_level)
        else:
            raise Exception(
                "Log level must be either 'CRITICAL', 'ERROR', 'WARNING', 'INFO' or 'DEBUG'."
            )
        stream_handler.setFormatter(formatter)
        if logging.StreamHandler not in set(map(lambda x: type(x), logger.handlers)):
            logger.addHandler(stream_handler)

        return logger

    def _get_raw_data_path(self, config: configparser.ConfigParser) -> str:
        """
        TODO: docstring
        :param config:
        :return:
        """
        raw_data_path = config["DATA"]["RAW_DATA_PATH"]
        if not os.path.exists(raw_data_path):
            raise Exception(
                f"Raw data path : {raw_data_path} folder doesn't exist."
            )

        return raw_data_path

    def _get_processed_data_path(self, config: configparser.ConfigParser) -> str:
        """
        TODO: docstring
        :param config:
        :return:
        """
        processed_data_path = config["DATA"]["PROCESSED_DATA_PATH"]
        if not os.path.exists(processed_data_path):
            raise Exception(
                f"Processed data path : {processed_data_path} folder doesn't exist."
            )
        return processed_data_path

    def _get_raw_images_path(self, config: configparser.ConfigParser) -> str:
        """
        TODO: docstring
        :param config:
        :return:
        """
        raw_images_path = config["IMAGES"]["RAW_IMAGES_PATH"]
        if not os.path.exists(raw_images_path):
            raise Exception(
                f"Raw images path : {raw_images_path} folder doesn't exist."
            )

        return raw_images_path

    def _get_processed_images_path(self, config: configparser.ConfigParser) -> str:
        """
        TODO: docstring
        :param config:
        :return:
        """
        processed_images_path = config["IMAGES"]["PROCESSED_IMAGES_PATH"]
        if not os.path.exists(processed_images_path):
            raise Exception(
                f"Processed images path : {processed_images_path} folder doesn't exist."
            )
        return processed_images_path
