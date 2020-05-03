import pandas as pd
import re
import unicodedata
from typing import List
from pandas.core.indexes.base import Index


def _strip_accents(s: str) -> str:
    """
    Delete all accents from a string.

    Parameters
    ----------
    s : str
        String to process.

    Returns
    -------
    str
        Input string without accents.
    """
    res = unicodedata.normalize('NFD', s)
    res = ''.join((c for c in res if unicodedata.category(c) != 'Mn'))
    return res


def _special_chars_to_underscore(s: str) -> str:
    """
    Replace special characters by underscores.

    Parameters
    ----------
    s: str
        String to process.

    Returns
    -------
    str:
        Input string with special characters substituted.
    """
    special_chars = r'[\'’!@#$%^&*()\[\]{};:/<>?\\|/.:;,`~\-\_+="°]'
    s = re.sub(special_chars, '_', s)
    return s


def _space_to_underscore(s: str) -> str:
    """
    Replace spaces with underscores.

    Parameters
    ----------
    s: str
        String to process.

    Returns
    -------
    str:
        Input strings with spaces substituted.
    """
    s = re.sub(' ', '_', s)
    return s


def clean_df_column_names(columns: Index) -> List[str]:
    """
    Clean the dataframe column names by
    1. removing accents,
    2. removing special chars,
    3. replacing spaces by underscores,
    4. lowering case.

    Parameters
    ----------
        columns : Index
            Column names to clean.

    Returns
    -------
        List[str]
            List of cleaned column names.
    """
    cleaned_columns = [_strip_accents(colname) for colname in columns]
    cleaned_columns = [_special_chars_to_underscore(colname) for colname in cleaned_columns]
    cleaned_columns = [_space_to_underscore(colname) for colname in cleaned_columns]
    cleaned_columns = [re.sub(r'_+', '_', colname) for colname in cleaned_columns]
    cleaned_columns = [colname.lower() for colname in cleaned_columns]
    return cleaned_columns

def convert_to_datetime(date_serie: pd.Series, format: str = '%d/%M/%y'):
    return pd.to_datetime(date_serie,format=format, errors='ignore')