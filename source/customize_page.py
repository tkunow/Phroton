import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from layout_elements import InteractionBar, ViewFrame, InfoBar
from custom_types import Pages

class CustomizePage(tk.Frame):
    def __init__(self, parent, controller, image) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.current_image = image

        # draw mode
        self.mode_circle = False
        self.mode_rectangle = False
        self.mode_freehand = False

        self.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # region: Top Bar for interaction with the image
        interaction_bar = InteractionBar(root=self)
        back = interaction_bar.button(text="<-", width=5, command=lambda: self.controller.show_page(Pages.START), location=(0,0))

        #region: Display the image
        view_frame = ViewFrame(root=self)
        # canvas to display image
        self.canvas = view_frame.canvas(location=(0,0))
        self.current_image = image
        self.image_id = self.canvas.create_image(0, 0, anchor="nw")
        self._render_image()

        # keep image centered when smaller than the canvas
        self.canvas.bind("<Configure>", lambda event: self.controller._position_image(self.controller.base_image, self.canvas, self.image_id))

        # region: Bottom Bar for image information
        info_bar = InfoBar(self)
        self.name_l = info_bar.label(text=f"{self.controller.image_list[self.controller.image_index]}", location=(0,0))
        self.dimension_l = info_bar.label(text=f"{self.controller.base_image.shape[0]} x {self.controller.base_image.shape[1]}", location=(1,0))
        self.mode_switch = info_bar.slider(text="mode", command=lambda: self.controller._change_theme(), location=(2,0))

    def _render_image(self) -> None:
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.current_image))
        self.current_phototk = imgtk
        self.canvas.itemconfigure(self.image_id, image=imgtk)
        self.controller._position_image(self.current_image, self.canvas, self.image_id)

    #def _mouse_position(self, event) -> None:
    #    self.mouse_position_x = event.x
    #    self.mouse_position_y = event.y

    #    if self.mode_rectangle and self._check_image_bounds():
    #        image_xy = self.canvas.coords(self.image_id)
    #        x = event.x - image_xy[0]
    #        y = event.y - image_xy[1]
    #        self.draw_position_start = (int(x), int(y))

    #def _mouse_drag(self, event) -> None:
    #    if not self.mode_circle and not self.mode_rectangle and not self.mode_freehand:
    #        self._drag_image(event)
    #    elif self.mode_rectangle and self._check_image_bounds():
    #        image_xy = self.canvas.coords(self.image_id)
    #        self.draw_position_end = (int(event.x - image_xy[0]), int(event.y - image_xy[1]))
    #        self._render_zoomed_image(self.cv2_obj._draw_rectangle(self.base_image, self.draw_position_start, self.draw_position_end))
    #        #self._display_image(self.cv2_obj._draw_rectangle(self.base_image, self.draw_position_start, self.draw_position_end))

    #    self.mouse_position_x = event.x
    #    self.mouse_position_y = event.y

    #def _mouse_draw(self, event) -> None:
    #    if self.mode_rectangle and self._check_image_bounds():
    #        image_xy = self.canvas.coords(self.image_id)
    #        self.draw_position_end = (int(event.x - image_xy[0]), int(event.y - image_xy[1]))
    #        self.base_image = self.cv2_obj._draw_rectangle(self.base_image, self.draw_position_start, self.draw_position_end)
    #        self._render_zoomed_image()

    #        print(f"MousePos: {self.mouse_position_x}, {self.mouse_position_y} | RelativeMousePos: {self.draw_position_end}")
    #        #self._display_image(self.base_image)

    #def _check_image_bounds(self) -> bool:
    #    image_p1 = self.canvas.coords(self.image_id)
    #    image_p2 = [image_p1[0] + self.current_image.shape[1], image_p1[1] + self.current_image.shape[0]]

    #    mouse_pos = [self.mouse_position_x, self.mouse_position_y]
    #    print(f"top: {image_p1} | bottom {image_p2} | ")
    #    print(f"width: {self.current_image.shape[1]} | height: {self.current_image.shape[0]}")
    #    
    #    if (image_p1[0] <= self.mouse_position_x <= image_p2[0] and image_p1[1] <= self.mouse_position_y <= image_p2[1]):
    #        return True
    #    
    #    return False

