from os import listdir, path

from frontend import FrontEnd
from constants import WORKING_DIR, PROJECT_ROOT, IMAGETYPES
from custom_types import ThemeMode

def listImages() -> List:
    images = []
    for items in listdir(WORKING_DIR):
        if (items.endswith(IMAGETYPES)):
            images.append(items)
    return images

if __name__ == "__main__":
    print(listImages())

    phroton = FrontEnd(listImages(), ThemeMode.DARK)
    phroton.tk_root.mainloop()

