""""""
import os
import folium
from folium import LayerControl
from folium.plugins import MarkerCluster, FeatureGroupSubGroup

import branca
import base64
import re

from modules.config.configuration import Configuration
from data_factory.gold_data_builder import GoldDataBuilder
from image_factory.image_handler import ImageHandler

class MapVizualizer():
    """"""
    def __init__(self, gold_data_builder: GoldDataBuilder, config: Configuration):
        self.gold_data_builder = gold_data_builder
        self._config = config
        self.folium_map = None
    
    def create_map(self, grouping_feature: str):
        map_center_coord = (27.374017, -42.144164)
        m = folium.Map(
            location=map_center_coord,
            zoom_start=3
        )
        tooltip = 'Clique !'

        data = self.gold_data_builder.located_data
        data[grouping_feature] = data[grouping_feature].fillna("Non renseigné")
        ordered_grouping_unique_values = set(data[grouping_feature].values)

        m_cluster = MarkerCluster(control=False)
        m.add_child(m_cluster)
        for grouping_value in ordered_grouping_unique_values:
            folium_sub_group = FeatureGroupSubGroup(m_cluster, str(grouping_value))
            m.add_child(folium_sub_group)
            sub_data = data[data[grouping_feature] == grouping_value]
            for _,values in sub_data.iterrows():
                name = values['name']
                id = str(values['artist_id'])
                living_dates = ' - '.join([str(values["birth_date"]), str(values["death_date"])]) 
                place = values['birth_place']
                bio = values['biography']
                resized_images_folder = os.path.join(
                    self._config.processed_images_path, 'resized'
                )
                img_html_tag = ''
                for img_file in os.listdir(resized_images_folder):
                    if id in img_file:
                        img_handler = ImageHandler(img_file, 'resized', self._config)
                        decoded_image = img_handler.get_decoded_base64_png()
                        img_extension = re.sub(rf'{id}\.', '', img_file)
                        img_html_tag = f'<img src="data:image/{img_extension};base64,{decoded_image}">'


                audio_path = "/home/agnusfabien/Bureau/Personnel/Projets/projekto/eminem_64.mp3"

                encoded_audio = base64.b64encode(open(audio_path, 'rb').read())
                decoded_audio = encoded_audio.decode('UTF-8')
                html = f"""
                <html>
                <body>
                <b>{name}</b>({living_dates})<br>Lieu : {place}
                <br><br>
                {img_html_tag}
                <br><br>
                <audio controls>
                <source src="data:audio/mp3;base64, {decoded_audio}"></audio>

                </body>
                </html>
                """
                iframe = branca.element.IFrame(html=html, width=500, height=300)
                popup = folium.Popup(iframe, max_width=2650)

                coord = [values['lat'], values['lng']]
                marker = folium.Marker(coord, popup=popup, tooltip=tooltip)
                folium_sub_group.add_child(marker)

        l = folium.LayerControl().add_to(m)
        self.map = m

    def save_map(self, path: str):
        self.map.save(path)
