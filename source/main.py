from os import listdir, path
from typing import List

from frontend import Application
from constants import WORKING_DIR, PROJECT_ROOT, IMAGETYPES
from custom_types import ThemeMode

def list_images() -> List:
    images = []
    for items in listdir(WORKING_DIR):
        if (items.endswith(IMAGETYPES)):
            images.append(items)
    return images

if __name__ == "__main__":
    print(list_images())

    phroton = Application(list_images(), ThemeMode.DARK)
    phroton.tk_root.mainloop()

