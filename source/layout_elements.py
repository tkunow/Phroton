import tkinter as tk
from tkinter import ttk, Button, Scale, Canvas, Label, Checkbutton
from typing import Tuple

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

    def slider(self, text:str, command, location: Tuple) -> ttk.Checkbutton:
        c = ttk.Checkbutton(self.frame, text=text, command=command, style="Switch.TCheckbutton")
        c.grid(column=location[0], row=location[1], padx=(0,5))
        return c

    def dropdown(self, default: int, values:Tuple, location: Tuple) -> ttk.Combobox:
        c = ttk.Combobox(self.frame, values=values, width=5)
        c.current(default)
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
