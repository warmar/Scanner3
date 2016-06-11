#!/usr/bin/env python3

from GUI import baseoptions
import tkinter.ttk as ttk
import tkinter as tk
import time


class IDsOptions(baseoptions.BaseOptions):
    def __init__(self, tab):
        super().__init__(tab)

        self.default_button.config(command=lambda: self.set_as_default('ids'))
