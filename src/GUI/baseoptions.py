#!/usr/bin/env python3

import tkinter.ttk as ttk
import tkinter as tk
import time


class BaseOptions(tk.Toplevel):
    def __init__(self, tab):
        super().__init__()
        self.tab = tab

        self.title('Options')
        self.iconbitmap('Resources/Icon.ico')
        self.grid_columnconfigure(1, weight=1)

        self.category_listbox = tk.Listbox(self, selectmode='single')
        self.category_listbox.insert('end', 'Player', 'Output', 'Technical')
        self.category_listbox.grid(row=0, column=0, sticky='nsw')
        self.category_listbox.bind('<<ListboxSelect>>', self.display_category)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky='w')
        self.close_button = ttk.Button(self.button_frame, text='Close', command=self.withdraw)
        self.close_button.grid(row=0, column=0)
        self.apply_button = ttk.Button(self.button_frame, text='Apply', command=self.apply)
        self.apply_button.grid(row=0, column=1)
        self.default_button = ttk.Button(self.button_frame, text='Set as Defaults')
        self.default_button.grid(row=0, column=2)

        # Player Options
        self.player_options_frame = tk.LabelFrame(self, text='Player')

        self.display_players_label = tk.Label(self.player_options_frame, text='Display Players: ')
        self.display_players_label.grid(row=0, column=0, sticky='w')

        self.display_players_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=4,
                                                     values=('True', 'False'))
        self.display_players_combobox.set(self.tab.display_players)
        self.display_players_combobox.grid(row=0, column=1, sticky='ew', columnspan=2)

        self.collect_hours_label = tk.Label(self.player_options_frame, text='Collect Hours: ')
        self.collect_hours_label.grid(row=1, column=0, sticky='w')

        self.collect_hours_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=5,
                                                   values=('True', 'False'))
        self.collect_hours_combobox.set(self.tab.collect_hours)
        self.collect_hours_combobox.grid(row=1, column=1, sticky='ew', columnspan=2)

        self.f2p_label = tk.Label(self.player_options_frame, text='F2P: ')
        self.f2p_label.grid(row=2, column=0, sticky='w')

        self.f2p_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=4,
                                         values=('Both', 'True', 'False'))
        self.f2p_combobox.set(self.tab.f2p)
        self.f2p_combobox.grid(row=2, column=1, sticky='ew', columnspan=2)

        self.status_label = tk.Label(self.player_options_frame, text='Status: ')
        self.status_label.grid(row=3, column=0, sticky='w')

        self.status_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=11,
                                            values=('Offline', 'Semi-Online', 'Online', 'In-Game'))
        self.status_combobox.set(self.tab.status)
        self.status_combobox.grid(row=3, column=1, sticky='ew', columnspan=2)

        self.max_hours_label = tk.Label(self.player_options_frame, text='Max Hours: ')
        self.max_hours_label.grid(row=4, column=0, sticky='w')

        self.max_hours_entry = ttk.Entry(self.player_options_frame, width=14)
        self.max_hours_entry.insert(0, self.tab.max_hours)
        self.max_hours_entry.grid(row=4, column=1, sticky='ew', columnspan=2)

        self.minimum_player_value_label = tk.Label(self.player_options_frame, text='Min Player Value: ')
        self.minimum_player_value_label.grid(row=5, column=0, sticky='w')

        self.minimum_player_value_entry = ttk.Entry(self.player_options_frame, width=5)
        self.minimum_player_value_entry.insert(0, self.tab.minimum_player_value)
        self.minimum_player_value_entry.grid(row=5, column=1, sticky='w')

        self.minimum_player_value_currency_combobox = ttk.Combobox(self.player_options_frame, state='readonly',
                                                                   width=7, values=('Keys', 'Refined', 'USD'))
        self.minimum_player_value_currency_combobox.set(self.tab.minimum_player_value_currency)
        self.minimum_player_value_currency_combobox.grid(row=5, column=2, sticky='ew')

        self.last_online_label = tk.Label(self.player_options_frame, text='Last Online (M-D-Y): ')
        self.last_online_label.grid(row=6, column=0, sticky='w')

        self.last_online_entry = ttk.Entry(self.player_options_frame, width=14)
        self.last_online_entry.insert(0, self.tab.last_online)
        self.last_online_entry.grid(row=6, column=1, sticky='ew', columnspan=2)

        # Output Options
        self.output_options_frame = tk.LabelFrame(self, text='Output')

        self.currency_label = tk.Label(self.output_options_frame, text='Currency: ')
        self.currency_label.grid(row=0, column=0, sticky='w')

        self.currency_combobox = ttk.Combobox(self.output_options_frame, state='readonly', width=7,
                                              values=('Default', 'Keys', 'Refined', 'USD'))
        self.currency_combobox.set(self.tab.currency)
        self.currency_combobox.grid(row=0, column=1, sticky='ew', columnspan=2)

        self.minimum_item_value_label = tk.Label(self.output_options_frame, text='Min Item Value: ')
        self.minimum_item_value_label.grid(row=1, column=0, sticky='w')

        self.minimum_item_value_entry = ttk.Entry(self.output_options_frame, width=5)
        self.minimum_item_value_entry.insert(0, self.tab.minimum_item_value)
        self.minimum_item_value_entry.grid(row=1, column=1, sticky='w')

        self.minimum_item_value_currency_combobox = ttk.Combobox(self.output_options_frame, state='readonly', width=7,
                                                                 values=('Keys', 'Refined', 'USD'))
        self.minimum_item_value_currency_combobox.set(self.tab.minimum_item_value_currency)
        self.minimum_item_value_currency_combobox.grid(row=1, column=2, sticky='ew')

        self.displayed_items_label = tk.Label(self.output_options_frame, text='Displayed Items: ')
        self.displayed_items_label.grid(row=2, column=0, sticky='w')

        self.displayed_items_entry = ttk.Entry(self.output_options_frame, width=16)
        self.displayed_items_entry.insert(0, self.tab.process_manager.config['output']['displayed_items'])
        self.displayed_items_entry.grid(row=2, column=1, sticky='w', columnspan=2)

        self.items_per_line_label = tk.Label(self.output_options_frame, text='Items Per Line')
        self.items_per_line_label.grid(row=3, column=0, sticky='w')

        self.items_per_line_entry = ttk.Entry(self.output_options_frame, width=16)
        self.items_per_line_entry.insert(0, self.tab.process_manager.config['output']['items_per_line'])
        self.items_per_line_entry.grid(row=3, column=1, columnspan=2)

        self.image_size_label = tk.Label(self.output_options_frame, text='Image Size: ')
        self.image_size_label.grid(row=4, column=0, sticky='w')

        self.image_size_entry = ttk.Entry(self.output_options_frame, width=16)
        self.image_size_entry.insert(0, self.tab.process_manager.config['output']['image_size'])
        self.image_size_entry.grid(row=4, column=1, sticky='w', columnspan=2)

        self.font_size_label = tk.Label(self.output_options_frame, text='Font Size: ')
        self.font_size_label.grid(row=5, column=0, sticky='w')

        self.font_size_entry = ttk.Entry(self.output_options_frame, width=16)
        self.font_size_entry.insert(0, self.tab.process_manager.config['output']['font_size'])
        self.font_size_entry.grid(row=5, column=1, sticky='w', columnspan=2)

        # Technical Options
        self.technical_options_frame = tk.LabelFrame(self, text='Technical')

        self.display_avatars_label = tk.Label(self.technical_options_frame, text='Display Avatars: ')
        self.display_avatars_label.grid(row=0, column=0, sticky='w')

        self.display_avatars_combobox = ttk.Combobox(self.technical_options_frame, state='readonly', width=5,
                                                     values=('True', 'False'))
        self.display_avatars_combobox.set(self.tab.process_manager.config['technical']['display_avatars'])
        self.display_avatars_combobox.grid(row=0, column=1, sticky='ew')

        self.limit_requests_label = tk.Label(self.technical_options_frame, text='Limit Requests: ')
        self.limit_requests_label.grid(row=1, column=0, sticky='w')

        self.limit_requests_combobox = ttk.Combobox(self.technical_options_frame, state='readonly', width=5,
                                                    values=('True', 'False'))
        self.limit_requests_combobox.set(self.tab.process_manager.config['technical']['limit_requests'])
        self.limit_requests_combobox.grid(row=1, column=1, sticky='ew')

        self.request_period_label = tk.Label(self.technical_options_frame, text='Request Period: ')
        self.request_period_label.grid(row=2, column=0, sticky='w')

        self.request_period_entry = ttk.Entry(self.technical_options_frame, width=14)
        self.request_period_entry.insert(0, self.tab.process_manager.config['technical']['request_period'])
        self.request_period_entry.grid(row=2, column=1, sticky='w')

        self.requests_per_period_label = tk.Label(self.technical_options_frame, text='Requests Per Period: ')
        self.requests_per_period_label.grid(row=3, column=0, sticky='w')

        self.requests_per_period_entry = ttk.Entry(self.technical_options_frame, width=14)
        self.requests_per_period_entry.insert(0, self.tab.process_manager.config['technical']['requests_per_period'])
        self.requests_per_period_entry.grid(row=3, column=1, sticky='w')

        self.simultaneous_scans_label = tk.Label(self.technical_options_frame, text='Simultaneous Scans: ')
        self.simultaneous_scans_label.grid(row=4, column=0, sticky='w')

        self.simultaneous_scans_entry = ttk.Entry(self.technical_options_frame, width=14)
        self.simultaneous_scans_entry.insert(0, self.tab.process_manager.config['technical']['simultaneous_scans'])
        self.simultaneous_scans_entry.grid(row=4, column=1, sticky='w')

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

    def apply(self):
        # Player
        self.tab.display_players = self.display_players_combobox.get()
        self.tab.collect_hours = self.collect_hours_combobox.get()
        self.tab.f2p = self.f2p_combobox.get()
        self.tab.status = self.status_combobox.get()

        if self.max_hours_entry.get():
            self.check_entry_integer(self.max_hours_entry, self.tab.max_hours)
        self.tab.max_hours = self.max_hours_entry.get()

        if self.minimum_player_value_entry.get():
            self.check_entry_float(self.minimum_player_value_entry, self.tab.minimum_player_value)
        self.tab.minimum_player_value = self.minimum_player_value_entry.get()

        self.tab.minimum_player_value_currency = self.minimum_player_value_currency_combobox.get()

        if self.tab.minimum_player_value:
            if self.tab.minimum_player_value_currency == 'Refined':
                self.tab.raw_minimum_player_value = self.tab.minimum_player_value
            elif self.tab.minimum_player_value_currency == 'Keys':
                self.tab.raw_minimum_player_value = str(float(self.tab.minimum_player_value) *
                                                        self.tab.process_manager.key_price)
            elif self.tab.minimum_player_value_currency == 'USD':
                self.tab.raw_minimum_player_value = str(float(self.tab.minimum_player_value) /
                                                        self.tab.process_manager.refined_price)
        else:
            self.tab.raw_minimum_player_value = '0'

        if self.last_online_entry.get():
            try:
                raw_last_online = time.mktime(time.strptime(self.last_online_entry.get(), '%m-%d-%y'))
                self.tab.raw_last_online = str(raw_last_online)
            except ValueError:
                self.last_online_entry.delete(0, 'end')
                self.last_online_entry.insert(0, self.tab.last_online)
        else:
            self.tab.raw_last_online = '0'
        self.tab.last_online = self.last_online_entry.get()

        # Output
        self.tab.currency = self.currency_combobox.get()

        if self.minimum_item_value_entry.get():
            self.check_entry_float(self.minimum_item_value_entry, self.tab.minimum_item_value)
        self.tab.minimum_item_value = self.minimum_item_value_entry.get()

        self.tab.minimum_item_value_currency = self.minimum_item_value_currency_combobox.get()

        if self.tab.minimum_item_value:
            if self.tab.minimum_item_value_currency == 'Refined':
                self.tab.raw_minimum_item_value = self.tab.minimum_item_value
            elif self.tab.minimum_item_value_currency == 'Keys':
                self.tab.raw_minimum_item_value = (str(float(self.tab.minimum_item_value) *
                                                       self.tab.process_manager.key_price))
            elif self.tab.minimum_item_value_currency == 'USD':
                self.tab.raw_minimum_item_value = (str(float(self.tab.minimum_item_value) /
                                                       self.tab.process_manager.refined_price))
        else:
            self.tab.raw_minimum_item_value = '0'

        self.check_entry_integer(self.displayed_items_entry,
                                 self.tab.process_manager.config['output']['displayed_items'])
        self.tab.process_manager.config['output']['displayed_items'] = self.displayed_items_entry.get()

        self.check_entry_integer(self.items_per_line_entry, self.tab.process_manager.config['output']['items_per_line'])
        if self.items_per_line_entry.get() != self.tab.process_manager.config['output']['items_per_line']:
            self.tab.process_manager.config['output']['items_per_line'] = self.items_per_line_entry.get()
            self.tab.process_manager.gui.clear_tab_outputs()

        self.check_entry_integer(self.image_size_entry, self.tab.process_manager.config['output']['image_size'])
        if self.image_size_entry.get() != self.tab.process_manager.config['output']['image_size']:
            self.tab.process_manager.config['output']['image_size'] = self.image_size_entry.get()
            self.tab.process_manager.gui.clear_tab_outputs()
            self.tab.process_manager.gui.update_images()

        self.check_entry_integer(self.font_size_entry, self.tab.process_manager.config['output']['font_size'])
        if self.font_size_entry.get() != self.tab.process_manager.config['output']['font_size']:
            self.tab.process_manager.config['output']['font_size'] = self.font_size_entry.get()
            self.tab.process_manager.gui.clear_tab_outputs()

        # Technical
        self.tab.process_manager.config['technical']['display_avatars'] = self.display_avatars_combobox.get()

        self.tab.process_manager.config['technical']['limit_requests'] = self.limit_requests_combobox.get()

        self.check_entry_integer(self.request_period_entry,
                                 self.tab.process_manager.config['technical']['request_period'])
        self.tab.process_manager.config['technical']['request_period'] = self.request_period_entry.get()

        self.check_entry_integer(self.requests_per_period_entry,
                                 self.tab.process_manager.config['technical']['requests_per_period'])
        self.tab.process_manager.config['technical']['requests_per_period'] = self.requests_per_period_entry.get()

        self.check_entry_integer(self.simultaneous_scans_entry,
                                 self.tab.process_manager.config['technical']['simultaneous_scans'])
        self.tab.process_manager.config['technical']['simultaneous_scans'] = self.simultaneous_scans_entry.get()

        self.tab.process_manager.gui.update_tab_sizes()

    def set_as_default(self, name):
        self.apply()

        self.tab.process_manager.config[name]['display_players'] = self.tab.display_players
        self.tab.process_manager.config[name]['collect_hours'] = self.tab.collect_hours
        self.tab.process_manager.config[name]['f2p'] = self.tab.f2p
        self.tab.process_manager.config[name]['status'] = self.tab.status
        self.tab.process_manager.config[name]['max_hours'] = self.tab.max_hours
        self.tab.process_manager.config[name]['currency'] = self.tab.currency
        self.tab.process_manager.config[name]['minimum_item_value'] = self.tab.minimum_item_value
        self.tab.process_manager.config[name]['minimum_item_value_currency'] = self.tab.minimum_item_value_currency
        self.tab.process_manager.config[name]['raw_minimum_item_value'] = self.tab.raw_minimum_item_value
        self.tab.process_manager.config[name]['minimum_player_value'] = self.tab.minimum_player_value
        self.tab.process_manager.config[name]['minimum_player_value_currency'] = self.tab.minimum_player_value_currency
        self.tab.process_manager.config[name]['raw_minimum_player_value'] = self.tab.raw_minimum_player_value
        self.tab.process_manager.config[name]['last_online'] = self.tab.last_online
        self.tab.process_manager.config[name]['raw_last_online'] = self.tab.raw_last_online

        self.tab.process_manager.config.write(open('config.ini', 'w'))

    def display_category(self, event):
        selection = self.category_listbox.get(int(self.category_listbox.curselection()[0]))
        if selection == 'Player':
            self.output_options_frame.grid_remove()
            self.technical_options_frame.grid_remove()
            self.player_options_frame.grid(row=0, column=1, sticky='nsew')
        if selection == 'Output':
            self.technical_options_frame.grid_remove()
            self.player_options_frame.grid_remove()
            self.output_options_frame.grid(row=0, column=1, sticky='nsew')
        if selection == 'Technical':
            self.output_options_frame.grid_remove()
            self.player_options_frame.grid_remove()
            self.technical_options_frame.grid(row=0, column=1, sticky='nsew')
