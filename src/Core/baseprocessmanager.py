#!/usr/bin/env python3

import configparser
import json
import os
import sys
import time

import requests

from Core import requestmanager
from Core.globals import SCHEMA_URL, PRICELIST_URL, MARKET_PRICELIST_URL


class BaseProcessManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def start(self):
        self.update_schema()
        self.update_pricelist()
        self.update_market_pricelist()

        self.item_schema = self.read_schema('ItemSchema.txt')
        self.particle_effect_schema = self.read_schema('ParticleEffectSchema.txt')
        self.process_schemas()

        self.price_list = self.read_schema('PriceList.txt')
        self.market_price_list = self.read_schema('MarketPriceList.txt')

        self.refined_price = self.price_list['Refined Metal']['prices']['6']['Tradable']['Craftable'][0]['value']
        self.key_price = self.price_list['Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0][
            'value_raw']

        self.request_manager = requestmanager.RequestManager(self)
        self.request_manager.start()

    def show_error(self, error):
        print(error)

    def update_schema(self):
        if os.path.isfile('Resources/ItemSchema.txt') and os.path.isfile('Resources/ParticleEffectSchema.txt'):
            if os.path.getmtime('Resources/ItemSchema.txt') > (time.time() - 300) and os.path.getmtime('Resources/ParticleEffectSchema.txt') > (time.time()-300):
                return

        try:
            raw_schema = requests.get(SCHEMA_URL % self.config['api']['steam_api_key']).json()
        except ValueError:
            self.show_error('There was an error updating the item schema.\nTry again in a few minutes.')
            sys.exit()

        try:
            item_schema = raw_schema['result']['items']
            particle_effect_schema = raw_schema['result']['attribute_controlled_attached_particles']
        except KeyError:
            self.show_error('There was an error updating the item schema.\nTry again in a few minutes.')
            sys.exit()

        with open('Resources/ItemSchema.txt', 'wb') as write_item_schema:
            write_item_schema.write(json.dumps(item_schema).encode())
        with open('Resources/ParticleEffectSchema.txt', 'wb') as write_particle_effect_schema:
            write_particle_effect_schema.write(json.dumps(particle_effect_schema).encode())

    def update_pricelist(self):
        if os.path.isfile('Resources/PriceList.txt'):
            if os.path.getmtime('Resources/PriceList.txt') > (time.time() - 300):
                return

        try:
            raw_prices = requests.get(PRICELIST_URL % self.config['api']['backpack_tf_api_key']).json()
        except ValueError:
            self.show_error('There was an error updating the price list.\nTry again in a few minutes.')
            sys.exit()

        try:
            price_list = raw_prices['response']['items']
        except KeyError:
            self.show_error('There was an error updating the price list.\nTry again in a few minutes.')
            sys.exit()

        with open('Resources/PriceList.txt', 'wb') as write_price_list:
            write_price_list.write(json.dumps(price_list).encode())

    def update_market_pricelist(self):
        if os.path.isfile('Resources/MarketPriceList.txt'):
            if os.path.getmtime('Resources/MarketPriceList.txt') > (time.time()-300):
                return

        try:
            raw_market_prices = requests.get(MARKET_PRICELIST_URL % self.config['api']['backpack_tf_api_key']).json()
        except ValueError:
            self.show_error('There was an error updating the market price list.\nTry again in a few minutes.')
            sys.exit()

        try:
            market_price_list = raw_market_prices['response']['items']
        except KeyError:
            self.show_error('There was an error updating the market price list.\nTry again in a few minutes.')
            sys.exit()

        with open('Resources/MarketPriceList.txt', 'wb') as write_market_price_list:
            write_market_price_list.write(json.dumps(market_price_list).encode())

    def read_schema(self, schema_name):
        with open('Resources/{0}'.format(schema_name), 'rb') as read_schema:
            try:
                schema = json.loads(read_schema.read().decode())
            except ValueError:
                self.show_error('There was an error reading %s.\nTry deleting the file and restarting.' % schema_name)
                sys.exit()
        return schema

    def process_schemas(self):
        self.item_schema = {item['defindex']: item for item in self.item_schema}
        self.particle_effect_schema = {effect['id']: effect for effect in self.particle_effect_schema}

    def report_finished_scan_monitor(self, scan_monitor):
        pass

    def update_progress(self):
        pass
