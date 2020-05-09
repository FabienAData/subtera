""""
Tools to produce HTML code as strings.
They will be displayed as popups of a network vizualization.
"""


node_label_template_head = \
  """<head>
<style>
artist_name {
font-family: 'proxima_nova_rgbold', Helvetica, Arial, sans-serif;
font-size: 1.8em;
}
</style>
</head>"""


def get_node_label_template(
    artist_name: str,
    node_label_template_head: str = node_label_template_head
) -> str:
    node_label_template = f"""
<html>
{node_label_template_head}
<body>

<artist_name>{artist_name}</artist_name>

</body>
</html>
"""
    return node_label_template
