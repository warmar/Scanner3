#!/usr/bin/env python3

import os
import sys
import threading
import time
from tkinter import messagebox

import requests
from requests.exceptions import RequestException

from Core import baseprocessmanager
from GUI import gui


class GUIProcessManager(baseprocessmanager.BaseProcessManager):
    version = '1.2.1'

    def __init__(self):
        super().__init__()

        if not self.config['api']['steam_api_key']:
            messagebox.showerror('API Key', 'You need a steam API key')
            return
        if not self.config['api']['backpack_tf_api_key']:
            messagebox.showerror('API Key', 'You need a backpack.tf API key')
            return

        self.gui = gui.GUI(self)
        self.gui.splash.set_status('Loading...')

        self.check_update()
        self.start()

        self.update_images()
        self.gui.update_images()
        self.gui.start()

    def show_error(self, error):
        messagebox.showerror('Error', error)

    def check_update(self):
        self.gui.splash.set_status('Checking For Updates...')

        try:
            raw_response = requests.get('http://scanner3server-warmar.rhcloud.com/checkupdate').json()
        except (ValueError, ConnectionError, RequestException):
            self.show_error('There was an error checking for updates.')
            return

        major, minor, patch = raw_response['version'].split('.')
        current_major, current_minor, current_patch = self.version.split('.')
        if current_major >= major:
            if current_minor >= minor:
                if current_patch >= patch:
                    return
        messagebox.showinfo('Update', raw_response['message'])

    def update_schema(self):
        self.gui.splash.set_status('Updating Schema...')
        super().update_schema()

    def update_images(self):
        self.gui.splash.set_status('Updating Images...')
        item_schema = self.read_schema('ItemSchema.txt')
        for item in item_schema:
            if not item['image_url']:
                continue
            if 'Paint Can' in item['name']:
                if not os.path.isfile('Resources/Items/Paint/%s.png' % item['item_name']):
                    self.show_error('Missing Paint Image: %s' % item['item_name'])
                    sys.exit()
                continue
            file_name = item['item_name'].replace('?', '')
            file_name = file_name.replace(':', '')
            file_name = file_name.replace('/', '')
            if not os.path.exists('Resources/Items/%s.png' % file_name):
                with open('Resources/Items/%s.png' % file_name, 'wb+') as write_item_image:
                    image = requests.get(item['image_url']).content
                    write_item_image.write(image)

    def update_pricelist(self):
        self.gui.splash.set_status('Updating Pricelist...')
        super().update_pricelist()

    def update_market_pricelist(self):
        self.gui.splash.set_status('Updating Market Pricelist...')
        super().update_market_pricelist()

    def end(self):
        def func():
            self.gui.protocol('WM_DELETE_WINDOW', lambda: None)

            if self.gui.tabs:
                for tab in self.gui.tabs:
                    if tab.scan is not None:
                        tab.scan.end()
                while [tab for tab in self.gui.tabs if tab.scan is not None]:
                    time.sleep(0.01)
            self.request_manager.end()
            self.gui.quit()
            sys.exit()

        threading.Thread(target=func).start()
