#!/usr/bin/env python3

from PIL import Image, ImageTk
import tkinter.ttk as ttk
import tkinter as tk
import webbrowser
import requests
import time
import io
import os

STATUSES = {
    -2: {'name': 'Unknown', 'color': '#FFFFFF'},
    -1: {'name': 'In-Game', 'color': '#8CB359'},
    0: {'name': 'Offline', 'color': '#5E5B58'},
    1: {'name': 'Online', 'color': '#86B5D9'},
    2: {'name': 'Busy', 'color': '#86B5D9'},
    3: {'name': 'Away', 'color': '#86B5D9'},
    4: {'name': 'Snooze', 'color': '#86B5D9'},
    5: {'name': 'Looking to Trade', 'color': '#86B5D9'},
    6: {'name': 'Looking to Play', 'color': '#86B5D9'}
}
QUALITIES = {
    0: {'name': 'Normal', 'color': '#B2B2B2'},
    1: {'name': 'Genuine', 'color': '#4D7455'},
    3: {'name': 'Vintage', 'color': '#476291'},
    5: {'name': 'Unusual', 'color': '#8650AC'},
    6: {'name': 'Unique', 'color': '#FFD700'},
    7: {'name': 'Community', 'color': '#70B04A'},
    8: {'name': 'Valve', 'color': '#A50F79'},
    9: {'name': 'Self-Made', 'color': '#70B04A'},
    11: {'name': 'Strange', 'color': '#CF6A32'},
    13: {'name': 'Haunted', 'color': '#38F3AB'},
    14: {'name': 'Collectors', 'color': '#AA0000'},
    15: {'name': 'Decorated', 'color': '#FAFAFA'}
}


class GUI(tk.Tk):
    def __init__(self, process_manager):
        tk.Tk.__init__(self)
        self.process_manager = process_manager
        self.config = self.process_manager.config

        self.scan_notebook = None
        self.ids_input_frame = None
        self.ids_input_text = None
        self.ids_input_scrollbar = None
        self.ids_scan_button = None
        self.ids_progressbar = None
        self.ids_progress_label = None
        self.ids_output_canvas = None
        self.ids_output_scrollbar = None
        self.ids_output_button = None
        self.ids_options_frame = None
        self.ids_player_options_frame = None
        self.ids_output_options_frame = None
        self.ids_display_players_label = None
        self.ids_display_players_combobox = None
        self.ids_collect_hours_label = None
        self.ids_collect_hours_combobox = None
        self.ids_f2p_label = None
        self.ids_f2p_combobox = None
        self.ids_status_label = None
        self.ids_status_combobox = None
        self.ids_max_hours_label = None
        self.ids_max_hours_entry = None
        self.ids_minimum_player_value_label = None
        self.ids_minimum_player_value_entry = None
        self.ids_minimum_player_value_currency_combobox = None
        self.ids_last_online_label = None
        self.ids_last_online_entry = None
        self.ids_currency_label = None
        self.ids_currency_combobox = None
        self.ids_minimum_item_value_label = None
        self.ids_minimum_item_value_entry = None
        self.ids_minimum_item_value_currency_combobox = None
        self.ids_displayed_items_label = None
        self.ids_displayed_items_entry = None
        self.ids_image_size_label = None
        self.ids_image_size_entry = None
        self.ids_font_size_label = None
        self.ids_font_size_entry = None
        self.ids_technical_options_frame = None
        self.ids_limit_requests_label = None
        self.ids_limit_requests_combobox = None
        self.ids_request_period_label = None
        self.ids_request_period_entry = None
        self.ids_requests_per_period_label = None
        self.ids_requests_per_period_entry = None
        self.ids_simultaneous_scans_label = None
        self.ids_simultaneous_scans_entry = None
        self.ids_options_button = None

        # Technical
        self.text_height = None
        self.text_width = None
        self.default_avatar = None

        self.resizable(width=False, height=True)

        self.protocol('WM_DELETE_WINDOW', self.process_manager.end)
        self.title('Scanner')
        self.iconbitmap('Resources/Icon.ico')

        self.grid_rowconfigure(1, weight=1)

        # Input
        self.shark = ImageTk.PhotoImage(Image.open('Resources/Shark.jpg').resize((421, 26), Image.ANTIALIAS))
        self.xshark = ImageTk.PhotoImage(Image.open('Resources/XShark.jpg').resize((421, 26), Image.ANTIALIAS))
        self.up = ImageTk.PhotoImage(Image.open('Resources/Up.png').resize((10, 10), Image.ANTIALIAS))
        self.down = ImageTk.PhotoImage(Image.open('Resources/Down.png').resize((10, 10), Image.ANTIALIAS))

        self.create_scan_notebook()
        self.create_ids_tab()

        credits_frame = tk.Frame(self)
        credits_frame.grid(row=2, column=0, sticky='w')
        powered_by = tk.Label(credits_frame, text='Powered by ')
        powered_by.pack(side='left')
        steam = tk.Label(credits_frame, text='Steam', fg='blue', cursor='hand2')
        steam.bind('<Button-1>', lambda event: webbrowser.open('http://steampowered.com'))
        steam.pack(side='left')
        and_label = tk.Label(credits_frame, text=' and ')
        and_label.pack(side='left')
        backpack_tf = tk.Label(credits_frame, text='Backpack.tf', fg='blue', cursor='hand2')
        backpack_tf.bind('<Button-1>', lambda event: webbrowser.open('http://backpack.tf'))
        backpack_tf.pack(side='left')

        self.update_ids_options()

        self.images = {}
        self.particle_effects = {}
        self.ids_players = {}

        self.name_to_canvas = {
            'ids': self.ids_output_canvas
        }
        self.name_to_dict = {
            'ids': self.ids_players
        }
        self.canvas_to_name = {
            self.ids_output_canvas: 'ids'
        }

        self.update_images()

    def create_scan_notebook(self):
        self.scan_notebook = ttk.Notebook(self)
        self.scan_notebook.grid(row=1, column=0, sticky='nsew')

    def create_ids_tab(self):
        self.ids_input_frame = tk.Frame()
        self.ids_input_frame.grid_rowconfigure(2, weight=1)
        self.ids_input_frame.grid_columnconfigure(3, weight=1)

        self.ids_input_text = tk.Text(self.ids_input_frame, width=51)
        self.ids_input_text.grid(row=2, column=0, sticky='ns')

        self.ids_input_scrollbar = ttk.Scrollbar(self.ids_input_frame, command=self.ids_input_text.yview)
        self.ids_input_text.config(yscrollcommand=self.ids_input_scrollbar.set)
        self.ids_input_scrollbar.grid(row=2, column=1, sticky='ns')

        self.ids_scan_button = ttk.Button(self.ids_input_frame, image=self.shark,
                                          command=self.process_manager.start_ids_scan)
        self.ids_scan_button.grid(row=3, column=0, columnspan=2, sticky='ew')

        self.ids_progressbar = ttk.Progressbar(self.ids_input_frame)
        self.ids_progressbar.grid(row=4, column=0, columnspan=2, sticky='ew')

        self.ids_progress_label = tk.Label(self.ids_input_frame)
        self.ids_progress_label.grid(row=5, column=0, columnspan=2, sticky='w')

        # Output
        self.ids_output_canvas = tk.Canvas(self.ids_input_frame, scrollregion=(0, 0, 0, 0), relief='ridge',
                                           bg='#999999', bd=2, highlightthickness=0)
        self.ids_output_canvas.bind('<MouseWheel>', lambda event: self.ids_output_canvas.yview_scroll(
            int(-event.delta / 120), 'units'))
        self.ids_output_canvas.bind('<Button-2>', self.event_clear_output)
        self.ids_output_scrollbar = ttk.Scrollbar(self.ids_input_frame, command=self.ids_output_canvas.yview)
        self.ids_output_canvas.config(yscrollcommand=self.ids_output_scrollbar.set)
        self.ids_output_canvas.grid(row=0, column=3, rowspan=6, sticky='nsew')
        self.ids_output_scrollbar.grid(row=0, column=4, rowspan=6, sticky='ns')

        self.ids_output_button = ttk.Button(self.ids_input_frame, text='«', command=self.hide_output, width=1)
        self.ids_output_button.grid(row=0, column=2, rowspan=6, sticky='ns')

        # Options
        self.ids_options_frame = tk.Frame(self.ids_input_frame)

        # Player Options
        self.ids_player_options_frame = tk.LabelFrame(self.ids_options_frame, text='Players')
        self.ids_player_options_frame.grid_columnconfigure(0, weight=1)
        self.ids_player_options_frame.grid(row=0, column=0, sticky='nsew')

        self.ids_output_options_frame = tk.LabelFrame(self.ids_options_frame, text='Output')
        self.ids_output_options_frame.grid(row=1, column=1, sticky='nsew')

        self.ids_display_players_label = tk.Label(self.ids_player_options_frame, text='Display Players: ')
        self.ids_display_players_label.grid(row=0, column=0, sticky='w')

        self.ids_display_players_combobox = ttk.Combobox(self.ids_player_options_frame, state='readonly', width=4,
                                                         values=('True', 'False'))
        self.ids_display_players_combobox.set(self.config['ids']['display_players'])
        self.ids_display_players_combobox.grid(row=0, column=1, sticky='ew', columnspan=2)

        self.ids_collect_hours_label = tk.Label(self.ids_player_options_frame, text='Collect Hours: ')
        self.ids_collect_hours_label.grid(row=1, column=0, sticky='w')

        self.ids_collect_hours_combobox = ttk.Combobox(self.ids_player_options_frame, state='readonly', width=5,
                                                       values=('True', 'False'))
        self.ids_collect_hours_combobox.set(self.config['ids']['collect_hours'])
        self.ids_collect_hours_combobox.grid(row=1, column=1, sticky='ew', columnspan=2)

        self.ids_f2p_label = tk.Label(self.ids_player_options_frame, text='F2P: ')
        self.ids_f2p_label.grid(row=2, column=0, sticky='w')

        self.ids_f2p_combobox = ttk.Combobox(self.ids_player_options_frame, state='readonly', width=4,
                                             values=('Both', 'True', 'False'))
        self.ids_f2p_combobox.set(self.config['ids']['f2p'])
        self.ids_f2p_combobox.grid(row=2, column=1, sticky='ew', columnspan=2)

        self.ids_status_label = tk.Label(self.ids_player_options_frame, text='Status: ')
        self.ids_status_label.grid(row=4, column=0, sticky='w')

        self.ids_status_combobox = ttk.Combobox(self.ids_player_options_frame, state='readonly', width=11,
                                                values=('Offline', 'Semi-Online', 'Online', 'In-Game'))
        self.ids_status_combobox.set(self.config['ids']['status'])
        self.ids_status_combobox.grid(row=4, column=1, sticky='ew', columnspan=2)

        self.ids_max_hours_label = tk.Label(self.ids_player_options_frame, text='Max Hours: ')
        self.ids_max_hours_label.grid(row=5, column=0, sticky='w')

        self.ids_max_hours_entry = ttk.Entry(self.ids_player_options_frame, width=14)
        self.ids_max_hours_entry.insert(0, self.config['ids']['max_hours'])
        self.ids_max_hours_entry.grid(row=5, column=1, sticky='ew', columnspan=2)
        
        self.ids_minimum_player_value_label = tk.Label(self.ids_player_options_frame, text='Min Player Value: ')
        self.ids_minimum_player_value_label.grid(row=6, column=0, sticky='w')

        self.ids_minimum_player_value_entry = ttk.Entry(self.ids_player_options_frame, width=5)
        self.ids_minimum_player_value_entry.insert(0, self.config['ids']['minimum_player_value'])
        self.ids_minimum_player_value_entry.grid(row=6, column=1, sticky='w')

        self.ids_minimum_player_value_currency_combobox = ttk.Combobox(self.ids_player_options_frame, state='readonly',
                                                                       width=7, values=('Keys', 'Refined', 'USD'))
        self.ids_minimum_player_value_currency_combobox.set(self.config['ids']['minimum_player_value_currency'])
        self.ids_minimum_player_value_currency_combobox.grid(row=6, column=2, sticky='ew')

        self.ids_last_online_label = tk.Label(self.ids_player_options_frame, text='Last Online (M-D-Y): ')
        self.ids_last_online_label.grid(row=7, column=0, sticky='w')

        self.ids_last_online_entry = ttk.Entry(self.ids_player_options_frame, width=14)
        self.ids_last_online_entry.insert(0, self.config['ids']['last_online'])
        self.ids_last_online_entry.grid(row=7, column=1, sticky='ew', columnspan=2)

        # Output Options
        self.ids_currency_label = tk.Label(self.ids_output_options_frame, text='Currency: ')
        self.ids_currency_label.grid(row=0, column=0, sticky='w')

        self.ids_currency_combobox = ttk.Combobox(self.ids_output_options_frame, state='readonly', width=7,
                                                  values=('Default', 'Keys', 'Refined', 'USD'))
        self.ids_currency_combobox.set(self.config['ids']['currency'])
        self.ids_currency_combobox.grid(row=0, column=1, sticky='ew', columnspan=2)

        self.ids_minimum_item_value_label = tk.Label(self.ids_output_options_frame, text='Min Item Value: ')
        self.ids_minimum_item_value_label.grid(row=1, column=0, sticky='w')

        self.ids_minimum_item_value_entry = ttk.Entry(self.ids_output_options_frame, width=5)
        self.ids_minimum_item_value_entry.insert(0, self.config['ids']['minimum_item_value'])
        self.ids_minimum_item_value_entry.grid(row=1, column=1, sticky='w')

        self.ids_minimum_item_value_currency_combobox = ttk.Combobox(self.ids_output_options_frame, state='readonly',
                                                                     width=7, values=('Keys', 'Refined', 'USD'))
        self.ids_minimum_item_value_currency_combobox.set(self.config['ids']['minimum_item_value_currency'])
        self.ids_minimum_item_value_currency_combobox.grid(row=1, column=2, sticky='ew')

        self.ids_displayed_items_label = tk.Label(self.ids_output_options_frame, text='Displayed Items: ')
        self.ids_displayed_items_label.grid(row=2, column=0, sticky='w')

        self.ids_displayed_items_entry = ttk.Entry(self.ids_output_options_frame, width=16)
        self.ids_displayed_items_entry.insert(0, self.config['output']['displayed_items'])
        self.ids_displayed_items_entry.grid(row=2, column=1, sticky='w', columnspan=2)

        self.ids_image_size_label = tk.Label(self.ids_output_options_frame, text='Image Size: ')
        self.ids_image_size_label.grid(row=3, column=0, sticky='w')

        self.ids_image_size_entry = ttk.Entry(self.ids_output_options_frame, width=16)
        self.ids_image_size_entry.insert(0, self.config['output']['image_size'])
        self.ids_image_size_entry.grid(row=3, column=1, sticky='w', columnspan=2)

        self.ids_font_size_label = tk.Label(self.ids_output_options_frame, text='Font Size: ')
        self.ids_font_size_label.grid(row=4, column=0, sticky='w')

        self.ids_font_size_entry = ttk.Entry(self.ids_output_options_frame, width=16)
        self.ids_font_size_entry.insert(0, self.config['output']['font_size'])
        self.ids_font_size_entry.grid(row=4, column=1, sticky='w', columnspan=2)

        # Technical Options
        self.ids_technical_options_frame = tk.LabelFrame(self.ids_options_frame, text='Technical')
        self.ids_technical_options_frame.grid(row=1, column=0, sticky='nsew')

        self.ids_limit_requests_label = tk.Label(self.ids_technical_options_frame, text='Limit Requests: ')
        self.ids_limit_requests_label.grid(row=0, column=0, sticky='w')

        self.ids_limit_requests_combobox = ttk.Combobox(self.ids_technical_options_frame, state='readonly', width=5,
                                                        values=('True', 'False'))
        self.ids_limit_requests_combobox.set(self.config['technical']['limit_requests'])
        self.ids_limit_requests_combobox.grid(row=0, column=1, sticky='ew')

        self.ids_request_period_label = tk.Label(self.ids_technical_options_frame, text='Request Period: ')
        self.ids_request_period_label.grid(row=1, column=0, sticky='w')

        self.ids_request_period_entry = ttk.Entry(self.ids_technical_options_frame, width=14)
        self.ids_request_period_entry.insert(0, self.config['technical']['request_period'])
        self.ids_request_period_entry.grid(row=1, column=1, sticky='w')

        self.ids_requests_per_period_label = tk.Label(self.ids_technical_options_frame, text='Requests Per Period: ')
        self.ids_requests_per_period_label.grid(row=2, column=0, sticky='w')

        self.ids_requests_per_period_entry = ttk.Entry(self.ids_technical_options_frame, width=14)
        self.ids_requests_per_period_entry.insert(0, self.config['technical']['requests_per_period'])
        self.ids_requests_per_period_entry.grid(row=2, column=1, sticky='w')

        self.ids_simultaneous_scans_label = tk.Label(self.ids_technical_options_frame, text='Simultaneous Scans: ')
        self.ids_simultaneous_scans_label.grid(row=3, column=0, sticky='w')

        self.ids_simultaneous_scans_entry = ttk.Entry(self.ids_technical_options_frame, width=14)
        self.ids_simultaneous_scans_entry.insert(0, self.config['technical']['simultaneous_scans'])
        self.ids_simultaneous_scans_entry.grid(row=3, column=1, sticky='w')

        self.ids_options_button = ttk.Button(self.ids_input_frame, image=self.down, command=self.display_ids_options)
        self.ids_options_button.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.scan_notebook.add(self.ids_input_frame, text='IDs')

    def display_output(self):
        self.ids_output_canvas.grid(row=0, column=3, rowspan=6, sticky='nsew')
        self.ids_output_scrollbar.grid(row=0, column=4, rowspan=6, sticky='ns')

        self.ids_output_button.config(command=self.hide_output, text='«')

    def hide_output(self):
        self.ids_output_canvas.grid_remove()
        self.ids_output_scrollbar.grid_remove()

        self.ids_output_button.config(command=self.display_output, text='»')

    def display_ids_options(self):
        self.ids_displayed_items_entry.delete(0, 'end')
        self.ids_displayed_items_entry.insert(0, int(self.config['output']['displayed_items']))
        self.ids_image_size_entry.delete(0, 'end')
        self.ids_image_size_entry.insert(0, int(self.config['output']['image_size']))
        self.ids_font_size_entry.delete(0, 'end')
        self.ids_font_size_entry.insert(0, int(self.config['output']['font_size']))

        self.ids_limit_requests_combobox.set(str(self.config['technical']['limit_requests']))
        self.ids_request_period_entry.delete(0, 'end')
        self.ids_request_period_entry.insert(0, int(self.config['technical']['request_period']))
        self.ids_requests_per_period_entry.delete(0, 'end')
        self.ids_requests_per_period_entry.insert(0, int(self.config['technical']['requests_per_period']))
        self.ids_simultaneous_scans_entry.delete(0, 'end')
        self.ids_simultaneous_scans_entry.insert(0, self.config['technical']['simultaneous_scans'])

        self.ids_options_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.ids_options_button.config(image=self.up, command=self.hide_ids_options)

    def hide_ids_options(self):
        self.ids_options_frame.grid_remove()
        self.ids_options_button.config(image=self.down, command=self.display_ids_options)
        self.update_ids_options()

    def check_entry_integer(self, entry, default):
        if not entry.get().isdigit():
            entry.delete(0, 'end')
            entry.insert(0, default)

    def check_entry_float(self, entry, default):
        try:
            float(entry.get())
        except ValueError:
            entry.delete(0, 'end')
            entry.insert(0, default)

    def update_ids_options(self):
        self.config['ids']['display_players'] = self.ids_display_players_combobox.get()

        self.config['ids']['collect_hours'] = self.ids_collect_hours_combobox.get()

        self.config['ids']['f2p'] = self.ids_f2p_combobox.get()

        self.config['ids']['status'] = self.ids_status_combobox.get()

        if self.ids_max_hours_entry.get():
            self.check_entry_integer(self.ids_max_hours_entry, self.config['ids']['max_hours'])
        self.config['ids']['max_hours'] = self.ids_max_hours_entry.get()
            
        if self.ids_minimum_player_value_entry.get():
            self.check_entry_float(self.ids_minimum_player_value_entry, self.config['ids']['minimum_player_value'])
        self.config['ids']['minimum_player_value'] = self.ids_minimum_player_value_entry.get()

        self.config['ids']['minimum_player_value_currency'] = self.ids_minimum_player_value_currency_combobox.get()

        if self.config['ids']['minimum_player_value']:
            if self.config['ids']['minimum_player_value_currency'] == 'Refined':
                self.config['ids']['raw_minimum_player_value'] = self.config['ids']['minimum_player_value']
            elif self.config['ids']['minimum_player_value_currency'] == 'Keys':
                self.config['ids']['raw_minimum_player_value'] = (str(
                    float(self.config['ids']['minimum_player_value']) * self.process_manager.key_price))
            elif self.config['ids']['minimum_player_value_currency'] == 'USD':
                self.config['ids']['raw_minimum_player_value'] = (str(
                    float(self.config['ids']['minimum_player_value']) / self.process_manager.refined_price))
        else:
            self.config['ids']['raw_minimum_player_value'] = '0'

        if self.ids_last_online_entry.get():
            try:
                raw_last_online = time.mktime(time.strptime(self.ids_last_online_entry.get(), '%m-%d-%y'))
                self.config['ids']['raw_last_online'] = str(raw_last_online)
            except ValueError:
                self.ids_last_online_entry.delete(0, 'end')
                self.ids_last_online_entry.insert(0, self.config['ids']['last_online'])
        else:
            self.config['ids']['raw_last_online'] = '0'
        self.config['ids']['last_online'] = self.ids_last_online_entry.get()

        self.config['ids']['currency'] = self.ids_currency_combobox.get()

        if self.ids_minimum_item_value_entry.get():
            self.check_entry_float(self.ids_minimum_item_value_entry, self.config['ids']['minimum_item_value'])
        self.config['ids']['minimum_item_value'] = self.ids_minimum_item_value_entry.get()

        self.config['ids']['minimum_item_value_currency'] = self.ids_minimum_item_value_currency_combobox.get()

        if self.config['ids']['minimum_item_value']:
            if self.config['ids']['minimum_item_value_currency'] == 'Refined':
                self.config['ids']['raw_minimum_item_value'] = self.config['ids']['minimum_item_value']
            elif self.config['ids']['minimum_item_value_currency'] == 'Keys':
                self.config['ids']['raw_minimum_item_value'] = (str(float(self.config['ids']['minimum_item_value']) *
                                                                    self.process_manager.key_price))
            elif self.config['ids']['minimum_item_value_currency'] == 'USD':
                self.config['ids']['raw_minimum_item_value'] = (str(float(self.config['ids']['minimum_item_value']) /
                                                                    self.process_manager.refined_price))
        else:
            self.config['ids']['raw_minimum_item_value'] = '0'

        self.check_entry_integer(self.ids_displayed_items_entry, self.config['output']['displayed_items'])
        if self.ids_displayed_items_entry.get() != self.config['output']['displayed_items']:
            self.config['output']['displayed_items'] = self.ids_displayed_items_entry.get()
            self.clear_output('ids')

        self.check_entry_integer(self.ids_image_size_entry, self.config['output']['image_size'])
        if self.ids_image_size_entry.get() != self.config['output']['image_size']:
            self.config['output']['image_size'] = self.ids_image_size_entry.get()
            self.clear_output('ids')
            self.update_images()

        self.check_entry_integer(self.ids_font_size_entry, self.config['output']['font_size'])
        if self.ids_font_size_entry.get() != self.config['output']['font_size']:
            self.config['output']['font_size'] = self.ids_font_size_entry.get()
            self.clear_output('ids')

        self.config['technical']['limit_requests'] = str(self.ids_limit_requests_combobox.get() == 'True')

        self.check_entry_integer(self.ids_request_period_entry, self.config['technical']['request_period'])
        self.config['technical']['request_period'] = self.ids_request_period_entry.get()

        self.check_entry_integer(self.ids_requests_per_period_entry, self.config['technical']['requests_per_period'])
        self.config['technical']['requests_per_period'] = self.ids_requests_per_period_entry.get()

        self.check_entry_integer(self.ids_simultaneous_scans_entry, self.config['technical']['simultaneous_scans'])
        self.config['technical']['simultaneous_scans'] = self.ids_simultaneous_scans_entry.get()

        test_text = self.ids_output_canvas.create_text(0, 0, text='0', anchor='nw',
                                                       font=('Helvetica', int(self.config['output']['font_size'])))
        self.text_height = self.ids_output_canvas.bbox(test_text)[3]
        self.text_width = self.ids_output_canvas.bbox(test_text)[2] - self.ids_output_canvas.bbox(test_text)[0]
        self.ids_output_canvas.delete(test_text)

        self.ids_output_canvas.config(width=self.text_width + int(self.config['output']['image_size']) * (
            int(self.config['output']['displayed_items']) + 1 + 0.4))

    def update_images(self):
        image_size = int(self.config['output']['image_size'])
        for file_name in os.listdir('Resources/Items'):
            file_name = file_name.replace('.png', '')
            self.images[file_name] = ImageTk.PhotoImage(Image.open('Resources/Items/%s.png' % file_name).resize(
                (image_size, image_size), Image.ANTIALIAS))
        for file_name in os.listdir('Resources/Particle Effects'):
            file_name = file_name.replace('.png', '')
            self.particle_effects[file_name] = ImageTk.PhotoImage(
                Image.open('Resources/Particle Effects/%s.png' % file_name).resize(
                    (image_size, image_size), Image.ANTIALIAS))

        self.default_avatar = ImageTk.PhotoImage(Image.open('Resources/TF2 Logo.png').resize(
            (image_size, image_size), Image.ANTIALIAS))

    def display_player(self, name, player):
        minimum_value = {
            'ids': float(self.config['ids']['raw_minimum_item_value'])
        }[name]
        currency = {
            'ids': self.ids_currency_combobox.get()
        }[name]
        canvas = self.name_to_canvas[name]
        height = int(self.config['output']['image_size']) + self.text_height + 1

        if not player.avatar:
            player.avatarimage = self.default_avatar
        else:
            avatarimage = requests.get('http://' + player.avatar[8:])  # [8:] is to avoid certificate errors with ssl
            if avatarimage.status_code == 200:
                player.avatarimage = ImageTk.PhotoImage(Image.open(io.BytesIO(avatarimage.content)).resize(
                    (int(self.config['output']['image_size']), int(self.config['output']['image_size'])),
                    Image.ANTIALIAS))
            else:
                player.avatarimage = self.default_avatar

        # Player Name
        player_name = player.name.encode('ascii', 'ignore').decode()
        if player.last_online is not None:
            player_name += ' (%s)' % time.ctime(player.last_online)
        canvas.create_text(0, (-height), tags='player%s' % player.id64, text=player_name,
                           anchor='nw', font=('Helvetica', int(self.config['output']['font_size'])))

        # Hours
        hours = canvas.create_text(int(self.config['output']['image_size']) / 10 + 1, (-height) + self.text_height,
                                   tags='player%s' % player.id64,
                                   text='\n'.join(str(player.hours) if player.hours is not None else ' '),
                                   font=('Helvetica', int(self.config['output']['font_size'])), anchor='nw')
        canvas.tag_bind(hours, '<Button-1>', self.event_remove_player)

        # Status Box
        status_box = canvas.create_rectangle(int(self.config['output']['image_size']) / 10,
                                             (-height) + self.text_height,
                                             int(self.config['output']['image_size']) / 10 + self.text_width,
                                             (-height) + self.text_height + int(self.config['output']['image_size']),
                                             tags='player%s' % player.id64,
                                             fill=STATUSES[player.status]['color'])
        canvas.tag_lower(status_box)
        canvas.tag_bind(status_box, '<Button-1>', self.event_remove_player)

        # Player Avatar
        avatar = canvas.create_image((int(self.config['output']['image_size']) / 5) + self.text_width,
                                     (-height) + self.text_height, tags='player%s' % player.id64,
                                     image=player.avatarimage, anchor='nw')
        profile_link = 'http://steamcommunity.com/profiles/%s' % player.id64
        friends_link = 'steam://friends/add/%s' % player.id64
        canvas.tag_bind(avatar, '<Button-1>', lambda event: webbrowser.open(profile_link))
        canvas.tag_bind(avatar, '<Button-3>', lambda event: webbrowser.open(friends_link))

        sorted_items = sorted(player.items, key=lambda x: x.get_raw_price() or 0, reverse=True)

        for item, index in zip(sorted_items[:int(self.config['output']['displayed_items'])],
                               range(min(len(sorted_items), int(self.config['output']['displayed_items'])))):
            if item.get_raw_price():
                if item.get_raw_price() < minimum_value:
                    break

            item_x = self.text_width + (int(self.config['output']['image_size']) * (index + 1.3))
            item_y = (-height) + self.text_height

            description_text = ''
            description_text += '%s %s' % (QUALITIES[item.quality]['name'], item.get_name())
            description_text += '\n%s' % item.get_price(currency)
            if item.quality == 5:
                effect = item.get_price_index()
                if not effect == '0':
                    description_text += '\n%s' % self.process_manager.particle_effect_schema[int(effect)]['name']
            item_description = canvas.create_text(
                item_x + (int(self.config['output']['image_size']) / 2),
                item_y + (int(self.config['output']['image_size']) / 2),
                tags=('player%s' % player.id64,
                      'item_description-%s-%s' % (player.id64, index),
                      'item-%s-%s' % (player.id64, index)),
                text=description_text,
                font=('Helvetica', int(int(self.config['output']['font_size']) * 1.5)),
                justify='center',
                anchor='center')
            canvas.tag_bind(item_description, '<Button-1>', self.hide_description)

            description_bbox = canvas.bbox(item_description)
            if description_bbox[0] < 1:
                canvas.move(item_description, -description_bbox[0], 0)
            width = self.text_width + int(self.config['output']['image_size']) * (
                int(self.config['output']['displayed_items']) + 1 + 0.4)
            if description_bbox[2] > width:
                canvas.move(item_description, (width - description_bbox[2]), 0)
            item_description_box = canvas.create_rectangle(canvas.bbox(item_description),
                                                           tags=('player%s' % player.id64,
                                                                 'item_description_box-%s-%s' % (player.id64, index),
                                                                 'item-%s-%s' % (player.id64, index)),
                                                           fill='#FFFFFF')
            canvas.tag_bind(item_description_box, '<Button-1>', self.hide_description)

            canvas.itemconfig(item_description, state='hidden')
            canvas.itemconfig(item_description_box, state='hidden')

            # Item Box
            canvas.create_rectangle(item_x,
                                    item_y,
                                    item_x + int(self.config['output']['image_size']),
                                    item_y + int(self.config['output']['image_size']),
                                    tags='player%s' % player.id64, fill=QUALITIES[item.quality]['color'])

            # Unusual Effect
            if item.quality == 5:
                effect = item.get_price_index()
                if effect != '0':
                    canvas.create_image(item_x, item_y, tags='player%s' % player.id64,
                                        image=self.particle_effects[effect], anchor='nw')

            # Item Image
            file_name = item.get_name()
            file_name = file_name.replace('?', '')
            file_name = file_name.replace(':', '')
            item_image = canvas.create_image(item_x, item_y,
                                             tags=('player%s' % player.id64, 'item-%s-%s' % (player.id64, index)),
                                             image=self.images[file_name], anchor='nw')
            canvas.tag_bind(item_image, '<Button-1>', self.display_description)

            # Item Price
            item_price = canvas.create_text(item_x + 1, item_y + int(self.config['output']['image_size']) - 1,
                                            tags=('player%s' % player.id64, 'item-%s-%s' % (player.id64, index)),
                                            text=item.get_price(currency),
                                            font=('Helvetica', int(self.config['output']['font_size'])),
                                            anchor='sw')
            canvas.tag_bind(item_price, '<Button-1>', self.display_description)

            # Traded Marker
            if item.is_traded():
                traded_marker = canvas.create_line(item_x + int(self.config['output']['image_size']) / 2,
                                                   item_y + int(self.config['output']['image_size']) - 1,
                                                   item_x + int(self.config['output']['image_size']) - 1,
                                                   item_y + int(self.config['output']['image_size']) / 2,
                                                   tags=('player%s' % player.id64, 'item-%s-%s' % (player.id64, index)),
                                                   width=2,
                                                   fill='#00FFFF')
                canvas.tag_bind(traded_marker, '<Button-1>', self.display_description)

            # Non-Craftable Marker
            if not item.craftable:
                craftable_marker = canvas.create_line(item_x + int(self.config['output']['image_size']) * (3 / 4),
                                                      item_y + int(self.config['output']['image_size']) - 1,
                                                      item_x + int(self.config['output']['image_size']) - 1,
                                                      item_y + int(self.config['output']['image_size']) * (3 / 4),
                                                      tags=('player%s' % player.id64,
                                                            'item-%s-%s' % (player.id64, index)),
                                                      width=2,
                                                      fill='#FFFFFF')
                canvas.tag_bind(craftable_marker, '<Button-1>', self.display_description)

            # Non-Tradable marker
            if not item.tradable:
                tradable_marker = canvas.create_line(item_x + 1,
                                                     item_y + int(self.config['output']['image_size']) / 4,
                                                     item_x + int(self.config['output']['image_size']) / 4,
                                                     item_y + 1,
                                                     tags=('player%s' % player.id64,
                                                           'item-%s-%s' % (player.id64, index)),
                                                     width=2,
                                                     fill='#FF0000')
                canvas.tag_bind(tradable_marker, '<Button-1>', self.display_description)

            canvas.tag_raise(item_price)

        player_dict = self.name_to_dict[name]
        player.index = len(player_dict)
        player.done = False
        player_dict[player.id64] = player
        canvas.move('player%s' % player.id64, 0, (player.index + 1) * height)
        player.done = True

        self.update_output_scrollregion(name)

    def display_description(self, event):
        tags = event.widget.gettags('current')
        _, id64, index = tags[1].split('-')
        event.widget.tag_raise('item_description_box-%s-%s' % (id64, index))
        event.widget.tag_raise('item_description-%s-%s' % (id64, index))
        event.widget.itemconfig('item_description_box-%s-%s' % (id64, index), state='normal')
        event.widget.itemconfig('item_description-%s-%s' % (id64, index), state='normal')

    def hide_description(self, event):
        tags = event.widget.gettags('current')
        _, id64, index = tags[2].split('-')
        event.widget.itemconfig('item_description_box-%s-%s' % (id64, index), state='hidden')
        event.widget.itemconfig('item_description-%s-%s' % (id64, index), state='hidden')

    def event_remove_player(self, event):
        id64 = int(event.widget.gettags('current')[0].replace('player', ''))
        name = self.canvas_to_name[event.widget]
        self.remove_player(name, id64)

    def remove_player(self, name, id64):
        canvas = self.name_to_canvas[name]
        player_dict = self.name_to_dict[name]
        player = player_dict[id64]
        canvas.delete('player%s' % id64)
        for remove_id64 in player_dict:
            remove_player = player_dict[remove_id64]
            if remove_player.index > player.index:
                while not remove_player.done:
                    time.sleep(0.01)
                canvas.move('player%s' % remove_player.id64, 0,
                            -(int(self.config['output']['image_size']) + self.text_height + 1))
                remove_player.index -= 1
        del player_dict[id64]
        self.update_output_scrollregion(name)

    def event_clear_output(self, event):
        self.clear_output(self.canvas_to_name[event.widget])

    def clear_output(self, name, steam_id64s=None):
        if steam_id64s is None:
            self.name_to_canvas[name].delete('all')
            self.name_to_dict[name] = {}
        else:
            for id64 in steam_id64s:
                if id64 in self.name_to_dict[name]:
                    self.remove_player(name, id64)
        self.update_output_scrollregion(name)

    def update_output_scrollregion(self, name):
        canvas = self.name_to_canvas[name]
        bbox = canvas.bbox('all')
        if not bbox:
            bbox = (0, 0, 0, 0)
        bbox_xpos1 = 0
        bbox_ypos1 = 0
        bbox_xpos2 = bbox[2] + int(self.config['output']['image_size']) / 10
        bbox_ypos2 = bbox[3] + int(self.config['output']['image_size']) / 10
        canvas.config(scrollregion=(bbox_xpos1, bbox_ypos1, bbox_xpos2, bbox_ypos2))
