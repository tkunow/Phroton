import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from imageview import ImageView
from custom_types import Rotation
from typing import List
import os
from constants import PROJECT_ROOT, ASSETS, WORKING_DIR, THEME
from custom_types import ThemeMode

class FrontEnd:
    def __init__(self, imagelist: List, mode: ThemeMode):
        self.tk_root = tk.Tk()
        self.tk_root.title("Phroto - Imageviewer")
        self.tk_root.protocol("WM_DELETE_WINDOW", self._close)
        self.tk_root.columnconfigure(0, weight=1)
        self.tk_root.rowconfigure(0, weight=1)

        self.mode = mode
        self.theme_path = os.path.join(ASSETS, THEME.lower(), THEME.lower() + ".tcl")
        self.tk_root.tk.call("source", self.theme_path)
        self.tk_root.tk.call("set_theme", self.mode.lower())

        self.cv2_obj = ImageView()
        self.zoom_factor = 1.0
        self.current_image = None

        content = tk.Frame(self.tk_root)

        content.grid(column=0, row=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)


        interactionbar = ttk.Frame(content, padding=10)
        interactionbar.grid(column=0, row=0, sticky="ew")

        # next Button
        nleft = ttk.Button(interactionbar, text="<-", width=5, command=lambda: self._displayImage(self._nextImage(-1)))
        nleft.grid(column=0, row=0, padx=(0, 5))
        nright = ttk.Button(interactionbar, text="->", width=5, command=lambda: self._displayImage(self._nextImage(1)))
        nright.grid(column=1, row=0, padx=(0, 20))

        # rotate Buttons
        rleft = ttk.Button(
            interactionbar,
            text="rleft",
            command=lambda: self._displayImage(self.cv2_obj.rotateImage(self.base_image, Rotation.LEFT)),
        )
        rleft.grid(column=2, row=0, padx=(0, 5))
        rright = ttk.Button(
            interactionbar,
            text="rright",
            command=lambda: self._displayImage(self.cv2_obj.rotateImage(self.base_image, Rotation.RIGHT)),
        )
        rright.grid(column=3, row=0, padx=(0, 5))

        # zoom Image
        self.zoomB = ttk.Scale(
            interactionbar,
            from_=0.0,
            to=16.0,
            value=self.zoom_factor,
            orient="horizontal",
            command=self._zoom,
        )
        self.zoomB.grid(column=4, row=0, padx=(0, 5), sticky="ew")
        interactionbar.columnconfigure(4, weight=1)

        view_frame = ttk.Frame(content)
        view_frame.grid(column=0, row=1, sticky="nsew")
        view_frame.columnconfigure(0, weight=1)
        view_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(view_frame, bg="black", highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky="nsew")

        # keep image centered when smaller than the canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.image_id = self.canvas.create_image(0, 0, anchor="nw")

        self.image_list = imagelist
        self.image_index = 0
        self._displayImage(self.cv2_obj.readImage(os.path.join(WORKING_DIR, self.image_list[self.image_index])))

        # bottom infobar
        infobar = ttk.Frame(content, padding=10)
        infobar.grid(column=0, row=2, sticky="nsew")

        self.nameL = ttk.Label(infobar, text=f"{self.image_list[self.image_index]}")
        self.nameL.grid(column=0, row=0, padx=(0, 5))

        # keyboard shortcut
        self.tk_root.bind("<Left>", lambda val: self._displayImage(self._nextImage(-1)))
        self.tk_root.bind("<Right>", lambda val: self._displayImage(self._nextImage(1)))
        self.canvas.bind("<Button-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_image)

    def _nextImage(self, direction: int):
        if self.image_index + direction < 0:
            self.image_index = len(self.image_list) - 1
        elif self.image_index + direction > len(self.image_list) - 1:
            self.image_index = 0
        else:
            self.image_index = self.image_index + direction

        self.nameL.configure(text=self.image_list[self.image_index])
        return self.cv2_obj.readImage(os.path.join(WORKING_DIR, self.image_list[self.image_index]))

    def _zoom(self, value):
        zoom_value = float(value)
        self.zoom_factor = max(0.01, zoom_value)
        self._renderZoomedImage()

    def _renderZoomedImage(self):
        if self.base_image is None:
            return

        display_image = self.cv2_obj.zoomImage(self.base_image, self.zoom_factor)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(display_image))
        # keep a reference to the array and the PhotoImage
        self.current_image = display_image
        self.current_phototk = imgtk
        self.canvas.itemconfigure(self.image_id, image=imgtk)
        self._position_image()

    def _displayImage(self, image) -> None:
        self.base_image = image
        self.zoom_factor = 1.0
        self.zoomB.set(self.zoom_factor)
        self._renderZoomedImage()

    def _changeTheme(self, theme: Theme) -> None:
        self.mode = theme

    def _close(self):
        self.tk_root.destroy()

    def _on_canvas_configure(self, event):
        # When the canvas resizes, reposition the image to stay centered if possible.
        self._position_image()

    def _drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _drag_image(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.canvas.move(self.image_id, dx, dy)

        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _position_image(self):
        # Position the image inside the canvas. Center if smaller than canvas,
        # otherwise anchor at top-left
        if not hasattr(self, 'current_image') or self.current_image is None:
            return

        try:
            img_w = int(self.current_image.shape[1])
            img_h = int(self.current_image.shape[0])
        except Exception:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if img_w <= canvas_w and img_h <= canvas_h:
            x = (canvas_w - img_w) // 2
            y = (canvas_h - img_h) // 2
        else:
            x = 0
            y = 0

        self.canvas.coords(self.image_id, x, y)
