import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from enum import Enum


img_path = "../test/dots.bmp"

class Rotation(Enum):
    LEFT = -90
    RIGHT = 90

class ImageView:
    def convertBGR2RGB(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def readImage(self, path: str, mode: int = cv2.IMREAD_COLOR):
        img = cv2.imread(path, mode)
    
        if img is None:
            raise FileNotFoundError(f"Could not decode image: {path}")
        return self.convertBGR2RGB(img)

    def rotateImage(self, image, direction: Rotation):
        height, width = image.shape[:2]
        center = (width/2, height/2)

        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=direction.value, scale=1)
        return self.convertBGR2RGB(cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height)))

class FrontEnd:
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.title("Phroto - Imageviewer")
        self.tk_root.protocol("WM_DELETE_WINDOW", self.close)

        self.cv2_obj = ImageView()


        rleft = tk.Button(self.tk_root, text="rleft", command=lambda: self.displayImage(self.cv2_obj.rotateImage(self.current_image, Rotation.LEFT)))
        rleft.pack(padx=10, pady=10)
        rright = tk.Button(self.tk_root, text="rright", command=lambda: self.displayImage(self.cv2_obj.rotateImage(self.current_image, Rotation.RIGHT)))
        rright.pack(padx=10, pady=10)

        self.panel = tk.Label(self.tk_root)
        self.panel.pack(padx=10, pady=10)


        self.current_image = self.cv2_obj.readImage(img_path)
        self.displayImage(self.current_image)

    def displayImage(self, image):
        self.current_image = image
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.current_image))
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

    def close(self):
              self.tk_root.destroy()


if __name__ == "__main__":
    phroton = FrontEnd()
    phroton.tk_root.mainloop()

