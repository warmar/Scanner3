#!/usr/bin/env python3

import math
import time

from Core import baseprocessmanager
from Core.globals import GET_ITEMS_URL, GET_OWNED_GAMES_URL
from Core.item import Item


class Player:
    def __init__(self, process_manager: baseprocessmanager.BaseProcessManager, id64, data=None):
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

    def check(self, f2p, status, max_hours):
        if f2p != 'Both':
            if self.f2p is not f2p:
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

    def check_items(self, requirements):
        if not requirements:
            return True

        has_requirements = False
        for item in self.items:
            if not has_requirements:
                has_requirements = item.check(requirements)

        return has_requirements

    def get_number_refined(self):
        ref = 0
        rec = 0
        scrap = 0
        for item in self.items:
            if item.defindex == 5002:
                ref += 1
                continue
            if item.defindex == 5001:
                rec += 1
                continue
            if item.defindex == 5000:
                scrap += 1

        print(ref, rec, scrap)

        divrec, scrap = divmod(scrap, 3)
        rec += divrec
        divref, rec = divmod(rec, 3)
        ref += divref
        total = ref + 0.33*rec + 0.11*scrap
        return total

    def get_number_keys(self):
        total = 0
        for item in self.items:
            if item.get_name() == 'Mann Co. Supply Crate Key':
                total += 1
        return total

    def get_hours(self):
        url = GET_OWNED_GAMES_URL.format(self.process_manager.config['api']['steam_api_key']) % self.id64
        raw_games = self.process_manager.request_manager.make_api_request(url, mode='json', priority=False, tags=(self.id64,))

        if raw_games is None:
            return

        if 'games' not in raw_games['response']:
            return

        tf2 = [game for game in raw_games['response']['games'] if game['appid'] == 440]
        if not tf2:
            return

        self.hours = math.ceil(tf2[0]['playtime_forever'] / 60)

    def get_items(self):
        url = GET_ITEMS_URL.format(self.process_manager.config['api']['steam_api_key']) % self.id64
        raw_items = self.process_manager.request_manager.make_api_request(url, mode='json', priority=False, tags=(self.id64,))

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
