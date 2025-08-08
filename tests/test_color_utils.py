import sys
import types
from pathlib import Path
import pytest

# Stub PIL.Image to avoid Pillow dependency
PIL_module = types.ModuleType('PIL')
Image_module = types.ModuleType('Image')
class DummyImageClass:
    pass
Image_module.Image = DummyImageClass
PIL_module.Image = Image_module
sys.modules['PIL'] = PIL_module
sys.modules['PIL.Image'] = Image_module

# Add package directory to path without importing package __init__
sys.path.append(str(Path(__file__).resolve().parents[1] / 'CTkColorPicker'))

from color_utils import update_colors, normalize_hex


class DummyWidget:
    def __init__(self):
        self.config = {}
        self._fg_color = None

    def configure(self, **kwargs):
        self.config.update(kwargs)
        if 'fg_color' in kwargs:
            self._fg_color = kwargs['fg_color']


class DummyEntry(DummyWidget):
    def __init__(self):
        super().__init__()
        self.text = ""

    def delete(self, start, end):
        self.text = ""

    def insert(self, index, value):
        self.text = value


class DummyImage:
    def __init__(self, color):
        self.color = color

    def getpixel(self, coords):
        return self.color


def test_update_colors_returns_hex_and_rgb():
    img = DummyImage((255, 0, 0))
    slider, label = DummyWidget(), DummyWidget()
    rgb, hex_color = update_colors(img, 0, 0, 255, [0, 0, 0], slider, label)
    assert rgb == [255, 0, 0]
    assert hex_color == '#ff0000'


def test_brightness_adjustment():
    img = DummyImage((255, 0, 0))
    slider, label = DummyWidget(), DummyWidget()
    rgb, hex_color = update_colors(img, 0, 0, 128, [0, 0, 0], slider, label)
    assert rgb == [128, 0, 0]
    assert hex_color == '#800000'


def test_callback_invoked():
    img = DummyImage((255, 0, 0))
    slider, label = DummyWidget(), DummyWidget()
    received = []

    def callback(color):
        received.append(color)

    def getter():
        return label._fg_color

    update_colors(img, 0, 0, 255, [0, 0, 0], slider, label, command=callback, get_callback=getter)
    assert received == ['#ff0000']


def test_update_colors_entry_widget():
    img = DummyImage((0, 255, 0))
    slider, entry = DummyWidget(), DummyEntry()
    update_colors(img, 0, 0, 255, [0, 0, 0], slider, entry)
    assert entry.text == '#00ff00'
    assert entry._fg_color == '#00ff00'
    assert entry.config['text_color'] == 'black'


def test_normalize_hex_valid():
    assert normalize_hex('#fff') == '#ffffff'
    assert normalize_hex('abc') == '#aabbcc'
    assert normalize_hex('#123456') == '#123456'
    assert normalize_hex('123456') == '#123456'


def test_normalize_hex_invalid():
    assert normalize_hex('#ff') is None
    assert normalize_hex('ggg') is None
    assert normalize_hex('') is None
    assert normalize_hex(None) is None
