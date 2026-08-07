import tkinter as tk
from tkinter import ttk, Button, Scale, Canvas, Label, Checkbutton
from PIL import Image, ImageTk
from imageview import ImageView
from custom_types import Rotation
from typing import List, Tuple, Literal
import os
from constants import PROJECT_ROOT, ASSETS, WORKING_DIR, THEME
from custom_types import ThemeMode
from cv2.typing import MatLike

class Panel():
    def __init__(self, root) -> None:
        self.root = root
        self.padding = 10
        self.frame = ttk.Frame(self.root, padding=self.padding)

    def button(self, text: str, command,  location: Tuple, width: int | Literal[''] = "") -> ttk.Button:
        b = ttk.Button(self.frame, text=text, width=width, command=command)
        b.grid(column=location[0], row=location[1], padx=(0, 5))
        return b

    def scale(self, from_: float, to: float, value: float, command, location: Tuple) -> ttk.Scale:
        s = ttk.Scale(
            self.frame,
            from_=0.0,
            to=16.0,
            value=value,
            orient="horizontal",
            command=command
        )
        s.grid(column=location[0], row=location[1], padx=(0, 5), sticky="ew")
        return s

    def canvas(self, location: Tuple) -> Canvas:
        c = tk.Canvas(self.frame, bg="black", highlightthickness=0)
        c.grid(column=location[0], row=location[1], sticky="nsew")
        return c

    def label(self, text: str, location: Tuple) -> ttk.Label:
        l = ttk.Label(self.frame, text=text)
        l.grid(column=location[0], row=location[1], padx=(0, 5))
        return l

    def slider(self, command, location: Tuple) -> ttk.Checkbutton:
        c = ttk.Checkbutton(self.frame, text="mode", command=command, style="Switch.TCheckbutton")
        c.grid(column=location[0], row=location[1], padx=(0,5))
        return c



class InteractionBar(Panel):
    def __init__(self, root) -> None:
        super().__init__(root)

        self.frame.grid(column=0, row=0, sticky="ew")
        self.frame.columnconfigure(4, weight=1)

class InfoBar(Panel):
    def __init__(self, root) -> None:
        super().__init__(root)

        self.frame.grid(column=0, row=2, sticky="nsew")

class ViewFrame(Panel):
    def __init__(self, root) -> None:
        super().__init__(root)

        self.frame.grid(column=0, row=1, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

class Application:
    def __init__(self, imagelist: List, mode: str) -> None:
        self.image_list = imagelist
        self.mode = mode
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
        self.zoom_factor = 1.0
        self.current_image = None
        self.base_image = self.cv2_obj.read_image(os.path.join(WORKING_DIR, self.image_list[self.image_index]))

        # set image viewer frame
        self._set_image_viewer_frame()

        # load and display image
        self.image_id = self.canvas.create_image(0, 0, anchor="nw")
        self._display_image(self.base_image)

        # keyboard shortcut
        self._set_keyboard_shortcut()

    def _set_image_viewer_frame(self) -> None:
        content = tk.Frame(self.tk_root)
        content.grid(column=0, row=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        # region: Top Bar for interaction with the image
        interaction_bar = InteractionBar(root=content)
        # next Button
        nleft = interaction_bar.button(text="<-", width=5, command=lambda: self._display_image(self._next_image(-1)), location=(0,0))
        nright = interaction_bar.button(text="->", width=5, command=lambda: self._display_image(self._next_image(1)), location=(1,0))
        # rotate Buttons
        rleft = interaction_bar.button(text="rleft", command=lambda: self._display_image(self.cv2_obj.rotate_image(self.base_image, Rotation.LEFT)), location=(2,0))
        rright = interaction_bar.button(text="rright", command=lambda: self._display_image(self.cv2_obj.rotate_image(self.base_image, Rotation.RIGHT)), location=(3,0))
        # zoom Image
        self.zoomB = interaction_bar.scale(from_=0.0, to=16.0, value=self.zoom_factor, command=self._zoom, location=(4,0))

        #region: Display the image
        view_frame = ViewFrame(root=content)
        # canvas to display image
        self.canvas = view_frame.canvas(location=(0,0))
        # keep image centered when smaller than the canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)


        # region: Bottom Bar for image information
        info_bar = InfoBar(content)
        self.name_l = info_bar.label(text=f"{self.image_list[self.image_index]}", location=(0,0))
        self.dimension_l = info_bar.label(text=f"{self.base_image.shape[0]} x {self.base_image.shape[1]}", location=(1,0))
        self.mode_switch = info_bar.slider(command=lambda: self._change_theme(), location=(2,0))

    def _set_keyboard_shortcut(self) -> None:
        self.tk_root.bind("<Left>", lambda val: self._display_image(self._next_image(-1)))
        self.tk_root.bind("<Right>", lambda val: self._display_image(self._next_image(1)))
        self.canvas.bind("<Button-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_image)

    def _next_image(self, direction: int) -> MatLike:
        if self.image_index + direction < 0:
            self.image_index = len(self.image_list) - 1
        elif self.image_index + direction > len(self.image_list) - 1:
            self.image_index = 0
        else:
            self.image_index = self.image_index + direction

        self.name_l.configure(text=self.image_list[self.image_index])
        self.dimension_l.configure(text=f"{self.base_image.shape[0]} x {self.base_image.shape[1]}")
        return self.cv2_obj.read_image(os.path.join(WORKING_DIR, self.image_list[self.image_index]))

    def _zoom(self, value) -> None:
        zoom_value = float(value)
        self.zoom_factor = max(0.01, zoom_value)
        self._render_zoomed_image()

    def _render_zoomed_image(self) -> None:
        if self.base_image is None:
            return

        display_image = self.cv2_obj.zoom_image(self.base_image, self.zoom_factor)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(display_image))
        # keep a reference to the array and the PhotoImage
        self.current_image = display_image
        self.current_phototk = imgtk
        self.canvas.itemconfigure(self.image_id, image=imgtk)
        self._position_image()

    def _display_image(self, image) -> None:
        self.base_image = image
        self.zoom_factor = 1.0
        self.zoomB.set(self.zoom_factor)
        self._render_zoomed_image()

    def _change_theme(self) -> None:
        if self.mode is not None:
            if self.mode is ThemeMode.LIGHT:
                self.mode = ThemeMode.DARK
                self.canvas.configure(bg='black')
            else:
                self.mode = ThemeMode.LIGHT
                self.canvas.configure(bg='white')
        else:
            self.mode = ThemeMode.DARK

        self.tk_root.tk.call("set_theme", self.mode.lower())

    def _close(self) -> None:
        self.tk_root.destroy()

    def _on_canvas_configure(self, event) -> None:
        # When the canvas resizes, reposition the image to stay centered if possible.
        self._position_image()

    def _drag_start(self, event) -> None:
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _drag_image(self, event) -> None:
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.canvas.move(self.image_id, dx, dy)

        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _position_image(self) -> None:
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
