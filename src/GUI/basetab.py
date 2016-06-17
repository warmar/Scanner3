#!/usr/bin/env python3

from PIL import Image, ImageTk
import tkinter.ttk as ttk
import tkinter as tk
import webbrowser
import threading
import requests
import time
import io

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


class BaseTab(tk.Frame):
    def __init__(self, process_manager):
        super().__init__()
        self.process_manager = process_manager

        self.grid_rowconfigure(2, weight=1)

        self.players = {}

        self.output_canvas = None

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

        self.output_canvas = tk.Canvas(self, scrollregion=(0, 0, 0, 0), relief='ridge', bg='#999999', bd=2,
                                       highlightthickness=0)
        self.output_canvas.bind('<MouseWheel>', lambda event: self.output_canvas.yview_scroll(
            int(-event.delta / 120), 'units'))
        self.output_canvas.bind('<Button-2>', lambda event: self.clear_output())
        self.output_scrollbar = ttk.Scrollbar(self, command=self.output_canvas.yview)
        self.output_canvas.config(yscrollcommand=self.output_scrollbar.set)
        self.output_canvas.grid(row=0, column=3, rowspan=6, sticky='nsew')
        self.output_scrollbar.grid(row=0, column=4, rowspan=6, sticky='ns')

    def create_options(self, name):
        # Player
        self.display_players = self.process_manager.config[name]['display_players']
        self.collect_hours = self.process_manager.config[name]['collect_hours']
        self.f2p = self.process_manager.config[name]['f2p']
        self.status = self.process_manager.config[name]['status']
        self.max_hours = self.process_manager.config[name]['max_hours']
        self.minimum_player_value = self.process_manager.config[name]['minimum_player_value']
        self.minimum_player_value_currency = self.process_manager.config[name]['minimum_player_value_currency']
        self.raw_minimum_player_value = self.process_manager.config[name]['raw_minimum_player_value']
        self.last_online = self.process_manager.config[name]['last_online']
        self.raw_last_online = self.process_manager.config[name]['raw_last_online']

        # Output
        self.currency = self.process_manager.config[name]['currency']
        self.minimum_item_value = self.process_manager.config[name]['minimum_item_value']
        self.minimum_item_value_currency = self.process_manager.config[name]['minimum_item_value_currency']
        self.raw_minimum_item_value = self.process_manager.config[name]['raw_minimum_item_value']

    def open_options(self):
        return None

    def start_scan(self):
        return None

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
            avatarimage = requests.get('http://' + player.avatar[8:])
            if avatarimage.status_code == 200:
                player.avatarimage = ImageTk.PhotoImage(Image.open(io.BytesIO(avatarimage.content)).resize(
                    (self.image_size(), self.image_size()), Image.ANTIALIAS))
            else:
                player.avatarimage = self.process_manager.gui.default_avatar

        # Player Name
        player_name = player.name.encode('ascii', 'ignore').decode()
        if player.last_online is not None:
            player_name += ' (%s)' % time.ctime(player.last_online)
        self.output_canvas.create_text(0, (-height), tags='player%s' % player.id64, text=player_name, anchor='nw',
                                       font=('Helvetica', self.font_size()))

        # Hours
        hours = self.output_canvas.create_text(self.image_size() / 10 + 1, (-height) + self.text_height(),
                                               tags='player%s' % player.id64,
                                               text='\n'.join(str(player.hours) if player.hours is not None else ' '),
                                               font=('Helvetica', self.font_size()), anchor='nw')
        self.output_canvas.tag_bind(hours, '<Button-1>', self.event_remove_player)
        # Status Box
        status_box = self.output_canvas.create_rectangle(self.image_size() / 10, (-height) + self.text_height(),
                                                         self.image_size() / 10 + self.text_width(),
                                                         (-height) + self.text_height() + self.image_size(),
                                                         tags='player%s' % player.id64,
                                                         fill=STATUSES[player.status]['color'])
        self.output_canvas.tag_lower(status_box)
        self.output_canvas.tag_bind(status_box, '<Button-1>', self.event_remove_player)

        # Player Avatar
        avatar = self.output_canvas.create_image((self.image_size() / 5) + self.text_width(),
                                                 (-height) + self.text_height(), tags='player%s' % player.id64,
                                                 image=player.avatarimage, anchor='nw')
        profile_link = 'http://steamcommunity.com/profiles/%s' % player.id64
        friends_link = 'steam://friends/add/%s' % player.id64
        self.output_canvas.tag_bind(avatar, '<Button-1>', lambda event: webbrowser.open(profile_link))
        self.output_canvas.tag_bind(avatar, '<Button-3>', lambda event: webbrowser.open(friends_link))

        sorted_items = sorted(player.items, key=lambda x: x.get_raw_price() or 0, reverse=True)

        for item, index in zip(sorted_items[:self.displayed_items()],
                               range(min(len(sorted_items), self.displayed_items()))):
            if item.get_raw_price():
                if item.get_raw_price() < float(self.raw_minimum_item_value):
                    break

            y_index, x_index = divmod(index, int(self.process_manager.config['output']['items_per_line']))
            item_x = self.text_width() + (self.image_size() * (x_index + 1.3))
            item_y = (-height) + self.text_height() + (y_index * self.image_size())

            description_text = ''
            description_text += '%s %s' % (QUALITIES[item.quality]['name'], item.get_name())
            description_text += '\n%s' % item.get_price(self.currency)
            if item.quality == 5:
                effect = item.get_price_index()
                if not effect == '0':
                    description_text += '\n%s' % self.process_manager.particle_effect_schema[int(effect)]['name']
            item_description = self.output_canvas.create_text(
                item_x + (self.image_size() / 2),
                item_y + (self.image_size() / 2),
                tags=('player%s' % player.id64,
                      'item_description-%s-%s' % (player.id64, index),
                      'item-%s-%s' % (player.id64, index)),
                text=description_text,
                font=('Helvetica', int(self.font_size() * 1.5)),
                justify='center',
                anchor='center')
            self.output_canvas.tag_bind(item_description, '<Button-1>', self.hide_description)

            description_bbox = self.output_canvas.bbox(item_description)
            if description_bbox[0] < 1:
                self.output_canvas.move(item_description, -description_bbox[0], 0)
            width = self.text_width() + self.image_size() * (
                self.displayed_items() + 1 + 0.4)
            if description_bbox[2] > width:
                self.output_canvas.move(item_description, (width - description_bbox[2]), 0)
            item_description_box = self.output_canvas.create_rectangle(
                self.output_canvas.bbox(item_description),
                tags=('player%s' % player.id64,
                      'item_description_box-%s-%s' % (player.id64, index),
                      'item-%s-%s' % (player.id64, index)),
                fill='#FFFFFF')
            self.output_canvas.tag_bind(item_description_box, '<Button-1>', self.hide_description)

            self.output_canvas.itemconfig(item_description, state='hidden')
            self.output_canvas.itemconfig(item_description_box, state='hidden')

            # Item Box
            self.output_canvas.create_rectangle(item_x, item_y, item_x + self.image_size(), item_y + self.image_size(),
                                                tags='player%s' % player.id64, fill=QUALITIES[item.quality]['color'])

            # Unusual Effect
            if item.quality == 5:
                effect = item.get_price_index()
                if effect != '0':
                    if effect in self.process_manager.gui.particle_effects:
                        self.output_canvas.create_image(item_x, item_y, tags='player%s' % player.id64,
                                                        image=self.process_manager.gui.particle_effects[effect],
                                                        anchor='nw')

            # Item Image
            file_name = item.get_name()
            file_name = file_name.replace('?', '')
            file_name = file_name.replace(':', '')
            item_image = self.output_canvas.create_image(item_x, item_y,
                                                         tags=('player%s' % player.id64,
                                                               'item-%s-%s' % (player.id64, index)),
                                                         image=self.process_manager.gui.images[file_name],
                                                         anchor='nw')
            self.output_canvas.tag_bind(item_image, '<Button-1>', self.display_description)

            # Item Price
            item_price = self.output_canvas.create_text(item_x + 1, item_y + self.image_size() - 1,
                                                        tags=('player%s' % player.id64,
                                                              'item-%s-%s' % (player.id64, index)),
                                                        text=item.get_price(self.currency),
                                                        font=('Helvetica', self.font_size()),
                                                        anchor='sw')
            self.output_canvas.tag_bind(item_price, '<Button-1>', self.display_description)

            # Traded Marker
            if item.is_traded():
                traded_marker = self.output_canvas.create_line(item_x + self.image_size() / 2,
                                                               item_y + self.image_size() - 1,
                                                               item_x + self.image_size() - 1,
                                                               item_y + self.image_size() / 2,
                                                               tags=('player%s' % player.id64,
                                                                     'item-%s-%s' % (player.id64, index)),
                                                               width=2,
                                                               fill='#00FFFF')
                self.output_canvas.tag_bind(traded_marker, '<Button-1>', self.display_description)

            # Non-Craftable Marker
            if not item.craftable:
                craftable_marker = self.output_canvas.create_line(item_x + self.image_size() * (3 / 4),
                                                                  item_y + self.image_size() - 1,
                                                                  item_x + self.image_size() - 1,
                                                                  item_y + self.image_size() * (3 / 4),
                                                                  tags=('player%s' % player.id64,
                                                                        'item-%s-%s' % (player.id64, index)),
                                                                  width=2,
                                                                  fill='#FFFFFF')
                self.output_canvas.tag_bind(craftable_marker, '<Button-1>', self.display_description)

            # Non-Tradable marker
            if not item.tradable:
                tradable_marker = self.output_canvas.create_line(item_x + 1,
                                                                 item_y + self.image_size() / 4,
                                                                 item_x + self.image_size() / 4,
                                                                 item_y + 1,
                                                                 tags=('player%s' % player.id64,
                                                                       'item-%s-%s' % (player.id64, index)),
                                                                 width=2,
                                                                 fill='#FF0000')
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

    def finish_scan(self, scan):
        self.scan = None

    def close(self):
        def func():
            if self.scan is not None:
                self.scan.end()
                while self.scan is not None:
                    time.sleep(0.01)
            self.process_manager.gui.scan_notebook.forget(self)
            self.process_manager.gui.tabs.remove(self)

        threading.Thread(target=func).start()
