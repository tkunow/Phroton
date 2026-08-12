from typing import Tuple
from math import sqrt, pow

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from layout_elements import InteractionBar, ViewFrame, InfoBar
from custom_types import Pages, DrawMode

class CustomizePage(tk.Frame):
    def __init__(self, parent, controller, image) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.tmp_image = None

        # draw mode
        self.draw_mode = {
            DrawMode.RECTANGLE: False,
            DrawMode.CIRCLE: False,
            DrawMode.LINE: False,
            DrawMode.FREEHAND: False
        }

        self.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # region: Top Bar for interaction with the image
        interaction_bar = InteractionBar(root=self)
        back = interaction_bar.button(text="<-", width=5, command=lambda: self.controller.show_page(Pages.START), location=(0,0))
        reset = interaction_bar.button(text="reset", command=lambda: self._reset_image(), location=(1,0))
        self.rectangle = interaction_bar.slider(text="rectangle", command=lambda: self._switch_draw_mode(DrawMode.RECTANGLE), location=(2,0))
        self.circle = interaction_bar.slider(text="circle", command=lambda: self._switch_draw_mode(DrawMode.CIRCLE), location=(3,0))
        self.line = interaction_bar.slider(text="line", command=lambda: self._switch_draw_mode(DrawMode.LINE), location=(4,0))
        self.freehand = interaction_bar.slider(text="freehand", command=lambda: self._switch_draw_mode(DrawMode.FREEHAND), location=(5,0))

        #region: Display the image
        view_frame = ViewFrame(root=self)
        # canvas to display image
        self.canvas = view_frame.canvas(location=(0,0))
        self.current_image = image.copy()
        self.image_id = self.canvas.create_image(0, 0, anchor="nw")
        self._render_image()

        # keep image centered when smaller than the canvas
        self.canvas.bind("<Configure>", lambda event: self.controller._position_image(self.controller.base_image, self.canvas, self.image_id))

        # region: Bottom Bar for image information
        info_bar = InfoBar(self)
        self.name_l = info_bar.label(text=f"{self.controller.image_list[self.controller.image_index]}", location=(0,0))
        self.dimension_l = info_bar.label(text=f"{self.controller.base_image.shape[0]} x {self.controller.base_image.shape[1]}", location=(1,0))
        self.mode_switch = info_bar.slider(text="mode", command=lambda: self.controller._change_theme(), location=(2,0))

        # keyboard shortcut
        self.canvas.bind("<ButtonPress-1>", self._mouse_start_position)
        self.canvas.bind("<ButtonRelease-1>", self._mouse_draw)
        self.canvas.bind("<B1-Motion>", self._mouse_follow_position)

        self.last_freehand_position = None

    def _render_image(self, image=None) -> None:
        display_image = None
        if image is None:
            display_image = self.current_image
        else:
            display_image = image

        imgtk = ImageTk.PhotoImage(image=Image.fromarray(display_image))
        self.current_phototk = imgtk
        self.canvas.itemconfigure(self.image_id, image=imgtk)
        self.controller._position_image(self.current_image, self.canvas, self.image_id)

    def _reset_image(self) -> None:
        self.current_image = self.controller.base_image.copy()
        self._render_image()

    def _switch_draw_mode(self, mode) -> None:
        for key in self.draw_mode:
            if key is mode:
                self.draw_mode[key] = True
            else:
                self.draw_mode[key] = False

        if mode is not DrawMode.RECTANGLE:
            self.rectangle.state(['!selected'])
        if mode is not DrawMode.CIRCLE:
            self.circle.state(['!selected'])
        if mode is not DrawMode.LINE:
            self.line.state(['!selected'])
            self.line.selection_clear()
        if mode is not DrawMode.FREEHAND:
            self.freehand.state(['!selected'])

    def _mouse_start_position(self, event) -> None:
        self.mouse_position_x = event.x
        self.mouse_position_y = event.y

        if self._check_image_bounds():
            image_xy = self.canvas.coords(self.image_id)
            x = event.x - image_xy[0]
            y = event.y - image_xy[1]
            self.draw_position_start = (int(x), int(y))
            if self.draw_mode[DrawMode.FREEHAND]:
                self.last_freehand_position = self.draw_position_start
                self._render_image()

    def _mouse_follow_position(self, event) -> None:
        image_xy = self.canvas.coords(self.image_id)
        draw_position_end = (int(event.x - image_xy[0]), int(event.y - image_xy[1]))

        if self.draw_mode[DrawMode.RECTANGLE] and self._check_image_bounds():
            self.tmp_image = self.controller.cv2_obj._draw_rectangle(self.current_image, self.draw_position_start, draw_position_end)
        elif self.draw_mode[DrawMode.LINE] and self._check_image_bounds():
            self.tmp_image = self.controller.cv2_obj._draw_line(self.current_image, self.draw_position_start, draw_position_end)
        elif self.draw_mode[DrawMode.CIRCLE] and self._check_image_bounds():
            radius = self._distanceP2P(self.draw_position_start, draw_position_end)
            self.tmp_image = self.controller.cv2_obj._draw_circle(self.current_image, self.draw_position_start, radius)
        elif self.draw_mode[DrawMode.FREEHAND] and self._check_image_bounds():
            self.current_image = self.controller.cv2_obj._draw_line(self.current_image, self.last_freehand_position, draw_position_end)
            self.tmp_image = self.current_image
            self.last_freehand_position = draw_position_end

        self._render_image(self.tmp_image)

        self.mouse_position_x = event.x
        self.mouse_position_y = event.y

    def _mouse_draw(self, event) -> None:
        image_xy = self.canvas.coords(self.image_id)
        draw_position_end = (int(event.x - image_xy[0]), int(event.y - image_xy[1]))

        if self.draw_mode[DrawMode.RECTANGLE] and self._check_image_bounds():
            self.current_image = self.controller.cv2_obj._draw_rectangle(self.current_image, self.draw_position_start, draw_position_end)
        if self.draw_mode[DrawMode.LINE] and self._check_image_bounds():
            self.current_image = self.controller.cv2_obj._draw_line(self.current_image, self.draw_position_start, draw_position_end)
        elif self.draw_mode[DrawMode.CIRCLE] and self._check_image_bounds():
            radius = self._distanceP2P(self.draw_position_start, draw_position_end)
            self.current_image = self.controller.cv2_obj._draw_circle(self.current_image, self.draw_position_start, radius)

        self.tmp_image = None
        self._render_image()

    def _check_image_bounds(self) -> bool:
        image_p1 = self.canvas.coords(self.image_id)
        image_p2 = [image_p1[0] + self.current_image.shape[1], image_p1[1] + self.current_image.shape[0]]

        mouse_pos = [self.mouse_position_x, self.mouse_position_y]
        
        if (image_p1[0] <= self.mouse_position_x <= image_p2[0] and image_p1[1] <= self.mouse_position_y <= image_p2[1]):
            return True
        
        return False

    def _distanceP2P(self, p1: Tuple, p2: Tuple) -> int:
        return int(sqrt(pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)))
