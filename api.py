from bottle import run, route, get, request
from colors import BLUE, GREEN, PALETTES, RED, Palette
from confloader import CONFIG, conf_map, reload, set_option
from effects.effect_store import MODES
from state import RGBState, Event, EventType
from utilities import hex_to_rgb
from copy import deepcopy
from json import dumps

STATE = RGBState.get()

presets = {
    'battery_charging': [
        Event(EventType.Notification, 'up', 3, GREEN),
    ],
    'battery_full': [
        Event(EventType.Notification, 'up', 1, GREEN),
        Event(EventType.Notification, 'round', 1, GREEN),
        Event(EventType.Notification, 'blink_off', 1, GREEN),
    ],
    'battery_low': [
        Event(EventType.Notification, 'blink', 3, RED),
    ],
    'cheevo': [
        Event(EventType.Notification, 'cheevo', 1),
    ]
}

def run_preset_effect(preset):
    STATE.events.append(Event(EventType.FadeOut))
    for e in preset:
        STATE.events.append(deepcopy(e))
    STATE.events.append(Event(EventType.FadeIn))

@route("/reload-config")
def reload():
    reload()
    STATE.events.append(Event(EventType.LoadConfig))
    return ""

@route("/set-config", method='POST')
def set_config():
    req = request.body.read().decode().split() # pyright: ignore[reportAttributeAccessIssue]
    set_option(req[0], req[1])
    STATE.events.append(Event(EventType.LoadConfig))
    return f"[{req[0]}]: {req[1]}\n"

@route("/animation", method='POST')
def animation():
    req = request.body.read().decode() # pyright: ignore[reportAttributeAccessIssue]
    if req == 'charging':
        run_preset_effect(presets['battery_charging'])
    elif req == 'cheevo':
        run_preset_effect(presets['cheevo'])
    elif req == 'battery_low':
        run_preset_effect(presets['battery_low'])
    elif req == 'battery_full':
        run_preset_effect(presets['battery_full'])
    else:
        req_ = req.split()
        try:
            if len(req_):
                STATE.events.append(Event(EventType.FadeOut))
        except Exception as e:
            return "Error while processing Command:\n[name] [count] [hex_color]\n"
    return ""


@route("/update-battery-state", method='POST')
def battery():
    req = request.body.read().decode().split() # pyright: ignore[reportAttributeAccessIssue]
    STATE.DEV.BATTERY['percentage'] = int(req[0])

    last_state = STATE.DEV.BATTERY['state']

    if not CONFIG['charging_notification']: # notification mode
        if req[1] != last_state and req[1] == 'Charging':
            run_preset_effect(presets['battery_charging'])
        if req[1] != last_state and req[1] == 'Full':
            run_preset_effect(presets['battery_full'])
        if req[1] != last_state:
            STATE.events.append(Event(EventType.RemoveLayer, 'charging'))
    else:
        if req[1] != last_state:
            if req[1] == 'Charging':
                STATE.events.append(Event(EventType.AddLayer, 'charging'))
            else:
                STATE.events.append(Event(EventType.RemoveLayer, 'charging'))

    STATE.DEV.BATTERY['state'] = req[1]

@route("/update-screen-state", method='POST')
def screen():
    req = request.body.read().decode() # pyright: ignore[reportAttributeAccessIssue]

    if CONFIG['adaptive_brightness']:
        if(STATE._target_sc != int(req)):
            STATE._target_sc = int(req)
            STATE.DEV.nuke_savestates()
            STATE._idle = False

@get("/kill")
def kill():
    STATE.events.append(Event(EventType.FadeOut))
    STATE.events.append(Event(EventType.Die))

@get("/get-settings")
def settings():
    return dumps(conf_map, indent=4)+"\n"

@get("/get-modes")
def get_modes():
    m = {}
    for k, v in MODES.items():
        m[k] = {
            "name": v["metadata"]["name"]
        }
    return dumps(m, indent=4)+"\n"

@get("/get-palettes")
def get_palettes():
    p = {}
    for k, v1 in PALETTES.items():
        p[k] = {
            "name": f"{k} ({v1[0]}-{v1[1]})"
        }

    return dumps(p, indent=4)+"\n"

def run_api():
    run(host='localhost', port=1235)

if __name__ == '__main__':
    run_api()