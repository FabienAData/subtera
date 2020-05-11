""""
Tools to produce HTML code as strings.
They will be displayed as popups of a network vizualization.
"""


node_popup_template_head = \
  """<head>
<style>
node_label {
background-color: white;
font-family: 'proxima_nova_rgbold', Helvetica, Arial, sans-serif;
font-size: 1.2em;
}
</style>
</head>"""


def get_node_popup_template(
    node_label: str,
    node_popup_template_head: str = node_popup_template_head
) -> str:
    node_popup_template = f"""
<html>
{node_popup_template_head}
<body>

<node_label>{node_label}</node_label>

</body>
</html>
"""
    return node_popup_template


edge_popup_template_head = \
  """<head>
<style>
edge_title {
background-color: white;
font-family: 'proxima_nova_rgbold', Helvetica, Arial, sans-serif;
font-size: 1.2em;
}
edge_sub_title {
background-color: white;
font-family: 'FF Meta VF', 'Fira Sans', Helvetica, Arial, sans-serif;
font-size: 0.8em;
}
</style>
</head>"""


def get_edge_popup_template(
    edge_title: str,
    edge_sub_title: str,
    edge_audio_html_tag: str,
    edge_popup_template_head: str = edge_popup_template_head
) -> str:
    edge_popup_template = f"""
<html>
{edge_popup_template_head}
<body>

<edge_title>{edge_title}</edge_title>
<br>
<edge_sub_title>{edge_sub_title}</edge_sub_title>
<br>
{edge_audio_html_tag}

</body>
</html>
"""
    return edge_popup_template
