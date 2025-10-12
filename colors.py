
from utilities import mix, Numeric, Color
from copy import copy

SMOOTH = 0.15

class Palette():
    def __init__(self, bg:Color, fg:Color|None=None) -> None:
        self.bg = bg
        self._bg = bg
        if fg is None:
            self.fg = bg
            self._fg = bg
        else:
            self.fg = fg
            self._fg = fg

    def __eq__(self, p2) -> bool:
        return \
            round(self.fg[0]*255) == round(p2.fg[0]*255) and \
            round(self.fg[1]*255) == round(p2.fg[1]*255) and \
            round(self.fg[2]*255) == round(p2.fg[2]*255) and \
            round(self.bg[0]*255) == round(p2.bg[0]*255) and \
            round(self.bg[1]*255) == round(p2.bg[1]*255) and \
            round(self.bg[2]*255) == round(p2.bg[2]*255)

    def swap(self):
        return Palette(copy(self.fg), copy(self.bg))

    def paintdrop(self, p2:'Palette'):
        if self != p2:
            self._bg = mix(self._bg, 1-SMOOTH, p2.bg, SMOOTH)
            self._fg = mix(self._fg, 1-SMOOTH, p2.fg, SMOOTH)
            self.bg = [a for a in self._bg]
            self.fg = [a for a in self._fg]
            return False
        else:
            self.bg = [a for a in p2.bg]
            self.fg = [a for a in p2.fg]
        return True
    
    def __str__(self) -> str:
        return f"P( {str(self.bg)} {str(self.fg)} )"

GREEN = Palette([0,1,0])
RED = Palette([1,0,0])
BLUE = Palette([0,0,1])
WHITE = Palette([1,1,1])
BLACK = Palette([0,0,0])

colors = {
    # Original Set
    'Cyan': [0.0, 0.7843, 0.7843],
    'Aqua': [0.1961, 0.549, 0.8627],
    'Magenta': [1.0, 0.0, 0.7059],
    'Green': [0.0, 1.0, 0.0],
    'Blue': [0.0, 0.1961, 1.0],
    'PBlue': [0.0, 0.0, 1.0],         # Pure Blue
    'Mint': [0.0, 1.0, 0.4706],
    'Violet': [0.2941, 0.0, 1.0],
    'Orange': [1.0, 0.2353, 0.0],
    'Yellow': [1.0, 0.7843, 0.0],
    'Gold': [1.0, 0.498, 0.0],
    'Silver': [0.8, 0.8, 0.9],
    'Red': [1.0, 0.0196, 0.0],
    'PRed': [1.0, 0.0, 0.0],          # Pure Red
    'Pink': [1.0, 0.1961, 0.3922],
    'White': [1.0, 1.0, 1.0],
    'Black': [0.0, 0.0, 0.0],         # Same as Off

    # Second Set
    'Electric Blue': [0.0, 0.498, 1.0],
    'Sky Blue': [0.5294, 0.8078, 0.9216],
    'Turquoise': [0.251, 0.8784, 0.8157],
    'Teal': [0.0, 0.502, 0.502], # really low brightness
    'Deep Purple': [0.5412, 0.1686, 0.8863],
    'Hot Pink': [1.0, 0.4118, 0.7059],
    'Amethyst': [0.6, 0.4, 0.8],
    'Fuchsia': [1.0, 0.0, 1.0],
    'Lime Green': [0.1961, 0.8039, 0.1961],
    'Emerald': [0.0, 0.5882, 0.2941],
    'Spring Green': [0.0, 1.0, 0.498],
    'Crimson': [0.8627, 0.0784, 0.2353],
    'Tangerine': [1.0, 0.5098, 0.0],
    'Scarlet': [1.0, 0.1373, 0.0],
    'Goldenrod': [0.8549, 0.6471, 0.1255],
    'Warm White': [1.0, 0.9608, 0.902],
    'Ice White': [0.902, 0.9804, 1.0],
    'Off': [0.0, 0.0, 0.0]              # Same as Black
}

def get_palette(S):
    colors_ = S.split("-")
    if(len(colors_) == 1):
        c1 = colors_[0]
        ret = [colors[c1], colors[c1]]
        return ret
    if(len(colors_) == 2):
        c1 = colors_[0]
        c2 = colors_[1]
        ret = [colors[c1], colors[c2]]
        return ret