#!/usr/bin/env python3

import tkinter as tk
from PIL import Image, ImageTk


class Splash(tk.Frame):
    def __init__(self, gui):
        super().__init__(gui)
        self.gui = gui

        shark = ImageTk.PhotoImage(Image.open("Resources/Splash.jpg"))
        shark_label = tk.Label(self, image=shark)
        shark_label.image = shark
        shark_label.grid(row=0, column=0)

        self.status_label = tk.Label(self)
        self.status_label.grid(row=1, column=0)

    def set_status(self, status):
        self.status_label.config(text=status)
        self.gui.update()
