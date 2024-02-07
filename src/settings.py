import json

width = 1600
height = 900

launcher_width = 1000
launcher_height = 600

# FUNCTIONS #

# -------- COLOUR SCHEME FUNCTIONS -------- #

def hex_to_rgb(hex):
    return tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

rgb_to_hex = lambda rgb: '#{0:02x}{1:02x}{2:02x}'.format(rgb[0], rgb[1], rgb[2])

def lighten_color(hex_color, factor=0.25):
    rgb_color = hex_to_rgb(hex_color)
    lighter_rgb = tuple(int((255 - val) * factor + val) for val in rgb_color)
    return rgb_to_hex(lighter_rgb)

def darken_color(hex_color, factor=0.25):
    rgb_color = hex_to_rgb(hex_color)
    darker_rgb = tuple(int(val * (1 - factor)) for val in rgb_color)
    return rgb_to_hex(darker_rgb)


# COLOURS #

active_theme_type = 'dark'
active_light_theme = 'example-light-theme'
active_dark_theme = 'example-dark-theme'

with open('themes.json', 'r') as file:
    themes_data = json.load(file)
    
    match active_theme_type:
        case 'light':
            theme = themes_data["light"][f"{active_light_theme}"]
        case 'dark':
            theme = themes_data["dark"][f"{active_dark_theme}"]

    primary = theme['primary']
    secondary = theme['secondary']
    accent1 = theme['accent1']
    accent2 = theme['accent2']
    spare = theme['spare']
    
    primary_light = lighten_color(primary)
    secondary_light = lighten_color(secondary)
    accent1_light = lighten_color(accent1)
    accent2_light = lighten_color(accent2)
    print(primary, secondary, accent1, accent2, spare)

    primary_dark = darken_color(primary)
    secondary_dark = darken_color(secondary)
    accent1_dark = darken_color(accent1)
    accent2_dark = darken_color(accent2)

# NOTES #

#https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
#https://github.com/TomSchimansky/CustomTkinter/issues/93