import os
import re

from colors import get_palette

CONFIG = {
    "fps": 30,
    "mode": "null",
    "brightness": 100,
    "adaptive_brightness": False,
    "palette": [[0, 0, 0], [0, 0, 0]],
    "palette_swap": False,
    "palette_swap_secondary": False,
    "speed": 0
}

palettes = {
    # Warm & Fiery
    'Flame': ['Red', 'Orange'],
    'Sunset': ['Hot Pink', 'Tangerine'],
    'Volcano': ['PRed', 'Black'],
    'Crimson Gold': ['Crimson', 'Gold'],
    'Golden Hour': ['Goldenrod', 'Warm White'],
    #probably merge flame and crimson gold

    # Cool & Serene
    'Ocean Deep': ['Blue', 'Teal'],
    'Glacier': ['White', 'Cyan'],
    'Amethyst Haze': ['Amethyst', 'Deep Purple'], # small diff
    'Lagoon': ['Turquoise', 'Spring Green'],
    'Night Sky': ['PBlue', 'Silver'], #cool dark palette

    # Vibrant & Electric
    'Cyberpunk': ['Magenta', 'Cyan'],
    'Synthwave': ['Electric Blue', 'Hot Pink'],
    'Matrix': ['Lime Green', 'Black'],
    'Fuchsia Flash': ['Fuchsia', 'Electric Blue'], #probably redundant
    'Scarlet Surge': ['Scarlet', 'Aqua'],

    # Natural & Earthy
    'Forest': ['Green', 'Emerald'],
    'Spring Meadow': ['Spring Green', 'Yellow'],
    'Mint Chip': ['Mint', 'Silver'],
    'Orchid': ['Magenta', 'Violet'],
    
    # Fun & Sweet
    'Cotton Candy': ['Pink', 'Sky Blue'],
    'Lemon Lime': ['Lime Green', 'Yellow'], #basically spling meadow
    'Bubblegum': ['Pink', 'Aqua'], # there are a few like this
    'Tangerine Dream': ['Tangerine', 'White'],
    
    # Regal & Rich
    'Royalty': ['Violet', 'Gold'],
    'Emerald City': ['Emerald', 'Goldenrod'],
    'Prestige': ['Deep Purple', 'Silver']
}

KEY_LED_MODE="led.mode"
KEY_LED_BRIGHTNESS="led.brightness"
KEY_LED_BRIGHTNESS_ADAPTIVE="led.brightness.adaptive"
KEY_LED_SPEED="led.speed"
KEY_LED_COLOUR="led.colour"
KEY_LED_COLOUR_RIGHT="led.colour.right"
KEY_LED_BATTERY_LOW_THRESHOLD="led.battery.low"
KEY_LED_BATTERY_CHARGING_ENABLED="led.battery.charging"

mode_map = {
    '0' : 'null',
    '1' : 'framebuffer',
    '2' : 'shimmer',
    '3' : 'input_fade',
    '4' : 'wave',
    '5' : 'rainbow',
    '6' : 'static'
}

def identify_device():
    board = ""

    try:
        with open('/boot/boot/batocera.board', 'r') as f:
            board = f.read().strip()
    except (IOError, FileNotFoundError):
        pass

    return board

def get_param(key):
    ret = os.popen('batocera-settings-get '+key).read().strip()
    print('read knulli option:', key, '| val:', ret)
    return ret

def refresh(key:str|None=None):
    try:
        if key is None or key == KEY_LED_MODE:
            val = get_param(KEY_LED_MODE)
            CONFIG['mode'] = mode_map[val]

        if key is None or key == KEY_LED_BRIGHTNESS_ADAPTIVE:
            val = get_param(KEY_LED_BRIGHTNESS_ADAPTIVE)
            CONFIG['adaptive_brightness'] = val == '1'

        if key is None or key == KEY_LED_BATTERY_CHARGING_ENABLED:
            val = get_param(KEY_LED_BATTERY_CHARGING_ENABLED)
            CONFIG['charging_notification'] = val == '1'
        
        if key is None or key == KEY_LED_BRIGHTNESS:
            val = get_param(KEY_LED_BRIGHTNESS)
            CONFIG['brightness'] = 40 + int(int(val) * 0.6)
        
        if key is None or key == KEY_LED_COLOUR:
            val1, val2, val3 = [int(x) for x in get_param(KEY_LED_COLOUR).split()]
            sp = palettes[list(palettes.keys())[(val1//10)%len(palettes)]]
            CONFIG['palette'] = get_palette('-'.join(sp))
            CONFIG['palette_swap'] = val2 > 0
            CONFIG['palette_swap_secondary'] = val3 > 0
    except:
        pass
