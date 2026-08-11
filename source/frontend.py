import tkinter as tk
from tkinter import ttk, Button, Scale, Canvas, Label, Checkbutton
from PIL import Image, ImageTk
from imageview import ImageView
from custom_types import Rotation
from typing import List, Tuple, Literal
import os
from constants import PROJECT_ROOT, ASSETS, WORKING_DIR, THEME
from custom_types import ThemeMode, Pages
from cv2.typing import MatLike
from start_page import StartPage
from customize_page import CustomizePage

class Application:
    def __init__(self, imagelist: List, mode: str) -> None:
        self.mode = mode
        self.image_list = imagelist
        self.image_index = 0

        self.tk_root = tk.Tk()
        self.tk_root.title("Phroto - Imageviewer")
        self.tk_root.protocol("WM_DELETE_WINDOW", self._close)
        self.tk_root.columnconfigure(0, weight=1)
        self.tk_root.rowconfigure(0, weight=1)

        self.theme_path = os.path.join(ASSETS, THEME.lower(), THEME.lower() + ".tcl")
        self.tk_root.tk.call("source", self.theme_path)
        self.tk_root.tk.call("set_theme", self.mode.lower())

        self.cv2_obj = ImageView()
        self.base_image = self.cv2_obj.read_image(os.path.join(WORKING_DIR, self.image_list[self.image_index]))

        self.pages = {}
        self.pages[Pages.START] = StartPage(parent=self.tk_root, controller=self)
        self.pages[Pages.START].grid(row=0, column=0, sticky="nsew")
        self.pages[Pages.CUSTOMIZE] = CustomizePage(parent=self.tk_root, controller=self, image=self.base_image)
        self.pages[Pages.CUSTOMIZE].grid(row=0, column=0, sticky="nsew")

        self.show_page(Pages.START)

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


    # TODO: für customize image
    #def _display_image(self, image, image_id) -> None:
    #    self.zoom_factor = 1.0
    #    self.zoomB.set(self.zoom_factor)
    #    self._render_zoomed_image()

    def _change_theme(self) -> None:
        if self.mode is not None:
            if self.mode is ThemeMode.LIGHT:
                self.mode = ThemeMode.DARK
                #self.canvas.configure(bg='black')
            else:
                self.mode = ThemeMode.LIGHT
                #self.canvas.configure(bg='white')
        else:
            self.mode = ThemeMode.DARK

        self.tk_root.tk.call("set_theme", self.mode.lower())

    def _position_image(self, image, canvas, image_id) -> None:
        try:
            img_w = int(image.shape[1])
            img_h = int(image.shape[0])
        except Exception:
            return

        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()

        if img_w <= canvas_w and img_h <= canvas_h:
            x = (canvas_w - img_w) // 2
            y = (canvas_h - img_h) // 2
        else:
            x = 0
            y = 0

        canvas.coords(image_id, x, y)

    def _close(self) -> None:
        self.tk_root.destroy()
