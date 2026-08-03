from pathlib import Path
from os import listdir, path
from frontend import FrontEnd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKING_DIR = Path.cwd()

# for testing 
img_path = PROJECT_ROOT / "test" / "dots.bmp"

ImageTypes = (".png", ".bmp", ".jpg")

def listImages() -> List:
    images = []
    for items in listdir(WORKING_DIR):
        if (items.endswith(ImageTypes)):
            images.append(items)
    return images

if __name__ == "__main__":
    print(listImages())

    phroton = FrontEnd(img_path)
    phroton.tk_root.mainloop()

