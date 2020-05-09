import pandas as pd
import folium

from input_factories.data_factory.datasets.localizations import Localizations
from input_factories.data_factory.datasets.artists import Artists
from input_factories.data_factory.datasets.scientists import Scientists
from input_factories.data_factory.gold_data_builder import GoldDataBuilder
from modules.config.configuration import Configuration
from map_viz.map_vizualizer import MapVizualizer


def main():
    config = Configuration()
    localizations = Localizations("clean", config)
    scientists = Scientists("clean", config)
    artists = Artists("clean", config)

    gold_data_builder = GoldDataBuilder(artists, localizations, config)
    # gold_data_builder = GoldDataBuilder(scientists, localizations, config)

    gold_data_builder.add_locations()
    gold_data_builder.located_data = gold_data_builder.located_data.drop_duplicates()

    map_viz = MapVizualizer(gold_data_builder, config)
    map_viz.create_map(grouping_feature='birth_half_decade')
    map_viz.save_map('/home/agnusfabien/Bureau/map.html')

if __name__ == "__main__":
    main()
    