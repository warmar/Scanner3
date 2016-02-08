#!/usr/bin/env python3

from item import Item
import math

GET_OWNED_GAMES_URL = 'http://api.steampowered.com/iplayerservice/getownedgames/v1/?key={0}&include_played_free_games=1&steamid=%s'
GET_ITEMS_URL = 'http://api.steampowered.com/ieconitems_440/getplayeritems/v0001/?key={0}&steamid=%s'


class Player:
    def __init__(self, process_manager, id64, data=None):
        if not data:
            data = {}
        self.process_manager = process_manager
        self.id64 = id64
        self.name = data.get('name')
        self.hours = data.get('hours', None)
        self.f2p = data.get('f2p')
        self.avatar = data.get('avatar', None)
        self.status = data.get('status', -2)
        self.last_online = data.get('last_online', None)
        self.simplified_items = data.get('simplified_items', None)
        self.items = data.get('items', None)

    def get_simplified_items(self):
        simplified_items = []
        for item in self.items:
            simplified_items.append({'_id': item.original_id, 'defindex': item.defindex})
        return simplified_items

    def check(self, f2p, status, max_hours):
        if f2p != 'Both':
            if str(self.f2p) != f2p:
                return False
        if not self.check_status(status):
            return False
        if max_hours is not None:
            if self.hours and self.hours > max_hours:
                return False
        return True

    def check_status(self, status):
        if status == 'Semi-Online':
            if self.status == 0:
                return False
        if status == 'Online':
            if self.status in (0, 2, 3, 4):
                return False
        if status == 'In-Game':
            if self.status not in (-1, -2):
                return False
        return True

    def check_last_online(self, min_last_online):
        if self.last_online < min_last_online:
            return False
        return True

    def check_items(self, requirements, minimum_item_value, minimum_player_value):
        if not minimum_item_value and not minimum_player_value and not requirements:
            return True

        has_requirements = False
        has_item_value = False
        has_player_value = False
        for item in self.items:
            has_requirements = has_requirements or item.check(requirements)
            if (item.get_raw_price() or 0) >= minimum_item_value:
                has_item_value = True
            if (item.get_raw_price() or 0) >= minimum_player_value:
                has_player_value = True

        return (has_requirements and has_player_value) if requirements else (has_item_value and has_player_value)

    def get_hours(self):
        url = GET_OWNED_GAMES_URL.format(self.process_manager.config['api']['steam_api_key']) % self.id64
        raw_games = self.process_manager.request_manager.make_api_request(url,
                                                                          mode='json',
                                                                          priority=False,
                                                                          tags=(self.id64,))
        if raw_games is None:
            return

        if 'games' not in raw_games['response']:
            return
        tf2 = [game for game in raw_games['response']['games'] if game['appid'] == 440]
        if not tf2:
            return
        self.hours = math.ceil(tf2[0]['playtime_forever']/60)

    def get_items(self):
        url = GET_ITEMS_URL.format(self.process_manager.config['api']['steam_api_key']) % self.id64
        raw_items = self.process_manager.request_manager.make_api_request(url, mode='json',
                                                                          priority=False, tags=(self.id64,))
        if raw_items is None:
            return

        if raw_items['result']['status'] != 1:
            return

        self.f2p = raw_items['result']['num_backpack_slots'] < 300
        self.items = []
        for item in raw_items['result']['items']:
            # Handle Cheater Notification 'items'
            if item['defindex'] in range(122, 125):
                continue

            item['craftable'] = 'flag_cannot_craft' not in item
            item['tradable'] = 'flag_cannot_trade' not in item

            self.items.append(Item(self.process_manager, item))
