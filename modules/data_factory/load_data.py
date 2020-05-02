"""
Module with tools used by data_factory module to load data.
"""
import os
import re
import logging
import warnings

from typing import Any, Callable, Tuple, Union
import pandas as pd
import geopandas as gpd
from tqdm import tqdm


def _is_folder(data_path: str) -> bool:
    """
    Investigate if a `data_path` accounts for a folder or not.

    Parameters
    ----------
        data_path: str
            Path to investigate.

    Returns
    -------
        bool: True if `data_path` accounts for a folder. False otherwise.
    """
    is_folder = True
    try:
        os.listdir(data_path)
    except NotADirectoryError:
        is_folder = False
    return is_folder


def _spread_loading_on_folder(
    loading_func: Callable,
    data_path: str,
    files_extensions: Union[str, Tuple[str]],
    **kwargs: Any
    ) -> pd.DataFrame:
    """
    Given a folder, load all of its files which extensions are
    among `files_extensions`.
    Sort files by name and concatenate them as a pandas DataFrame
    and reset the index.

    Parameters
    ----------
        loading_func: Callable
            Loading function applied on each file.
            All files are loaded with the same function.
        data_path: str
            Path to the folder.
        files_extensions: Union[str, Tuple[str]]
            Only the files with extensions among `files_extensions`
            are loaded.

    Returns
    -------
    pd.DataFrame
        Ordered concatenation of data from each file.
        The index is reset.
        Files are sorted by name.
    """
    df_list = []
    if isinstance(files_extensions, tuple):
        files_extensions = f"({'|'.join(files_extensions)})"
    files_list = sorted(os.listdir(data_path))
    for file in tqdm(files_list):
        if re.match(fr".*\.{files_extensions}$", file):
            file_path = os.path.join(data_path, file)
            df = loading_func(file_path, **kwargs)
            df["FilePath"] = file_path
            df_list.append(df)
            logging.info(file_path)
            logging.info(f"Dataframe shape: {df.shape}")
    return pd.concat(df_list, sort=False).reset_index(drop=True)


def load_one_csv(data_path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Load data from one csv file as a pd.DataFrame.
    """
    return pd.read_csv(data_path, **kwargs)


def load_csv(data_path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Load data from one csv file or multiple csv files
    from a folder, as a pd.DataFrame.
    """
    is_folder = _is_folder(data_path)
    if is_folder:
        df = _spread_loading_on_folder(
            load_one_csv,
            data_path,
            "csv",
            **kwargs
            )
    else:
        df = load_one_csv(data_path, **kwargs)
    return df


def load_one_excel(data_path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Load data from one xls or xlsx file as a pd.DataFrame.
    Catch and filter out PendingDeprecationWarning warnings.
    They are from xlrd package and doesn't impact the returned pd.DataFrame.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
        df = pd.read_excel(data_path, **kwargs)
    return df


def load_excel(data_path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Load data from one or multiple xls or xlsx files
    from a folder, as a pd.DataFrame.
    """
    is_folder = _is_folder(data_path)
    if is_folder:
        df = _spread_loading_on_folder(
            load_one_excel,
            data_path,
            ("xls", "xlsx"),
            **kwargs
            )
    else:
        df = load_one_excel(data_path, **kwargs)
    return df


def load_one_shp(data_path: str, **kwargs: Any) -> pd.DataFrame:
    """
    Load data from one shp file as a gpd.GeoDataFrame.
    """
    return gpd.read_file(data_path, **kwargs)


FILE_TYPE_LOAD_FUNCTION_MAPPING = {
    "csv": load_csv,
    "excel": load_excel,
    "shp": load_one_shp,
}


def load_raw_data(
    raw_data_path: str, file_type: str, **kwargs: Any
    ) -> pd.DataFrame:
    """
    Load data from one file or one folder and return it as a pd.DataFrame.
        - Load only file(s) with a specific type.
        - The type must be among "FILE_TYPE_LOAD_FUNCTION_MAPPING" dictionary keys.
        - If data are loaded from a folder, load all the type specific files,
            ordered by name, and concatenate them. Reset the index.

    Use a loading function specific to the file(s) type.
    Map the file type with the specific loading function through the
    "FILE_TYPE_LOAD_FUNCTION_MAPPING" dictionary of this module.

    Parameters
    ----------
        raw_data_path: str
            Path to the file(s) to load. If it is a file, load the file.
            If it is a folder, load each files of the folder and return
            the pd.DataFrame of their concatenation (ordered by files name).
        file_type: str
            type of files to load. Must take a value among
            "FILE_TYPE_LOAD_FUNCTION_MAPPING" dictionary keys.
    """
    try:
        load_function = FILE_TYPE_LOAD_FUNCTION_MAPPING.get(file_type)
    except KeyError:
        print(
            f"Not loadable {file_type} file type.\n"
            f"Choose a value among {list(FILE_TYPE_LOAD_FUNCTION_MAPPING.keys())}."
        )
    return load_function(raw_data_path, **kwargs)
