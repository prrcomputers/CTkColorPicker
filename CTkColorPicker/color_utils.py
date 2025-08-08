import math
from typing import Sequence, Callable, List
from PIL import Image
import string


def normalize_hex_color(value: str) -> str:
    """Return a normalized ``#rrggbb`` color string or raise ``ValueError``."""

    if value is None:
        raise ValueError("No color provided")
    value = value.strip().lower()
    if not value:
        raise ValueError("No color provided")
    if not value.startswith("#"):
        value = "#" + value
    hex_part = value[1:]
    if len(hex_part) == 3:
        if all(c in string.hexdigits for c in hex_part):
            value = "#" + "".join(c * 2 for c in hex_part)
        else:
            raise ValueError("Invalid hex digits")
    elif len(hex_part) == 6:
        if not all(c in string.hexdigits for c in hex_part):
            raise ValueError("Invalid hex digits")
        value = "#" + hex_part
    else:
        raise ValueError("Invalid length for hex color")
    return value


def projection_on_circle(
    point_x: float, point_y: float, circle_x: float, circle_y: float, radius: float
) -> tuple[float, float]:
    """Project a point onto the circumference of a circle."""
    angle = math.atan2(point_y - circle_y, point_x - circle_x)
    projection_x = circle_x + radius * math.cos(angle)
    projection_y = circle_y + radius * math.sin(angle)
    return projection_x, projection_y


def get_target_color(
    image: Image.Image, target_x: int, target_y: int, default_rgb: Sequence[int]
) -> List[int]:
    """Return the RGB color of ``image`` at the given coordinates."""
    try:
        r, g, b = image.getpixel((target_x, target_y))[:3]
        return [r, g, b]
    except AttributeError:
        return list(default_rgb)


def update_colors(
    image: Image.Image,
    target_x: int,
    target_y: int,
    brightness: int,
    default_rgb: Sequence[int],
    slider: any,
    widget: any,
    command: Callable[[str], None] | None = None,
    get_callback: Callable[[], str] | None = None,
) -> tuple[list[int], str]:
    """Update color widgets and return the RGB list and hex color."""
    rgb_color = get_target_color(image, target_x, target_y, default_rgb)
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
