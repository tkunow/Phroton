from pathlib import Path
from os import path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKING_DIR = Path.cwd()
ASSETS = path.join(PROJECT_ROOT, "assets")
THEME = "park"

IMAGETYPES = (".png", ".bmp", ".jpg")
