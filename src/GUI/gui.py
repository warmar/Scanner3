#!/usr/bin/env python3

import os
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

from PIL import Image, ImageTk

from GUI import splash, idstab


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

        # Splash
        self.splash = splash.Splash(self)
        self.splash.grid(row=0, column=0)

        # Main Page
        self.main_frame = tk.Frame(self)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.tab_frame = tk.Frame(self.main_frame)
        self.tab_frame.grid(row=0, column=0, sticky='ew')

        self.tab_button = ttk.Button(self.tab_frame, text='Add Tab', command=self.add_tab)
        self.tab_button.pack(side='left')

        self.scan_notebook = ttk.Notebook(self.main_frame)
        self.scan_notebook.grid(row=1, column=0, sticky='nsew')

        # Credits
        credits_frame = tk.Frame(self.main_frame)
        credits_frame.grid(row=2, column=0, sticky='ew')
        powered_by = tk.Label(credits_frame, text='Powered by ')
        powered_by.pack(side='left')
        steam = tk.Label(credits_frame, text='Steam', fg='blue', cursor='hand2')
        steam.bind('<Button-1>', lambda event: webbrowser.open('http://steampowered.com'))
        steam.pack(side='left')
        and_label = tk.Label(credits_frame, text=' and ')
        and_label.pack(side='left')
        backpack_tf = tk.Label(credits_frame, text='Backpack.tf', fg='blue', cursor='hand2')
        backpack_tf.bind('<Button-1>', lambda event: webbrowser.open('https://backpack.tf'))
        backpack_tf.pack(side='left')

        # About
        about_window = tk.Toplevel()
        about_window.title('ABOUT/COPYRIGHT')
        about_window.wm_withdraw()
        about_window.protocol('WM_DELETE_WINDOW', about_window.wm_withdraw)

        about_button = tk.Label(credits_frame, text='ABOUT/COPYRIGHT', fg='blue', cursor='hand2')
        about_button.bind('<Button-1>', lambda event: about_window.deiconify())
        about_button.pack(side='right')

        copyright_frame = tk.Frame(about_window)
        copyright_frame.grid(row=0, column=0, sticky='ew')
        about_label = tk.Label(copyright_frame, text='Copyright © 2016-2017 Peter Marangos ')
        about_label.grid(row=0, column=0)
        github_link_label = tk.Label(copyright_frame, text='www.github.com/warmar', fg='blue', cursor='hand2')
        github_link_label.bind('<Button-1>', lambda event: webbrowser.open('https://www.github.com/warmar'))
        github_link_label.grid(row=0, column=1)

        version_label = tk.Label(about_window, text='Version %s' % self.process_manager.version)
        version_label.grid(row=1, column=0, sticky='w')

        guide_frame = tk.Frame(about_window)
        guide_frame.grid(row=2, column=0, sticky='ew')
        guide_label = tk.Label(guide_frame, text='Usage Guide Available: ')
        guide_label.grid(row=0, column=0)
        guide_link = tk.Label(guide_frame, text='Link', fg='blue', cursor='hand2')
        guide_link.bind('<Button-1>', lambda event: webbrowser.open('https://raw.githubusercontent.com/warmar/Scanner3IDsOnly/master/Guide.pdf'))
        guide_link.grid(row=0, column=1)

        license_frame = tk.Frame(about_window)
        license_frame.grid(row=3, column=0, sticky='ew')
        license_label = tk.Label(license_frame, text='Licensed Under GNU General Public License: ')
        license_label.grid(row=0, column=0)
        license_link = tk.Label(license_frame, text='Link', fg='blue', cursor='hand2')
        license_link.bind('<Button-1>', lambda event: webbrowser.open('https://www.gnu.org/licenses/gpl-3.0.en.html'))
        license_link.grid(row=0, column=1)

        # Technical
        self.output_hidden = False

        self.tabs = []

        self.images = {}
        self.particle_effects = {}

    def start(self):
        self.splash.grid_remove()
        self.splash = None
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.add_tab()
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
            0,
            0,
            text='0',
            anchor='nw',
            font=('Helvetica', int(self.config['output']['font_size']))
        )
        self.text_height = self.tabs[0].output_canvas.bbox(test_text)[3]
        self.text_width = self.tabs[0].output_canvas.bbox(test_text)[2] - self.tabs[0].output_canvas.bbox(test_text)[0]
        self.tabs[0].output_canvas.delete(test_text)
        for tab in self.tabs:
            tab.output_canvas.config(width=self.text_width + int(self.config['output']['image_size']) * (int(self.config['output']['items_per_line']) + 1 + 0.4))

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
        regular_item_names = os.listdir('Resources/Items/Regular')
        australium_item_names = os.listdir('Resources/Items/Australium')
        paint_item_names = os.listdir('Resources/Items/Paint')
        skin_item_names = os.listdir('Resources/Items/Skins')
        festive_skin_item_names = os.listdir('Resources/Items/Festive Skins')
        particle_file_names = os.listdir('Resources/Particle Effects')

        total = len(regular_item_names)
        total += len(australium_item_names)
        total += len(paint_item_names)
        total += len(skin_item_names)
        total += len(festive_skin_item_names)
        total += len(particle_file_names)
        done = 0

        def update_progress():
            nonlocal done
            done += 1
            if self.splash is not None:
                self.splash.set_status('Loading Images %s%%' % (int(done / total * 100)))

        for file_name in regular_item_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/Regular/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in australium_item_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/Australium/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in paint_item_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/Paint/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in skin_item_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/Skins/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in festive_skin_item_names:
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/Festive Skins/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()
        for file_name in particle_file_names:
            file_name = file_name.replace('.png', '')
            self.particle_effects[file_name] = ImageTk.PhotoImage(Image.open('Resources/Particle Effects/%s.png' % file_name).resize((image_size, image_size), Image.ANTIALIAS))
            update_progress()

        self.default_avatar = ImageTk.PhotoImage(Image.open('Resources/TF2 Logo.png').resize((image_size, image_size), Image.ANTIALIAS))
