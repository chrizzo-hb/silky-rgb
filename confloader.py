import os
import re

from colors import PALETTES, get_palette
from effects.effect_store import MODES

CONFIG = {
    "fps": 30,
    "mode": "shimmer",
    "brightness": 7,
    "brightness.adaptive": False,
    "palette": "Knulli",
    "palette.swap": False,
    "palette.secondary": False
}

conf_map = {
    "mode": {
        "type": "string",
        "available": True
    },
    "brightness": {
        "type": "int",
        "range": [0,10],
        "available": True
    },
    "brightness.adaptive": {
        "type": "bool",
        "available": True
    },
    "palette": {
        "type": "string",
        "available": True
    }
}

for k in conf_map:
    conf_map[k]["value"] = CONFIG[k]

def get_param(key):
    ret = os.popen('knulli-settings-get '+"led."+key).read().strip()
    print('read knulli option:', key, '| val:', ret)
    return ret

def reload():
    for k in conf_map:
        set_option(k, get_param(k))

def set_option(key:str, val:str):
    try:
        if key == "mode":
            if val in MODES:
                CONFIG["mode"] = val

        if key == "palette":
            if val in PALETTES:
                CONFIG["palette"] = val

        if key == "brightness":
            if val.isnumeric():
                CONFIG["brightness"] = int(val)

        if key == "brightness.adaptive":
            CONFIG['adaptive_brightness'] = val == '1'

    except:
        pass
