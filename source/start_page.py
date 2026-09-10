import os

import tkinter as tk
from tkinter import ttk, Button, Scale, Canvas, Label, Checkbutton
from PIL import Image, ImageTk

from layout_elements import InteractionBar, ViewFrame, InfoBar
from custom_types import Rotation, KeyEvent
from constants import WORKING_DIR  
from customize_page import CustomizePage

clamp = lambda val, minv, maxv: max(minv, min(val, maxv))

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.zoom_factor = 1.0
        self.current_image = None

        self.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # region: Top Bar for interaction with the image
        interaction_bar = InteractionBar(root=self)
        # next Button
        nleft = interaction_bar.button(text="<-", width=5, command=lambda: self._next_image(-1), location=(0,0))
        nright = interaction_bar.button(text="->", width=5, command=lambda: self._next_image(1), location=(1,0))
        # rotate Buttons
        rleft = interaction_bar.button(text="rleft", command=lambda: self._rotate_Image(Rotation.LEFT), location=(2,0))
        rright = interaction_bar.button(text="rright", command=lambda: self._rotate_Image(Rotation.RIGHT), location=(3,0))
        # zoom Image
        self.zoomB = interaction_bar.scale(from_=0.0, to=16.0, value=self.zoom_factor, command=self._zoom, location=(4,0))
        customize = interaction_bar.button(text="customize", command=lambda: self.controller.add_page(CustomizePage(parent=self.controller.tk_root, controller=self.controller)), location=(5,0))

        #region: Display the image
        view_frame = ViewFrame(root=self)
        # canvas to display image
        self.canvas = view_frame.canvas(location=(0,0))

        # region: Bottom Bar for image information
        info_bar = InfoBar(self)
        self.name_l = info_bar.label(text=f"{self.controller.image_list[self.controller.image_index]}", location=(0,0))
        self.dimension_l = info_bar.label(text=f"{self.controller.base_image.shape[0]} x {self.controller.base_image.shape[1]}", location=(1,0))
        self.mode_switch = info_bar.slider(text="mode", command=lambda: self.controller._change_theme(), location=(2,0))

        # self.focus_set()
        # keyboard shortcut
        self.bind("<Left>", lambda val: self._next_image(-1))
        self.bind("<Right>", lambda val: self._next_image(1))

        self.bind("<Key>", lambda val: self._keyhandler(val))
        self.bind("<KeyRelease>", lambda val: self.controller.check_controll_keys(val, KeyEvent.UP))

        self.canvas.bind("<ButtonPress-1>", self._mouse_position)
        self.canvas.bind("<B1-Motion>", self._mouse_drag)

        # load and display image
        self.image_id = self.canvas.create_image(0, 0, anchor="nw")
        self._render_image()

        # keep image centered when smaller than the canvas
        self.canvas.bind("<Configure>", lambda event: self.controller._position_image(self.controller.base_image, self.canvas, self.image_id))

    def _keyhandler(self, val):
        if val.keycode == 37 or val.keycode == 105:
            self.controller.check_controll_keys(val, KeyEvent.DOWN)
            return

        if self.controller.controll_keys["ctrl"]:
            if val.keycode == 27:
                self._rotate_Image(Rotation.LEFT)
            elif val.keycode == 46:
                self._rotate_Image(Rotation.RIGHT)
            elif val.keycode == 35:
                zoom_value = clamp(self.zoom_factor + 0.4, 0.0, 16.0)
                self.zoomB.set(zoom_value)
                self._zoom(zoom_value)
            elif val.keycode == 61:
                zoom_value = clamp(self.zoom_factor - 0.4, 0.0, 16.0)
                self.zoomB.set(zoom_value)
                self._zoom(zoom_value)
            elif val.keycode == 36:
                self.controller.add_page(CustomizePage(parent=self.controller.tk_root, controller=self.controller))
        else:
            print(val.keysym, val.keycode)

    def _next_image(self, direction: int) -> None:
        if self.controller.image_index + direction < 0:
            self.controller.image_index = len(self.controller.image_list) - 1
        elif self.controller.image_index + direction > len(self.controller.image_list) - 1:
            self.controller.image_index = 0
        else:
            self.controller.image_index = self.controller.image_index + direction

        self.name_l.configure(text=self.controller.image_list[self.controller.image_index])
        self.controller.base_image = self.controller.cv2_obj.read_image(os.path.join(WORKING_DIR, self.controller.image_list[self.controller.image_index]))
        self.dimension_l.configure(text=f"{self.controller.base_image.shape[0]} x {self.controller.base_image.shape[1]}")
        self.current_image = self.controller.base_image

        self.zoom_factor = 1.0
        self.zoomB.set(self.zoom_factor)

        self._render_image()


    def _mouse_position(self, event) -> None:
        self.mouse_position_x = event.x
        self.mouse_position_y = event.y

    def _mouse_drag(self, event) -> None:
        dx = event.x - self.mouse_position_x
        dy = event.y - self.mouse_position_y

        self.canvas.move(self.image_id, dx, dy)

        self.mouse_position_x = event.x
        self.mouse_position_y = event.y

    def _zoom(self, value) -> None:
        zoom_value = float(value)
        self.zoom_factor = max(0.01, zoom_value)

        self._render_image()

    def _rotate_Image(self, rotation: Rotation) -> None:
        self.current_image = self.controller.cv2_obj.rotate_image(self.current_image, rotation)
        self.zoom_factor = 1.0
        self.zoomB.set(self.zoom_factor)

        # write image to disk
        self.controller.cv2_obj.save_image(self.controller.image_list[self.controller.image_index], self.current_image)

        self._render_image()

    def _render_image(self) -> None:
        if self.current_image is None:
            print("set current image")
            self.current_image = self.controller.base_image

        zoom_image = self.controller.cv2_obj.zoom_image(self.current_image, self.zoom_factor)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(zoom_image))
        self.current_phototk = imgtk
        self.canvas.itemconfigure(self.image_id, image=imgtk)
        self.controller._position_image(self.current_image, self.canvas, self.image_id)
