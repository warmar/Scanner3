#!/usr/bin/env python3

from Core import requestmanager
from GUI import gui
import configparser
import threading
import requests
import time
import json
import sys
import os
from tkinter import messagebox

SCHEMA_URL = 'http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key=%s&language=en'
PRICELIST_URL = 'http://backpack.tf/api/IGetPrices/v4/?key=%s&raw=1'


class ProcessManager:

    version = '1.1.3'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        if not self.config['api']['steam_api_key']:
            messagebox.showerror('API Key', 'You need a steam API key')
            return
        if not self.config['api']['backpack_tf_api_key']:
            messagebox.showerror('API Key', 'You need a backpack.tf API key')
            return

        self.gui = gui.GUI(self)
        self.gui.splash.set_status('Loading...')

        self.check_update()
        self.update_schema()
        self.update_pricelist()

        self.item_schema = self.read_schema('ItemSchema.txt')
        self.particle_effect_schema = self.read_schema('ParticleEffectSchema.txt')
        self.process_schemas()

        self.price_list = self.read_schema('PriceList.txt')
        self.refined_price = self.price_list['Refined Metal']['prices']['6']['Tradable']['Craftable'][0]['value']
        self.key_price = self.price_list[
            'Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0]['value_raw']

        self.request_manager = requestmanager.RequestManager(self)
        self.request_manager.start()

        self.gui.update_images()
        self.gui.add_tab()
        self.gui.main()

    def check_update(self):
        self.gui.splash.set_status('Checking For Updates...')
        raw_response = requests.get('http://scanner3server-warmar.rhcloud.com/checkupdate').json()
        major, minor, patch = raw_response['version'].split('.')
        current_major, current_minor, current_patch = self.version.split('.')
        if current_major >= major:
            if current_minor >= minor:
                if current_patch >= patch:
                    return None
        messagebox.showinfo('Update', raw_response['message'])

    def update_schema(self):
        if os.path.getmtime('Resources/ItemSchema.txt') < (time.time() - 300):
            self.gui.splash.set_status('Updating Schema...')

            try:
                raw_schema = requests.get(SCHEMA_URL % self.config['api']['steam_api_key']).json()
            except ValueError:
                messagebox.showerror('Error', 'Schema Update Error')
                sys.exit()

            item_schema = raw_schema['result']['items']
            particle_effect_schema = raw_schema['result']['attribute_controlled_attached_particles']
            for item in item_schema:
                if not item['image_url']:
                    continue
                if 'Paint Can' in item['name']:
                    continue
                file_name = item['item_name'].replace('?', '')
                file_name = file_name.replace(':', '')
                if not os.path.exists('Resources/Items/%s.png' % file_name):
                    with open('Resources/Items/%s.png' % file_name, 'wb+') as write_item_image:
                        image = requests.get(item['image_url']).content
                        write_item_image.write(image)
            with open('Resources/ItemSchema.txt', 'wb') as write_item_schema:
                write_item_schema.write(json.dumps(item_schema).encode())
            with open('Resources/ParticleEffectSchema.txt', 'wb') as write_particle_effect_schema:
                write_particle_effect_schema.write(json.dumps(particle_effect_schema).encode())

    def update_pricelist(self):
        if os.path.getmtime('Resources/PriceList.txt') < (time.time() - 300):
            self.gui.splash.set_status('Updating Pricelist...')

            try:
                raw_prices = requests.get(PRICELIST_URL % self.config['api']['backpack_tf_api_key']).json()
            except ValueError:
                messagebox.showerror('Error', 'Pricelist Update Error')
                sys.exit()

            price_list = raw_prices['response']['items']
            with open('Resources/PriceList.txt', 'wb') as write_price_list:
                write_price_list.write(json.dumps(price_list).encode())

    def read_schema(self, schema_name):
        with open('Resources/{0}'.format(schema_name), 'rb') as read_schema:
            try:
                schema = json.loads(read_schema.read().decode())
            except ValueError:
                messagebox.showerror('Error', 'Schema Read Error')
                sys.exit()
        return schema

    def process_schemas(self):
        self.item_schema = {item['defindex']: item for item in self.item_schema}
        self.particle_effect_schema = {effect['id']: effect for effect in self.particle_effect_schema}

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
