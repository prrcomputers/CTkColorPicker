import math
import colorsys
from typing import Sequence, Callable, List
from PIL import Image
import string


def normalize_hex(value: str | None) -> str | None:
    """Return a normalized ``#rrggbb`` color string or ``None`` if invalid."""

    if value is None:
        return None
    value = value.strip().lower()
    if not value:
        return None
    if value.startswith("#"):
        value = value[1:]
    if len(value) == 3 and all(c in string.hexdigits for c in value):
        return "#" + "".join(c * 2 for c in value)
    if len(value) == 6 and all(c in string.hexdigits for c in value):
        return "#" + value
    return None


def rgb_to_hsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Return the HSV representation of an RGB color."""

    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """Return the integer RGB representation of an HSV color."""

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def hsv_to_wheel(h: float, s: float, image_dimension: int) -> tuple[float, float]:
    """Convert HSV values to ``(x, y)`` wheel coordinates."""

    radius = s * (image_dimension / 2 - 1)
    angle = h * 2 * math.pi
    x = image_dimension / 2 + radius * math.cos(angle)
    y = image_dimension / 2 + radius * math.sin(angle)
    return x, y


def hex_to_wheel(hex_color: str | None, image_dimension: int) -> tuple[float, float, int]:
    """Return wheel coordinates and brightness for ``hex_color``.

    The color wheel image contains colors at full brightness. Colors that are
    darker or lighter than those on the wheel are approximated by positioning
    the target at their hue/saturation location with full brightness and
    returning the original value component as the ``brightness`` slider value.
    Achromatic colors (saturation ``0``) map to the center of the wheel.
    """

    normalized = normalize_hex(hex_color) if hex_color else None
    center = image_dimension / 2
    if normalized is None:
        return center, center, 255

    r, g, b = (int(normalized[i : i + 2], 16) for i in (1, 3, 5))
    h, s, v = rgb_to_hsv(r, g, b)
    brightness = int(round(v * 255))
    target_x, target_y = hsv_to_wheel(h, s, image_dimension)
    return target_x, target_y, brightness


def projection_on_circle(
    point_x: float, point_y: float, circle_x: float, circle_y: float, radius: float
) -> tuple[float, float]:
    """Project a point onto the circumference of a circle."""
    angle = math.atan2(point_y - circle_y, point_x - circle_x)
    projection_x = circle_x + radius * math.cos(angle)
    projection_y = circle_y + radius * math.sin(angle)
    return projection_x, projection_y


def get_target_color(
    image: Image.Image, target_x: int, target_y: int, rgb_color: Sequence[int]
) -> List[int]:
    """Return the RGB color of ``image`` at the given coordinates.

    Falls back to ``rgb_color`` if the pixel cannot be retrieved.
    """
    try:
        r, g, b = image.getpixel((target_x, target_y))[:3]
        return [r, g, b]
    except Exception:
        return list(rgb_color)


def update_colors(
    image: Image.Image,
    target_x: int,
    target_y: int,
    brightness: int,
    rgb_color: Sequence[int],
    slider: any,
    widget: any,
    command: Callable[[str], None] | None = None,
    get_callback: Callable[[], str] | None = None,
) -> tuple[list[int], str]:
    """Update color widgets and return the RGB list and hex color.

    ``rgb_color`` provides the fallback when the target pixel cannot be read.
    """
    rgb_color = get_target_color(image, target_x, target_y, rgb_color)
    r = int(rgb_color[0] * (brightness / 255))
    g = int(rgb_color[1] * (brightness / 255))
    b = int(rgb_color[2] * (brightness / 255))
    rgb_color = [r, g, b]
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)

    slider.configure(progress_color=hex_color)

    if hasattr(widget, "delete"):
        widget.configure(fg_color=hex_color)
        widget.delete(0, "end")
        widget.insert(0, hex_color)
    else:
        try:
            widget.configure(fg_color=hex_color, text=str(hex_color))
        except Exception:
            widget.configure(fg_color=hex_color)

    if brightness < 70:
        widget.configure(text_color="white")
    else:
        widget.configure(text_color="black")
    if str(widget._fg_color) == "black":
        widget.configure(text_color="white")

    if command and get_callback:
        command(get_callback())

    return rgb_color, hex_color
