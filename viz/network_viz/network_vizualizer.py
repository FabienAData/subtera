import os
from typing import Any, Dict, Optional

import pandas as pd
import pyvis
from pyvis.network import Network
import networkx as nx

from input_factories.audio_factory.audio_handler import AudioHandler
from input_factories.image_factory.image_handler import ImageHandler
from modules.config.configuration import Configuration
from viz.network_viz.popup_templates import get_edge_popup_template, get_node_popup_template


class NetworkVizualizer(object):
    def __init__(
        self,
        data: pd.DataFrame,
        source_col: str,
        target_col: str,
        edge_title_col: str,
        edge_sub_title_col: str,
        nodes_titles_dict: Dict,
        nodes_categories_dict: Dict,
        categories_color_dict: Dict,
        config: Configuration,
        edge_audio_category: Optional[str] = None,
        height: str = '750px',
        width: str = '100%',
        bg_color: str = '#222222',
        font_color: str = 'white'
    ) -> None:
        self.data = data
        self.source_col = source_col
        self.target_col = target_col
        self.edge_title_col = edge_title_col
        self.edge_sub_title_col = edge_sub_title_col
        self.nodes_titles_dict = nodes_titles_dict
        self.nodes_categories_dict = nodes_categories_dict
        self.categories_color_dict = categories_color_dict
        self._config = config
        self.edge_audio_category = edge_audio_category
        self.height = height
        self.width = width
        self.bg_color = bg_color
        self.font_color = font_color
        self.net_viz = None

    def create_net_viz(self):
        net_viz = Network(
            height=self.height,
            width=self.width,
            bgcolor=self.bg_color,
            font_color=self.font_color)
        net_viz.barnes_hut()
        for _,values in self.data.iterrows():
            source = str(self.nodes_titles_dict.get(values[self.source_col]))
            source_image_path = ImageHandler(
                values[self.source_col],
                'png',
                'circled',
                self._config).image_path
            target = str(self.nodes_titles_dict.get(values[self.target_col]))
            target_image_path = ImageHandler(
                values[self.target_col],
                'png',
                'circled',
                self._config).image_path
            source_node_color = self._get_node_color(values[self.source_col])
            target_node_color = self._get_node_color(values[self.target_col])
            edge_color = get_edge_color(source_node_color, target_node_color)
            edge_title = values[self.edge_title_col]
            edge_sub_title = values[self.edge_sub_title_col]
            weight = 4
            net_viz.add_node(
                source,
                label=source,
                title=get_node_popup_template(source),
                color=source_node_color,
                shape='image',
                image=source_image_path
            )
            net_viz.add_node(
                target,
                label=target,
                title=get_node_popup_template(target),
                color=target_node_color,
                shape='image',
                image=target_image_path
            )
            edge_audio_html_tag = self._get_edge_audio_html_tag(
                edge_title, edge_sub_title
            )

            net_viz.add_edge(
                source,
                target,
                title=get_edge_popup_template(edge_title, edge_sub_title, edge_audio_html_tag),
                value=weight,
                color=edge_color
            )
        add_node_values(net_viz)
        self.net_viz = net_viz
    
    def _get_node_color(self, node_value: Any) -> str:
        node_color = 'white'
        node_category = self.nodes_categories_dict.get(node_value)
        if node_category is not None:
            color_candidate = self.categories_color_dict.get(node_category)
            if color_candidate is not None:
                node_color = color_candidate
        return node_color

    def _get_edge_audio_html_tag(self, edge_title: Any, edge_sub_title: Any) -> str:
        audio_html_tag = ''
        if self.edge_audio_category is not None:
            audios_folder_path = os.path.join(self._config.processed_audios_path, self.edge_audio_category)
            for audio_file in os.listdir(audios_folder_path):
                if audio_file == '.'.join([edge_title, 'mp3']):
                    audio_handler = AudioHandler(edge_title, 'mp3', self.edge_audio_category, 'processed', self._config)
                    decoded_audio = audio_handler.get_decoded_base64_str()
                    audio_html_tag = f'<audio controls autoplay><source src="data:audio/mp3;base64,{decoded_audio}"></audio>'
        return audio_html_tag

    def show(self):
        self.net_viz.show("/home/agnusfabien/Bureau/network.html")


def get_edge_color(source_node_color: str, target_node_color: str):
    edge_color = 'white'
    if source_node_color == target_node_color:
        edge_color = source_node_color
    return edge_color

def add_node_values(net_viz: pyvis.network.Network) -> None:
    neighbor_map = net_viz.get_adj_list()
    for node in net_viz.nodes:
        node["value"] = len(neighbor_map[node["id"]])
