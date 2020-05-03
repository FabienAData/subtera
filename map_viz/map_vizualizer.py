""""""
import folium
from folium.plugins import MarkerCluster

import branca

from data_factory.gold_data_builder import GoldDataBuilder

class MapVizualizer():
    """"""
    def __init__(self, gold_data_builder: GoldDataBuilder):
        self.gold_data_builder = gold_data_builder
        
        self.folium_map = None
    
    def create_map(self):
        data = self.gold_data_builder.located_data
        map_center_coord = (27.374017, -42.144164)
        m = folium.Map(
            location=map_center_coord,
            zoom_start=3
        )
        tooltip = 'Clique !'
        m_cluster = MarkerCluster()
        for _,values in data.iterrows():
            name = values['name']
            living_dates = ' - '.join([str(values["birth_date"]), str(values["death_date"])]) 
            place = values['birth_place']
            bio = values['biography']
            html = f'<b>{name}</b> ({living_dates})<br>Lieu : {place}<br><br>{bio}'


            iframe = branca.element.IFrame(html=html, width=500, height=300)
            popup = folium.Popup(iframe, max_width=2650)
            
            coord = [values['lat'], values['lng']]
            marker = folium.Marker(coord, popup=popup, tooltip=tooltip)
            m_cluster.add_child(marker)
        m.add_child(m_cluster)
        self.map = m

    def save_map(self, path: str):
        self.map.save(path) 
