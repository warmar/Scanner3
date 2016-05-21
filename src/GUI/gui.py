#!/usr/bin/env python3

from GUI import splash
from GUI import idstab
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import os


class GUI(tk.Tk):
    def __init__(self, process_manager):
        super().__init__()
        self.process_manager = process_manager
        self.config = self.process_manager.config

        self.resizable(width=False, height=True)
        self.protocol('WM_DELETE_WINDOW', self.process_manager.end)
        self.title('Scanner')
        self.iconbitmap('Resources/Icon.ico')
        self.grid_rowconfigure(0, weight=1)

        # Images
        self.shark = ImageTk.PhotoImage(Image.open('Resources/Shark.jpg').resize((421, 26), Image.ANTIALIAS))
        self.xshark = ImageTk.PhotoImage(Image.open('Resources/XShark.jpg').resize((421, 26), Image.ANTIALIAS))
        self.up = ImageTk.PhotoImage(Image.open('Resources/Up.png').resize((10, 10), Image.ANTIALIAS))
        self.down = ImageTk.PhotoImage(Image.open('Resources/Down.png').resize((10, 10), Image.ANTIALIAS))

        # Splash
        self.splash = splash.Splash(self)
        self.splash.grid(row=0, column=0)

        # Main Page
        self.main_frame = tk.Frame(self)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.tab_button = ttk.Button(self.main_frame, text='+', command=self.add_tab)
        self.tab_button.grid(row=0, column=0, sticky='w')

        self.scan_notebook = ttk.Notebook(self.main_frame)
        self.scan_notebook.grid(row=1, column=0, sticky='nsew')

        # Technical
        self.output_hidden = False

        self.tabs = []

        self.images = {}
        self.particle_effects = {}

    def main(self):
        self.splash.grid_remove()
        self.splash = None
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.mainloop()

    def add_tab(self):
        tab = idstab.IDsTab(self.process_manager)
        self.scan_notebook.add(tab, text='IDs')

        self.tabs.append(tab)
        self.scan_notebook.select(tab)
        if self.output_hidden:
            tab.output_canvas.grid_remove()
            tab.output_scrollbar.grid_remove()
            tab.output_button.config(text='»', command=self.display_output)
        self.update_tab_sizes()

    def update_tab_sizes(self):
        test_text = self.tabs[0].output_canvas.create_text(
            0, 0, text='0', anchor='nw', font=('Helvetica', int(self.config['output']['font_size'])))
        self.text_height = self.tabs[0].output_canvas.bbox(test_text)[3]
        self.text_width = self.tabs[0].output_canvas.bbox(test_text)[2] - self.tabs[0].output_canvas.bbox(test_text)[0]
        self.tabs[0].output_canvas.delete(test_text)
        for tab in self.tabs:
            tab.output_canvas.config(width=self.text_width + int(self.config['output']['image_size']) * (
                int(self.config['output']['displayed_items']) + 1 + 0.4))

    def clear_tab_outputs(self):
        for tab in self.tabs:
            tab.clear_output()

    def display_output(self):
        self.output_hidden = False
        for tab in self.tabs:
            tab.output_canvas.grid(row=0, column=3, rowspan=6)
            tab.output_scrollbar.grid(row=0, column=4, rowspan=6)
            tab.output_button.config(text='«', command=self.hide_output)

    def hide_output(self):
        self.output_hidden = True
        for tab in self.tabs:
            tab.output_canvas.grid_remove()
            tab.output_scrollbar.grid_remove()
            tab.output_button.config(text='»', command=self.display_output)

    def update_images(self):
        image_size = int(self.config['output']['image_size'])
        file_names = os.listdir('Resources/Items')
        particle_file_names = os.listdir('Resources/Particle Effects')

        total = len(file_names) + len(particle_file_names)
        done = 0

        def update_progress():
            nonlocal done
            done += 1
            if self.splash is not None:
                self.splash.set_status('Loading Images %s%%' % (int(done / total * 100)))

        for file_name in file_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/%s.png' % file_name).resize(
                (image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in particle_file_names:
            file_name = file_name.replace('.png', '')
            self.particle_effects[file_name] = ImageTk.PhotoImage(
                Image.open('Resources/Particle Effects/%s.png' % file_name).resize(
                    (image_size, image_size), Image.ANTIALIAS))
            update_progress()

        self.default_avatar = ImageTk.PhotoImage(Image.open('Resources/TF2 Logo.png').resize(
            (image_size, image_size), Image.ANTIALIAS))
