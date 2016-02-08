#!/usr/bin/env python3

import idsprocessor
import requestmanager
import configparser
import threading
import requests
import time
import gui
import sys
import os

SCHEMA_URL = 'http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key=%s&language=en'
PRICELIST_URL = 'http://backpack.tf/api/IGetPrices/v4/?key=%s&raw=1'


class ProcessManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.update_schema()
        self.update_pricelist()

        self.item_schema = self.read_schema('ItemSchema.txt')
        self.particle_effect_schema = self.read_schema('ParticleEffectSchema.txt')
        self.process_schemas()

        self.price_list = self.read_schema('PriceList.txt')
        self.refined_price = (self.price_list['Refined Metal']['prices']['6']['Tradable']['Craftable']['0']['value'])
        self.key_price = (self.price_list['Mann Co. Supply Crate Key']['prices']
                          ['6']['Tradable']['Craftable']['0']['value_raw'])

        self.gui = gui.GUI(self)
        self.request_manager = requestmanager.RequestManager(self)

        self.running_scans = []

        self.request_manager.start()
        self.gui.mainloop()

        self.config.write(open('config.ini', 'w'))

    def update_schema(self):
        if os.path.getmtime('Resources/ItemSchema.txt') < (time.time() - 300):
            print('Updating Schema')
            raw_schema = requests.get(SCHEMA_URL % self.config['api']['steam_api_key']).json()
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
                write_item_schema.write(repr(item_schema).encode())
            with open('Resources/ParticleEffectSchema.txt', 'wb') as write_particle_effect_schema:
                write_particle_effect_schema.write(repr(particle_effect_schema).encode())

    def update_pricelist(self):
        if os.path.getmtime('Resources/PriceList.txt') < (time.time() - 300):
            print('Updating Pricelist')
            raw_prices = requests.get(PRICELIST_URL % self.config['api']['backpack_tf_api_key']).json()
            price_list = raw_prices['response']['items']
            with open('Resources/PriceList.txt', 'wb') as write_price_list:
                write_price_list.write(repr(price_list).encode('utf-8'))

    def read_schema(self, schema_name):
        with open('Resources/{0}'.format(schema_name), 'rb') as read_schema:
            schema = eval(read_schema.read().decode())
        return schema

    def process_schemas(self):
        self.item_schema = {item['defindex']: item for item in self.item_schema}
        self.particle_effect_schema = {effect['id']: effect for effect in self.particle_effect_schema}

    def start_ids_scan(self):
        scan = idsprocessor.IDsProcessor(self)
        self.running_scans.append(scan)
        scan.start()

    def finish_scan(self, scan):
        self.running_scans.remove(scan)

    def end(self):
        def func():
            self.gui.protocol('WM_DELETE_WINDOW', lambda: None)

            if self.running_scans:
                for scan in self.running_scans:
                    scan.end()
                while self.running_scans:
                    time.sleep(0.01)
            self.request_manager.end()
            self.gui.quit()
            sys.exit()
        threading.Thread(target=func).start()
