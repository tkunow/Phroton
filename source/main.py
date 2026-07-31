from pathlib import Path
from frontend import FrontEnd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
img_path = PROJECT_ROOT / "test" / "dots.bmp"

if __name__ == "__main__":
    phroton = FrontEnd(img_path)
    phroton.tk_root.mainloop()

