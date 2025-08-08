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

from color_utils import update_colors, normalize_hex_color


class DummyWidget:
    def __init__(self):
        self.config = {}
        self._fg_color = None

    def configure(self, **kwargs):
        self.config.update(kwargs)
        if 'fg_color' in kwargs:
            self._fg_color = kwargs['fg_color']


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


def test_normalize_hex_color_shorthand():
    assert normalize_hex_color('#fff') == '#ffffff'
    assert normalize_hex_color('abc') == '#aabbcc'


def test_normalize_hex_color_full():
    assert normalize_hex_color('#123456') == '#123456'
    assert normalize_hex_color('123456') == '#123456'


def test_normalize_hex_color_invalid():
    with pytest.raises(ValueError):
        normalize_hex_color('#ff')
    with pytest.raises(ValueError):
        normalize_hex_color('ggg')
