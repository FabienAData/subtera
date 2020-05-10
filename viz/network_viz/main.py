import pandas as pd
from pyvis.network import Network
import networkx as nx

from typing import Dict

from viz.network_viz.network_vizualizer import NetworkVizualizer
from modules.config.configuration import Configuration
from input_factories.data_factory.datasets.artists import Artists


def main():
    config = Configuration()
    artists_data = Artists('clean', config).data
    nodes_titles_dict = {i:j for i,j in artists_data[['artist_id', 'name']].values}
    nodes_categories_dict = {i:j for i,j in artists_data[['artist_id', 'category']].values}
    categories_color_dict = {
        'Rap / R’N’B / Hip-Hop International': '#183BA0', # dark blue
        'Rap / R’N’B/ Hip Hop France': '#4BD6CB', # light blue
        'Variété Française + 20’s – 70’s': '#E2E34D', # dark yellow
        'Variété Française +80’s – 2010’s' : '#EA842D' # orange
    }
    data = pd.read_csv("/home/agnusfabien/Bureau/Personnel/Projets/projekto/data/raw/network_feat_songs.csv")

    net_vizualzier = NetworkVizualizer(
        data,
        'artist_start',
        'artist_end',
        'value',
        nodes_titles_dict,
        nodes_categories_dict,
        categories_color_dict,
        config
    )
    net_vizualzier.create_net_viz()
    net_vizualzier.show()

if __name__ == "__main__":
    main()





