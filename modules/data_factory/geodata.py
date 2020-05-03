"""
Tools for geographic data processing
"""

from typing import List
import pandas as pd
import requests

import re


def get_maps_api_url(place: str, api_key: str) -> str:
    """
    Transform a `place` string to the corresponding url to request to geolocate it
    with the  Google Maps geocode API.
    1. Replace spaces by "+"
    2. Include the resulting string in the corresponding url to request
    """
    place = re.sub(' ', '+', place)
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}'
    return url

def get_lat_lng(url: str, api_key: str) -> List[float]:
    """
    Request Google Maps geocode API to get latitude and longitude of an `url`
    """
    response = requests.get(url).json()
    lat = response['results'][0]['geometry']['location']['lat']
    lng = response['results'][0]['geometry']['location']['lng']
    return [lat, lng]

def get_geolocalized_df(df: pd.DataFrame, place_col: str, api_key: str) -> pd.DataFrame:
    """
    Add "lat" and "lng" columns to `df`, respectively for the latitude and the longitude of
    `place_col` column values.
    Those coordinates are requested to Google Maps geocode API.
    
    Return the updated pd.DataFrame.
    """
    urls_to_request = df[place_col].apply(lambda place: get_maps_api_url(place, api_key))
    df["lat"], df["lng"] = zip(*urls_to_request.apply(lambda url: get_lat_lng(url, api_key)))
    return df
    