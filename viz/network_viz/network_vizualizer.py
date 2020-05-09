from typing import Dict

import pandas as pd
from pyvis.network import Network
import networkx as nx

from modules.config.configuration import Configuration
from viz.network_viz.popup_templates import get_node_label_template


class NetworkVizualizer(object):
    def __init__(
        self,
        data: pd.DataFrame,
        source_col: str,
        target_col: str,
        nodes_titles_dict: Dict,
        edges_titles_dict: Dict,
        config: Configuration,
        height: str = '750px',
        width: str = '100%',
        bg_color: str = '#222222',
        font_color: str = 'white'
    ) -> None:
        self.data = data
        self.source_col = source_col
        self.target_col = target_col
        self.nodes_titles_dict = nodes_titles_dict
        self.edges_titles_dict = edges_titles_dict
        self._config = config
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
            source = values[self.source_col]
            target = values[self.target_col]
            weight = 4
            net_viz.add_node(
                source,
                label=source,
                title=get_node_label_template(str(source))
            )
            net_viz.add_node(
                target,
                label=target,
                title=get_node_label_template(str(target))
            )
            net_viz.add_edge(
                source,
                target,
                value=5
            )
        self.net_viz = net_viz
    
    def show(self):
        self.net_viz.show("essai_perso.html")
