"""
Customized exceptions class.
All those classes are daughter classes of BaseException class.
"""

from typing import Optional
import re


class MissingConfigKeyException(BaseException):
    """
    Exception raised when a missing key is called from a section of a
    configuration file.

    By defaut, print the message:  "No '{missing_key}' key in {path_config_file} config file."
    As options, add the section of the config file with the missing
    key or/and any additional message to the default message.
    The resulting message will be:
      "No '{missing_key}' key in {path_config_file} config file ({config_section} section).\n{additional_message}"

    Parameters
    ----------
    missing_key: str
        missing key
    path_config_file: str
        path to the config file
    config_section: Optional[str] = None
        section of the config file with the missing key.
        If not None, add the section to the default exception message.
    additional_message: Optional[str] = None
        If not None, add the additional message to the default exception message.

    """
    def __init__(
        self,
        missing_key: str,
        path_config_file: str,
        config_section: Optional[str] = None,
        additional_message: Optional[str] = None
            ) -> None:
        self.message = self._format_message(
            missing_key, path_config_file, config_section, additional_message
            )

    def _format_message(
        self,
        missing_key: str,
        path_config_file: str,
        config_section: Optional[str] = None,
        additional_message: Optional[str] = None
            ) -> str:
        """
        Build the message string from the config file values.
        Include optional values if needed.
        """
        mes = f"No '{missing_key}' key in {path_config_file} config file."
        if config_section:
            mes = re.sub(r".$", f" ('{config_section}' section).", mes)
        if additional_message:
            mes = "\n".join([mes, additional_message])
        return mes

    def __str__(self):
        return self.message
