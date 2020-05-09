

html_head = """
<head>
<style>
    .container-element {
    width:600px;
    }

    .image-element,
    .text-element {
    display:inline-block;
    vertical-align:bottom;
    }

    .image-element {
    width:200px;
    }

    .text-element {
    text-align:right;
    width:300px;
    }

    .artist_name {
    font-family: 'proxima_nova_rgbold', Helvetica, Arial, sans-serif;
    font-size: 1.3em;
    }

    .artist_birth {
    font-family: 'FF Meta VF', 'Fira Sans', Helvetica, Arial, sans-serif;
    font-size: 0.9em;
    }

    }

</style>
</head>
"""

def get_html_artist_pop_up(
    img_html_tag: str,
    name: str,
    birth_date_and_place: str,
    audio_html_tag: str
    ) -> str:
    html = f"""
<html>
{html_head}
<body>
<div class="container-element">
  <div class="image-element">
    {img_html_tag}
  </div>
  <div class="text-element">
  <div class="artist_name">
        {name}
    </div>
    <div class="artist_birth">
        {birth_date_and_place}
    </div>
  </div>
</div>
<br>
{audio_html_tag}
</body>
</html>
"""
    return html



    
