#!/usr/bin/env python3

import time
import tkinter as tk
import tkinter.ttk as ttk

from GUI import basetab
from Core.globals import WEARS


class BaseOptions(tk.Toplevel):
    def __init__(self, tab: basetab.BaseTab):
        super().__init__()
        self.tab = tab

        self.wm_withdraw()

        self.protocol('WM_DELETE_WINDOW', self.wm_withdraw)

        self.title('Options')
        self.iconbitmap('Resources/Icon.ico')
        self.grid_columnconfigure(1, weight=1)

        self.category_listbox = tk.Listbox(self, selectmode='single')
        self.category_listbox.insert('end', 'Player', 'Item', 'Output', 'Technical')
        self.category_listbox.grid(row=0, column=0, sticky='nsw')
        self.category_listbox.bind('<<ListboxSelect>>', self.display_category)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky='w')
        self.close_button = ttk.Button(self.button_frame, text='Close', command=self.wm_withdraw)
        self.close_button.grid(row=0, column=0)
        self.apply_button = ttk.Button(self.button_frame, text='Apply', command=self.apply)
        self.apply_button.grid(row=0, column=1)
        self.default_button = ttk.Button(self.button_frame, text='Set as Defaults', command=self.set_as_default)
        self.default_button.grid(row=0, column=2)

        # Player Options
        self.player_options_frame = tk.LabelFrame(self, text='Player')

        self.display_players_label = tk.Label(self.player_options_frame, text='Display Players: ')
        self.display_players_label.grid(row=0, column=0, sticky='w')

        self.display_players_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=4, values=('True', 'False'))
        self.display_players_combobox.set(self.tab.process_manager.config[self.tab.name]['display_players'])
        self.display_players_combobox.grid(row=0, column=1, sticky='ew')

        self.collect_hours_label = tk.Label(self.player_options_frame, text='Collect Hours: ')
        self.collect_hours_label.grid(row=1, column=0, sticky='w')

        self.collect_hours_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=5, values=('True', 'False'))
        self.collect_hours_combobox.set(self.tab.process_manager.config[self.tab.name]['collect_hours'])
        self.collect_hours_combobox.grid(row=1, column=1, sticky='ew')

        self.f2p_label = tk.Label(self.player_options_frame, text='F2P: ')
        self.f2p_label.grid(row=2, column=0, sticky='w')

        self.f2p_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=4, values=('Both', 'True', 'False'))
        self.f2p_combobox.set(self.tab.process_manager.config[self.tab.name]['f2p'])
        self.f2p_combobox.grid(row=2, column=1, sticky='ew')

        self.status_label = tk.Label(self.player_options_frame, text='Status: ')
        self.status_label.grid(row=4, column=0, sticky='w')

        self.status_combobox = ttk.Combobox(self.player_options_frame, state='readonly', width=11, values=('Offline', 'Semi-Online', 'Online', 'In-Game'))
        self.status_combobox.set(self.tab.process_manager.config[self.tab.name]['status'])
        self.status_combobox.grid(row=4, column=1, sticky='ew')

        self.max_hours_label = tk.Label(self.player_options_frame, text='Max Hours: ')
        self.max_hours_label.grid(row=5, column=0, sticky='w')

        self.max_hours_entry = ttk.Entry(self.player_options_frame, width=14)
        self.max_hours_entry.insert(0, self.tab.process_manager.config[self.tab.name]['max_hours'])
        self.max_hours_entry.grid(row=5, column=1, sticky='ew')

        self.last_online_label = tk.Label(self.player_options_frame, text='Last Online (M-D-Y): ')
        self.last_online_label.grid(row=6, column=0, sticky='w')

        self.last_online_entry = ttk.Entry(self.player_options_frame, width=14)
        self.last_online_entry.insert(0, self.tab.process_manager.config[self.tab.name]['last_online'])
        self.last_online_entry.grid(row=6, column=1, sticky='ew')

        # Item Options
        self.item_options_frame = tk.LabelFrame(self, text='Item')

        self.minimum_item_value_label = tk.Label(self.item_options_frame, text='Min Item Value: ')
        self.minimum_item_value_label.grid(row=0, column=0, sticky='w')

        self.minimum_item_value_entry = ttk.Entry(self.item_options_frame, width=5)
        self.minimum_item_value_entry.insert(0, self.tab.process_manager.config[self.tab.name]['minimum_item_value'])
        self.minimum_item_value_entry.grid(row=0, column=1, sticky='w')

        self.minimum_item_value_currency_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=7, values=('Keys', 'Refined', 'USD'))
        self.minimum_item_value_currency_combobox.set(self.tab.process_manager.config[self.tab.name]['minimum_item_value_currency'])
        self.minimum_item_value_currency_combobox.grid(row=0, column=2, sticky='ew')

        self.quality_label = tk.Label(self.item_options_frame, text='Quality: ')
        self.quality_label.grid(row=1, column=0, sticky='w')

        self.quality_entry = ttk.Entry(self.item_options_frame, width=16)
        self.quality_entry.insert(0, self.tab.process_manager.config[self.tab.name]['quality'])
        self.quality_entry.grid(row=1, column=1, sticky='w', columnspan=2)

        self.price_index_label = tk.Label(self.item_options_frame, text='Price Index: ')
        self.price_index_label.grid(row=2, column=0, sticky='w')

        self.price_index_entry = ttk.Entry(self.item_options_frame, width=16)
        self.price_index_entry.insert(0, self.tab.process_manager.config[self.tab.name]['price_index'])
        self.price_index_entry.grid(row=2, column=1, sticky='w', columnspan=2)

        self.level_label = tk.Label(self.item_options_frame, text='Level: ')
        self.level_label.grid(row=3, column=0, sticky='w')

        self.level_entry = ttk.Entry(self.item_options_frame, width=16)
        self.level_entry.insert(0, self.tab.process_manager.config[self.tab.name]['level'])
        self.level_entry.grid(row=3, column=1, sticky='w', columnspan=2)

        self.craftable_label = tk.Label(self.item_options_frame, text='Craftable: ')
        self.craftable_label.grid(row=4, column=0, sticky='w')

        self.craftable_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=5, values=('Both', 'True', 'False'))
        self.craftable_combobox.set(self.tab.process_manager.config[self.tab.name]['craftable'])
        self.craftable_combobox.grid(row=4, column=1, sticky='ew', columnspan=2)

        self.tradable_label = tk.Label(self.item_options_frame, text='Tradable: ')
        self.tradable_label.grid(row=5, column=0, sticky='w')

        self.tradable_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=5, values=('Both', 'True', 'False'))
        self.tradable_combobox.set(self.tab.process_manager.config[self.tab.name]['tradable'])
        self.tradable_combobox.grid(row=5, column=1, sticky='ew', columnspan=2)

        self.traded_label = tk.Label(self.item_options_frame, text='Traded: ')
        self.traded_label.grid(row=6, column=0, sticky='w')

        self.traded_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=5, values=('Both', 'True', 'False'))
        self.traded_combobox.set(self.tab.process_manager.config[self.tab.name]['traded'])
        self.traded_combobox.grid(row=6, column=1, sticky='ew', columnspan=2)

        self.slot_label = tk.Label(self.item_options_frame, text='Item Slot: ')
        self.slot_label.grid(row=7, column=0, sticky='w')

        self.slot_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=9, values=('Any', 'Primary', 'Secondary', 'Melee', 'Misc', 'PDA', 'PDA2', 'Action'))
        self.slot_combobox.set(self.tab.process_manager.config[self.tab.name]['slot'])
        self.slot_combobox.grid(row=7, column=1, sticky='ew', columnspan=2)

        self.wear_label = tk.Label(self.item_options_frame, text='Wear: ')
        self.wear_label.grid(row=8, column=0, sticky='w')

        wears = list(WEARS.values())
        wears.insert(0, 'Any')
        self.wear_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=14, values=wears)
        self.wear_combobox.set(self.tab.process_manager.config[self.tab.name]['wear'])
        self.wear_combobox.grid(row=8, column=1, sticky='ew', columnspan=2)

        self.australium_label = tk.Label(self.item_options_frame, text='Australium: ')
        self.australium_label.grid(row=9, column=0, sticky='w')

        self.australium_combobox = ttk.Combobox(self.item_options_frame, state='readonly', width=5, values=('Both', 'True', 'False'))
        self.australium_combobox.set(self.tab.process_manager.config[self.tab.name]['australium'])
        self.australium_combobox.grid(row=9, column=1, sticky='ew', columnspan=2)

        # Output Options
        self.output_options_frame = tk.LabelFrame(self, text='Output')

        self.currency_label = tk.Label(self.output_options_frame, text='Currency: ')
        self.currency_label.grid(row=0, column=0, sticky='w')

        self.currency_combobox = ttk.Combobox(self.output_options_frame, state='readonly', width=7, values=('Default', 'Keys', 'Refined', 'USD'))
        self.currency_combobox.set(self.tab.process_manager.config[self.tab.name]['currency'])
        self.currency_combobox.grid(row=0, column=1, sticky='ew', columnspan=2)

        self.minimum_displayed_item_value_label = tk.Label(self.output_options_frame, text='Min Displayed Item Value: ')
        self.minimum_displayed_item_value_label.grid(row=1, column=0, sticky='w')

        self.minimum_displayed_item_value_entry = ttk.Entry(self.output_options_frame, width=5)
        self.minimum_displayed_item_value_entry.insert(0, self.tab.process_manager.config[self.tab.name]['minimum_displayed_item_value'])
        self.minimum_displayed_item_value_entry.grid(row=1, column=1, sticky='w')

        self.minimum_displayed_item_value_currency_combobox = ttk.Combobox(self.output_options_frame, state='readonly', width=7, values=('Keys', 'Refined', 'USD'))
        self.minimum_displayed_item_value_currency_combobox.set(self.tab.process_manager.config[self.tab.name]['minimum_displayed_item_value_currency'])
        self.minimum_displayed_item_value_currency_combobox.grid(row=1, column=2, sticky='ew')

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

        self.display_avatars_combobox = ttk.Combobox(self.technical_options_frame, state='readonly', width=5, values=('True', 'False'))
        self.display_avatars_combobox.set(self.tab.process_manager.config['technical']['display_avatars'])
        self.display_avatars_combobox.grid(row=0, column=1, sticky='ew')

        self.limit_requests_label = tk.Label(self.technical_options_frame, text='Limit Requests: ')
        self.limit_requests_label.grid(row=1, column=0, sticky='w')

        self.limit_requests_combobox = ttk.Combobox(self.technical_options_frame, state='readonly', width=5, values=('True', 'False'))
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
            return False
        return True

    def check_entry_float(self, entry, default):
        try:
            float(entry.get())
            return True
        except ValueError:
            entry.delete(0, 'end')
            entry.insert(0, default)
            return False

    def apply(self):
        # Player
        self.tab.display_players = self.get_true_false_both_combobox(self.display_players_combobox)

        self.tab.set_collect_hours(self.get_true_false_both_combobox(self.collect_hours_combobox))

        self.tab.set_f2p(self.get_true_false_both_combobox(self.f2p_combobox))

        self.tab.set_status(self.status_combobox.get())

        max_hours = self.max_hours_entry.get()
        if max_hours:
            if self.check_entry_integer(self.max_hours_entry, self.tab.max_hours):
                self.tab.set_max_hours(int(max_hours))
        else:
            self.tab.set_max_hours(None)

        if self.last_online_entry.get():
            try:
                raw_minimum_last_online = time.mktime(time.strptime(self.last_online_entry.get(), '%m-%d-%y'))
                self.tab.set_raw_minimum_last_online(raw_minimum_last_online)
            except ValueError:
                self.last_online_entry.delete(0, 'end')
                self.last_online_entry.insert(0, self.tab.last_online)
        else:
            self.tab.set_raw_minimum_last_online(0)
        self.tab.last_online = self.last_online_entry.get()

        # Item
        minimum_item_value = self.minimum_item_value_entry.get()
        if minimum_item_value:
            self.check_entry_float(self.minimum_item_value_entry, self.tab.minimum_item_value)
        self.tab.minimum_item_value = minimum_item_value

        self.tab.minimum_item_value_currency = self.minimum_item_value_currency_combobox.get()

        if self.tab.minimum_item_value:
            if self.tab.minimum_item_value_currency == 'Refined':
                self.tab.set_raw_minimum_item_value(float(self.tab.minimum_item_value))
            elif self.tab.minimum_item_value_currency == 'Keys':
                self.tab.set_raw_minimum_item_value(
                    float(self.tab.minimum_item_value) * self.tab.process_manager.key_price)
            elif self.tab.minimum_item_value_currency == 'USD':
                self.tab.set_raw_minimum_item_value(
                    float(self.tab.minimum_item_value) / self.tab.process_manager.refined_price)
        else:
            self.tab.set_raw_minimum_item_value(0)

        quality = self.quality_entry.get()
        if quality:
            if self.check_entry_integer(self.quality_entry, self.tab.quality):
                self.tab.set_quality(int(quality))
        else:
            self.tab.set_quality(None)

        price_index = self.price_index_entry.get()
        if price_index:
            if self.check_entry_integer(self.price_index_entry, self.tab.price_index):
                self.tab.set_price_index(price_index)
        else:
            self.tab.set_price_index(None)

        level = self.level_entry.get()
        if level:
            if self.check_entry_integer(self.level_entry, self.tab.level):
                self.tab.set_level(int(level))
        else:
            self.tab.set_level(None)

        self.tab.set_craftable(self.get_true_false_both_combobox(self.craftable_combobox))
        self.tab.set_tradable(self.get_true_false_both_combobox(self.tradable_combobox))
        self.tab.set_traded(self.get_true_false_both_combobox(self.traded_combobox))
        self.tab.slot = self.slot_combobox.get()
        self.tab.wear = self.wear_combobox.get()
        self.tab.set_australium(self.get_true_false_both_combobox(self.australium_combobox))

        # Output
        self.tab.currency = self.currency_combobox.get()

        if self.minimum_displayed_item_value_entry.get():
            self.check_entry_float(self.minimum_displayed_item_value_entry, self.tab.minimum_displayed_item_value)
        self.tab.minimum_displayed_item_value = self.minimum_displayed_item_value_entry.get()

        self.tab.minimum_displayed_item_value_currency = self.minimum_displayed_item_value_currency_combobox.get()

        if self.tab.minimum_displayed_item_value:
            if self.tab.minimum_displayed_item_value_currency == 'Refined':
                self.tab.raw_minimum_displayed_item_value = float(self.tab.minimum_displayed_item_value)
            elif self.tab.minimum_displayed_item_value_currency == 'Keys':
                self.tab.raw_minimum_displayed_item_value = float(self.tab.minimum_displayed_item_value) * self.tab.process_manager.key_price
            elif self.tab.minimum_displayed_item_value_currency == 'USD':
                self.tab.raw_minimum_displayed_item_value = float(self.tab.minimum_displayed_item_value) / self.tab.process_manager.refined_price
        else:
            self.tab.raw_minimum_displayed_item_value = 0

        # Global Output
        if self.check_entry_integer(self.displayed_items_entry, self.tab.process_manager.config['output']['displayed_items']):
            self.tab.process_manager.config['output']['displayed_items'] = self.displayed_items_entry.get()

        if self.check_entry_integer(self.items_per_line_entry, self.tab.process_manager.config['output']['items_per_line']):
            if self.items_per_line_entry.get() != self.tab.process_manager.config['output']['items_per_line']:
                self.tab.process_manager.config['output']['items_per_line'] = self.items_per_line_entry.get()
                self.tab.process_manager.gui.clear_tab_outputs()
                self.tab.process_manager.gui.update_tab_sizes()

        if self.check_entry_integer(self.image_size_entry, self.tab.process_manager.config['output']['image_size']):
            if self.image_size_entry.get() != self.tab.process_manager.config['output']['image_size']:
                self.tab.process_manager.config['output']['image_size'] = self.image_size_entry.get()
                self.tab.process_manager.gui.clear_tab_outputs()
                self.tab.process_manager.gui.update_images()
                self.tab.process_manager.gui.update_tab_sizes()

        if self.check_entry_integer(self.font_size_entry, self.tab.process_manager.config['output']['font_size']):
            if self.font_size_entry.get() != self.tab.process_manager.config['output']['font_size']:
                self.tab.process_manager.config['output']['font_size'] = self.font_size_entry.get()
                self.tab.process_manager.gui.clear_tab_outputs()
                self.tab.process_manager.gui.update_tab_sizes()

        # Technical
        self.tab.process_manager.config['technical']['display_avatars'] = self.display_avatars_combobox.get()

        self.tab.process_manager.config['technical']['limit_requests'] = self.limit_requests_combobox.get()

        self.check_entry_integer(self.request_period_entry, self.tab.process_manager.config['technical']['request_period'])
        self.tab.process_manager.config['technical']['request_period'] = self.request_period_entry.get()

        self.check_entry_integer(self.requests_per_period_entry, self.tab.process_manager.config['technical']['requests_per_period'])
        self.tab.process_manager.config['technical']['requests_per_period'] = self.requests_per_period_entry.get()

        self.check_entry_integer(self.simultaneous_scans_entry, self.tab.process_manager.config['technical']['simultaneous_scans'])
        self.tab.process_manager.config['technical']['simultaneous_scans'] = self.simultaneous_scans_entry.get()

    def get_true_false_both_combobox(self, combobox):
        value = combobox.get()
        if value == 'Both':
            return value
        return value == 'True'

    def set_as_default(self):
        self.apply()

        # Player
        self.tab.process_manager.config[self.tab.name]['display_players'] = str(self.tab.display_players)
        self.tab.process_manager.config[self.tab.name]['collect_hours'] = str(self.tab.collect_hours)
        self.tab.process_manager.config[self.tab.name]['f2p'] = str(self.tab.f2p)
        self.tab.process_manager.config[self.tab.name]['status'] = self.tab.status
        self.tab.process_manager.config[self.tab.name]['max_hours'] = str(self.tab.max_hours) if self.tab.max_hours else ''
        self.tab.process_manager.config[self.tab.name]['last_online'] = self.tab.last_online

        # Item
        self.tab.process_manager.config[self.tab.name]['minimum_item_value'] = self.tab.minimum_item_value
        self.tab.process_manager.config[self.tab.name]['minimum_item_value_currency'] = self.tab.minimum_item_value_currency
        self.tab.process_manager.config[self.tab.name]['quality'] = str(self.tab.quality) if self.tab.quality else ''
        self.tab.process_manager.config[self.tab.name]['price_index'] = str(self.tab.price_index) if self.tab.price_index else ''
        self.tab.process_manager.config[self.tab.name]['level'] = str(self.tab.level) if self.tab.level else ''
        self.tab.process_manager.config[self.tab.name]['craftable'] = str(self.tab.craftable)
        self.tab.process_manager.config[self.tab.name]['tradable'] = str(self.tab.tradable)
        self.tab.process_manager.config[self.tab.name]['traded'] = str(self.tab.traded)
        self.tab.process_manager.config[self.tab.name]['slot'] = self.tab.slot
        self.tab.process_manager.config[self.tab.name]['wear'] = self.tab.wear
        self.tab.process_manager.config[self.tab.name]['australium'] = str(self.tab.australium)

        # Output
        self.tab.process_manager.config[self.tab.name]['currency'] = self.tab.currency
        self.tab.process_manager.config[self.tab.name]['minimum_displayed_item_value'] = self.tab.minimum_displayed_item_value
        self.tab.process_manager.config[self.tab.name]['minimum_displayed_item_value_currency'] = self.tab.minimum_displayed_item_value_currency

        self.tab.process_manager.config.write(open('config.ini', 'w'))

    def display_category(self, event):
        selection = self.category_listbox.get(int(self.category_listbox.curselection()[0]))
        if selection == 'Player':
            self.player_options_frame.grid(row=0, column=1, sticky='nsew')
            self.item_options_frame.grid_remove()
            self.output_options_frame.grid_remove()
            self.technical_options_frame.grid_remove()
        if selection == 'Item':
            self.player_options_frame.grid_remove()
            self.item_options_frame.grid(row=0, column=1, sticky='nsew')
            self.output_options_frame.grid_remove()
            self.technical_options_frame.grid_remove()
        if selection == 'Output':
            self.player_options_frame.grid_remove()
            self.item_options_frame.grid_remove()
            self.output_options_frame.grid(row=0, column=1, sticky='nsew')
            self.technical_options_frame.grid_remove()
        if selection == 'Technical':
            self.player_options_frame.grid_remove()
            self.item_options_frame.grid_remove()
            self.output_options_frame.grid_remove()
            self.technical_options_frame.grid(row=0, column=1, sticky='nsew')
