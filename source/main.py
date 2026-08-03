from os import listdir, path

from frontend import FrontEnd
from constants import WORKING_DIR, PROJECT_ROOT, IMAGETYPES
from custom_types import ThemeMode


# for testing 
img_path = PROJECT_ROOT / "test" / "dots.bmp"


def listImages() -> List:
    images = []
    for items in listdir(WORKING_DIR):
        if (items.endswith(IMAGETYPES)):
            images.append(items)
    return images

if __name__ == "__main__":
    print(listImages())

    phroton = FrontEnd(img_path, listImages(), ThemeMode.DARK)
    phroton.tk_root.mainloop()

