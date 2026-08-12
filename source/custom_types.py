from enum import Enum

class Rotation(Enum):
    LEFT = -90
    RIGHT = 90

class ThemeMode:
    DARK = "dark"
    LIGHT = "light"

class Pages:
    START = "start_page"
    CUSTOMIZE = "customize_page"

class DrawMode:
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    LINE = "line"
    FREEHAND = "freehand"
