import tkinter as tk
from PIL import Image, ImageTk
from imageview import ImageView
from custom_types import Rotation

class FrontEnd:
    def __init__(self, path: str):
        self.tk_root = tk.Tk()
        self.tk_root.title("Phroto - Imageviewer")
        self.tk_root.protocol("WM_DELETE_WINDOW", self.close)
        self.tk_root.columnconfigure(0, weight=1)
        self.tk_root.rowconfigure(0, weight=1)

        self.cv2_obj = ImageView()

        content = tk.Frame(self.tk_root)

        content.grid(column=0, row=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        interactionbar = tk.Frame(content, padx=10, pady=10)
        interactionbar.grid(column=0, row=0, sticky="ew")
        rleft = tk.Button(interactionbar, text="rleft", command=lambda: self.displayImage(self.cv2_obj.rotateImage(self.current_image, Rotation.LEFT)))
        rleft.grid(column=0, row=0, padx=(0, 5))
        rright = tk.Button(interactionbar, text="rright", command=lambda: self.displayImage(self.cv2_obj.rotateImage(self.current_image, Rotation.RIGHT)))
        rright.grid(column=1, row=0, padx=(0, 5))

        self.panel = tk.Label(content, pady=10, padx=10)
        self.panel.grid(column=0, row=1)

        self.current_image = self.cv2_obj.readImage(path)
        self.displayImage(self.current_image)

    def displayImage(self, image):
        self.current_image = image
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.current_image))
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

    def close(self):
              self.tk_root.destroy()

