#!/usr/bin/env python3

from Core import baseprocessmanager


class ScanMonitor:
    def __init__(self, process_manager: baseprocessmanager.BaseProcessManager):
        self.process_manager = process_manager

        self.message = None
        self.progress = 0
        self.maximum_progress = 0

        # Player
        self.collect_hours = None
        self.f2p = None
        self.status = None
        self.max_hours = None
        self.max_refined = None
        self.raw_minimum_last_online = None
        self.rescan = None

        # Item
        self.raw_minimum_item_value = None
        self.quality = None
        self.price_index = None
        self.level = None
        self.craftable = None
        self.tradable = None
        self.traded = None
        self.wear = None
        self.australium = None

        self.item_requirements = {}

        self.scan = None

    def update_requirements(self):
        self.item_requirements = {}
        if self.raw_minimum_item_value:
            self.item_requirements.update({'value': self.raw_minimum_item_value})
        if self.quality is not None:
            self.item_requirements.update({'quality': self.quality})
        if self.price_index is not None:
            self.item_requirements.update({'index': self.price_index})
        if self.level is not None:
            self.item_requirements.update({'level': self.level})
        if self.craftable != 'Both':
            self.item_requirements.update({'craftable': self.craftable})
        if self.tradable != 'Both':
            self.item_requirements.update({'tradable': self.tradable})
        if self.traded != 'Both':
            self.item_requirements.update({'traded': self.traded})
        if self.australium != 'Both':
            self.item_requirements.update({'australium': self.australium})

    # Player
    def set_collect_hours(self, collect_hours):
        self.collect_hours = collect_hours

    def set_f2p(self, f2p):
        self.f2p = f2p

    def set_status(self, status):
        self.status = status

    def set_max_hours(self, max_hours):
        self.max_hours = max_hours

    def set_max_refined(self, max_refined):
        self.max_refined = max_refined

    def set_raw_minimum_last_online(self, raw_minimum_last_online):
        self.raw_minimum_last_online = raw_minimum_last_online

    def set_rescan(self, rescan):
        self.rescan = rescan

    # Item
    def set_raw_minimum_item_value(self, raw_minimum_item_value):
        self.raw_minimum_item_value = raw_minimum_item_value

    def set_quality(self, quality):
        self.quality = quality

    def set_price_index(self, price_index):
        self.price_index = price_index

    def set_level(self, level):
        self.level = level

    def set_craftable(self, craftable):
        self.craftable = craftable

    def set_tradable(self, tradable):
        self.tradable = tradable

    def set_traded(self, traded):
        self.traded = traded

    def set_australium(self, australium):
        self.australium = australium

    def report_status(self, message, value, maximum):
        self.message = message
        self.progress = value
        self.maximum_progress = maximum
        self.process_manager.update_progress()

    def report_steam_id64s(self, steam_id64s):
        pass

    def report_finished_player(self, player):
        pass

    def report_finished_scan(self, scan):
        self.process_manager.report_finished_scan_monitor(self)
        self.scan = None
