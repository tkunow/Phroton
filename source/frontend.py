import tkinter as tk
from PIL import Image, ImageTk
from imageview import ImageView
from custom_types import Rotation

class FrontEnd:
    def __init__(self, path: str):
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


        self.current_image = self.cv2_obj.readImage(path)
        self.displayImage(self.current_image)

    def displayImage(self, image):
        self.current_image = image
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.current_image))
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

    def close(self):
              self.tk_root.destroy()

