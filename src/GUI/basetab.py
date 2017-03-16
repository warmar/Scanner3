#!/usr/bin/env python3

import io
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

import requests
from PIL import Image, ImageTk

from Core import scanmonitor
from Core.globals import QUALITIES, STATUSES


class BaseTab(tk.Frame, scanmonitor.ScanMonitor):
    name = None

    def __init__(self, process_manager):
        tk.Frame.__init__(self)
        scanmonitor.ScanMonitor.__init__(self, process_manager)

        # Player
        self.display_players = None
        self.last_online = None
        # Output
        self.currency = None
        self.minimum_displayed_item_value = None
        self.minimum_displayed_item_value_currency = None
        self.raw_minimum_displayed_item_value = None
        # Item
        self.minimum_item_value = None
        self.minimum_item_value_currency = None
        self.slot = None

        self.grid_rowconfigure(2, weight=1)
        self.create_widgets()

        self.create_options()

        self.players = {}

        self.display_threads = []

    def create_widgets(self):
        # Input
        self.options_button = ttk.Button(self, text='Options', command=self.open_options)
        self.options_button.grid(row=0, column=0, sticky='w')

        self.close_button = ttk.Button(self, text='Close', command=self.close)
        self.close_button.grid(row=0, column=0, sticky='e')

        self.input_text = tk.Text(self, width=51, height=20)
        self.input_text.grid(row=2, column=0, sticky='ns')

        self.input_scrollbar = ttk.Scrollbar(self, command=self.input_text.yview)
        self.input_text.config(yscrollcommand=self.input_scrollbar.set)
        self.input_scrollbar.grid(row=2, column=1, sticky='ns')

        self.scan_button = ttk.Button(self, image=self.process_manager.gui.shark, command=self.start_scan)
        self.scan_button.grid(row=3, column=0, columnspan=2, sticky='ew')

        self.progressbar = ttk.Progressbar(self)
        self.progressbar.grid(row=4, column=0, columnspan=2, sticky='ew')

        self.progress_label = tk.Label(self)
        self.progress_label.grid(row=5, column=0, columnspan=2, sticky='w')

        # Output
        self.output_button = ttk.Button(self, text='«', command=self.process_manager.gui.hide_output, width=1)
        self.output_button.grid(row=0, column=2, rowspan=6, sticky='ns')

        self.output_canvas = tk.Canvas(self, scrollregion=(0, 0, 0, 0), relief='ridge', bg='#999999', bd=2, highlightthickness=0)
        self.output_canvas.bind('<MouseWheel>', lambda event: self.output_canvas.yview_scroll(int(-event.delta / 120), 'units'))
        self.output_canvas.bind('<Button-2>', lambda event: self.clear_output())
        self.output_scrollbar = ttk.Scrollbar(self, command=self.output_canvas.yview)
        self.output_canvas.config(yscrollcommand=self.output_scrollbar.set)
        self.output_canvas.grid(row=0, column=3, rowspan=6, sticky='nsew')
        self.output_scrollbar.grid(row=0, column=4, rowspan=6, sticky='ns')

    def create_options(self):
        self.options = None

    def open_options(self):
        self.options.category_listbox.selection_clear(0, 'end')
        self.options.category_listbox.selection_set(0, 0)
        self.options.display_category(None)
        self.options.wm_deiconify()

    def start_scan(self):
        pass

    def image_size(self):
        return int(self.process_manager.config['output']['image_size'])

    def font_size(self):
        return int(self.process_manager.config['output']['font_size'])

    def displayed_items(self):
        return int(self.process_manager.config['output']['displayed_items'])

    def text_height(self):
        return self.process_manager.gui.text_height

    def text_width(self):
        return self.process_manager.gui.text_width

    def display_player(self, player):
        height = self.image_size() + self.text_height() + 1

        if self.process_manager.config['technical']['display_avatars'] != 'True' or not player.avatar:
            player.avatarimage = self.process_manager.gui.default_avatar
        else:
            avatarimage = requests.get(player.avatar)
            if avatarimage.status_code == 200:
                player.avatarimage = ImageTk.PhotoImage(Image.open(io.BytesIO(avatarimage.content)).resize((self.image_size(), self.image_size()), Image.ANTIALIAS))
            else:
                player.avatarimage = self.process_manager.gui.default_avatar

        # Player Name
        player_name = player.name.encode('ascii', 'ignore').decode()
        if player.last_online is not None:
            player_name += ' (%s)' % time.ctime(player.last_online)
        self.output_canvas.create_text(
            0,
            (-height),
            tags='player%s' % player.id64,
            text=player_name,
            anchor='nw',
            font=('Helvetica', self.font_size())
        )

        # Hours
        hours = self.output_canvas.create_text(
            self.image_size() / 10 + 1,
            (-height) + self.text_height(),
            tags='player%s' % player.id64,
            text='\n'.join(str(player.hours) if player.hours is not None else ' '),
            font=('Helvetica', self.font_size()), anchor='nw'
        )
        self.output_canvas.tag_bind(hours, '<Button-1>', self.event_remove_player)

        # Status Box
        status_box = self.output_canvas.create_rectangle(
            self.image_size() / 10,
            (-height) + self.text_height(),
            self.image_size() / 10 + self.text_width(),
            (-height) + self.text_height() + self.image_size(),
            tags='player%s' % player.id64,
            fill=STATUSES[player.status]['color']
        )
        self.output_canvas.tag_lower(status_box)
        self.output_canvas.tag_bind(status_box, '<Button-1>', self.event_remove_player)

        # Player Avatar
        avatar = self.output_canvas.create_image(
            (self.image_size() / 5) + self.text_width(),
            (-height) + self.text_height(),
            tags='player%s' % player.id64,
            image=player.avatarimage,
            anchor='nw'
        )
        profile_link = 'http://steamcommunity.com/profiles/%s' % player.id64
        friends_link = 'steam://friends/add/%s' % player.id64
        self.output_canvas.tag_bind(avatar, '<Button-1>', lambda event: webbrowser.open(profile_link))
        self.output_canvas.tag_bind(avatar, '<Button-3>', lambda event: webbrowser.open(friends_link))

        for item, index in zip(player.items[:self.displayed_items()], range(min(len(player.items), self.displayed_items()))):
            y_index, x_index = divmod(index, int(self.process_manager.config['output']['items_per_line']))
            item_x = self.text_width() + (self.image_size() * (x_index + 1.3))
            item_y = (-height) + self.text_height() + (y_index * self.image_size())

            description_text = '%s %s' % (QUALITIES[item.quality]['name'], item.get_name())
            description_text += '\n%s' % item.get_price(self.currency)
            if item.quality == 5:
                effect = item.get_price_index()
                if not effect == '0':
                    description_text += '\n%s' % self.process_manager.particle_effect_schema[int(effect)]['name']
            item_description = self.output_canvas.create_text(
                item_x + (self.image_size() / 2),
                item_y + (self.image_size() / 2),
                tags=(
                    'player%s' % player.id64,
                    'item_description-%s-%s' % (player.id64, index),
                    'item-%s-%s' % (player.id64, index)
                ),
                text=description_text,
                font=('Helvetica', int(self.font_size() * 1.5)),
                justify='center',
                anchor='center'
            )
            self.output_canvas.tag_bind(item_description, '<Button-1>', self.hide_description)

            description_bbox = self.output_canvas.bbox(item_description)
            if description_bbox[0] < 1:
                self.output_canvas.move(item_description, -description_bbox[0], 0)
            width = self.text_width() + self.image_size() * (self.displayed_items() + 1 + 0.4)
            if description_bbox[2] > width:
                self.output_canvas.move(item_description, (width - description_bbox[2]), 0)
            item_description_box = self.output_canvas.create_rectangle(
                self.output_canvas.bbox(item_description),
                tags=(
                    'player%s' % player.id64,
                    'item_description_box-%s-%s' % (player.id64, index),
                    'item-%s-%s' % (player.id64, index)
                ),
                fill='#FFFFFF')
            self.output_canvas.tag_bind(item_description_box, '<Button-1>', self.hide_description)

            self.output_canvas.itemconfig(item_description, state='hidden')
            self.output_canvas.itemconfig(item_description_box, state='hidden')

            # Item Box
            self.output_canvas.create_rectangle(
                item_x,
                item_y,
                item_x + self.image_size(),
                item_y + self.image_size(),
                tags='player%s' % player.id64,
                fill=QUALITIES[item.quality]['color']
            )

            # Unusual Effect
            if item.quality == 5:
                effect = item.get_price_index()
                if effect != '0':
                    if effect in self.process_manager.gui.particle_effects:
                        self.output_canvas.create_image(
                            item_x,
                            item_y,
                            tags='player%s' % player.id64,
                            image=self.process_manager.gui.particle_effects[effect],
                            anchor='nw'
                        )

            # Item Image
            file_name = item.get_name()
            file_name = file_name.replace('?', '')
            file_name = file_name.replace(':', '')
            file_name = file_name.replace('/', '')
            item_image = self.output_canvas.create_image(
                item_x,
                item_y,
                tags=(
                    'player%s' % player.id64,
                    'item-%s-%s' % (player.id64, index)
                ),
                image=self.process_manager.gui.images[file_name],
                anchor='nw'
            )
            self.output_canvas.tag_bind(item_image, '<Button-1>', self.display_description)

            # Item Price
            item_price = self.output_canvas.create_text(
                item_x + 1,
                item_y + self.image_size() - 1,
                tags=(
                    'player%s' % player.id64,
                    'item-%s-%s' % (player.id64, index)
                ),
                text=item.get_price(self.currency),
                font=('Helvetica', self.font_size()),
                anchor='sw'
            )
            self.output_canvas.tag_bind(item_price, '<Button-1>', self.display_description)

            # Traded Marker
            if item.is_traded():
                traded_marker = self.output_canvas.create_line(
                    item_x + self.image_size() / 2,
                    item_y + self.image_size() - 1,
                    item_x + self.image_size() - 1,
                    item_y + self.image_size() / 2,
                    tags=(
                        'player%s' % player.id64,
                        'item-%s-%s' % (player.id64, index)
                    ),
                    width=2,
                    fill='#00FFFF'
                )
                self.output_canvas.tag_bind(traded_marker, '<Button-1>', self.display_description)

            # Non-Craftable Marker
            if not item.craftable:
                craftable_marker = self.output_canvas.create_line(
                    item_x + self.image_size() * (3 / 4),
                    item_y + self.image_size() - 1,
                    item_x + self.image_size() - 1,
                    item_y + self.image_size() * (3 / 4),
                    tags=(
                        'player%s' % player.id64,
                        'item-%s-%s' % (player.id64, index)
                    ),
                    width=2,
                    fill='#FFFFFF'
                )
                self.output_canvas.tag_bind(craftable_marker, '<Button-1>', self.display_description)

            # Non-Tradable marker
            if not item.tradable:
                tradable_marker = self.output_canvas.create_line(
                    item_x + 1,
                    item_y + self.image_size() / 4,
                    item_x + self.image_size() / 4,
                    item_y + 1,
                    tags=(
                        'player%s' % player.id64,
                        'item-%s-%s' % (player.id64, index)
                    ),
                    width=2,
                    fill='#FF0000'
                )
                self.output_canvas.tag_bind(tradable_marker, '<Button-1>', self.display_description)

            self.output_canvas.tag_raise(item_price)

        player.index = len(self.players)
        player.done = False
        self.players[player.id64] = player
        self.output_canvas.move('player%s' % player.id64, 0, self.output_canvas.bbox('all')[3] + height)
        player.done = True

        self.update_output_scrollregion()

    def event_remove_player(self, event):
        id64 = int(self.output_canvas.gettags('current')[0].replace('player', ''))
        self.remove_player(id64)

    def remove_player(self, id64):
        player = self.players[id64]
        bbox = self.output_canvas.bbox('player%s' % player.id64)
        self.output_canvas.delete('player%s' % id64)
        for remove_id64 in self.players:
            remove_player = self.players[remove_id64]
            if remove_player.index > player.index:
                while not remove_player.done:
                    time.sleep(0.01)
                self.output_canvas.move('player%s' % remove_player.id64, 0, bbox[1] - bbox[3])
                remove_player.index -= 1
        del self.players[id64]
        self.update_output_scrollregion()

    def display_description(self, event):
        tags = self.output_canvas.gettags('current')
        _, id64, index = tags[1].split('-')
        self.output_canvas.tag_raise('item_description_box-%s-%s' % (id64, index))
        self.output_canvas.tag_raise('item_description-%s-%s' % (id64, index))
        self.output_canvas.itemconfig('item_description_box-%s-%s' % (id64, index), state='normal')
        self.output_canvas.itemconfig('item_description-%s-%s' % (id64, index), state='normal')

    def hide_description(self, event):
        tags = self.output_canvas.gettags('current')
        _, id64, index = tags[2].split('-')
        self.output_canvas.itemconfig('item_description_box-%s-%s' % (id64, index), state='hidden')
        self.output_canvas.itemconfig('item_description-%s-%s' % (id64, index), state='hidden')

    def clear_output(self, steam_id64s=None):
        if steam_id64s is None:
            self.output_canvas.delete('all')
            self.players = {}
        else:
            for id64 in steam_id64s:
                if id64 in self.players:
                    self.remove_player(id64)
        self.update_output_scrollregion()

    def update_output_scrollregion(self):
        bbox = self.output_canvas.bbox('all')
        if not bbox:
            bbox = (0, 0, 0, 0)
        bbox_xpos1 = 0
        bbox_ypos1 = 0
        bbox_xpos2 = bbox[2] + self.image_size() / 10
        bbox_ypos2 = bbox[3] + self.image_size() / 10
        self.output_canvas.config(scrollregion=(bbox_xpos1, bbox_ypos1, bbox_xpos2, bbox_ypos2))

    def close(self):
        def func():
            self.options.destroy()
            if self.scan is not None:
                self.scan.end()
                while self.scan is not None:
                    time.sleep(0.01)
            self.process_manager.gui.scan_notebook.forget(self)
            self.process_manager.gui.tabs.remove(self)

        threading.Thread(target=func).start()

    def report_status(self, message, value, maximum):
        super().report_status(message, value, maximum)
        self.progress_label.config(text=message)
        self.progressbar.config(value=value, maximum=maximum)

    def report_steam_id64s(self, steam_id64s):
        self.clear_output(steam_id64s)

    def report_finished_player(self, player):
        if self.display_players:
            player.items = [item for item in player.items if (item.get_raw_price() or 0) >= self.raw_minimum_displayed_item_value]
            if not player.items:
                return
            player.items = sorted(player.items, key=lambda x: x.get_raw_price() or 0, reverse=True)

            self.display_threads.append(threading.Thread(target=self.display_player, args=(player,)))
            self.display_threads[-1].start()

    def report_finished_scan(self, scan):
        super().report_finished_scan(scan)
        for display_thread in self.display_threads:
            display_thread.join()
        self.scan_button.config(image=self.process_manager.gui.shark, command=self.start_scan)
