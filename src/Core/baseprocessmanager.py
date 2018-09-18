#!/usr/bin/env python3

import configparser
import json
import os
import sys
import time

import requests

from Core.analytics import report_launch
from Core import requestmanager
from Core.globals import SCHEMA_ITEMS_URL, SCHEMA_OVERVIEW_URL, PRICELIST_URL


class BaseProcessManager:
    def __init__(self):
        if not os.path.exists('config.ini'):
            self.show_error('Could not find config.ini')
            sys.exit(1)
        if not os.path.exists('Resources/'):
            self.show_error('Could not find Resources folder')
            sys.exit(1)

        self.config = configparser.ConfigParser()
        try:
            self.config.read('config.ini')
        except:
            self.show_error('Invalid config file.\n'
                            'Try re-downloading the default file.')
            sys.exit(1)

        self.scan_monitors = []

    def start(self):
        report_launch()

        self.update_schema()
        self.update_pricelist()

        self.item_schema = self.read_schema('ItemSchema.txt')
        self.particle_effect_schema = self.read_schema('ParticleEffectSchema.txt')
        self.process_schemas()

        self.price_list = self.read_schema('PriceList.txt')
        # self.market_price_list = self.read_schema('MarketPriceList.txt')

        self.refined_price = self.price_list['Refined Metal']['prices']['6']['Tradable']['Craftable'][0]['value']
        self.key_price = self.price_list['Mann Co. Supply Crate Key']['prices']['6']['Tradable']['Craftable'][0][
            'value_raw']

        self.request_manager = requestmanager.RequestManager(self)
        self.request_manager.start()

    def show_error(self, error):
        print(error)

    def update_schema(self):
        # Only update if cached version is more than 5 minutes old
        if os.path.isfile('Resources/ItemSchema.txt') and os.path.isfile('Resources/ParticleEffectSchema.txt'):
            if os.path.getmtime('Resources/ItemSchema.txt') > (time.time() - 300) and os.path.getmtime('Resources/ParticleEffectSchema.txt') > (time.time()-300):
                return True

        success = self.update_particle_effects()
        if not success:
            return False

        success = self.update_item_schema()
        if not success:
            return False

        return True

    def update_item_schema(self):
        # Get paginated schema items
        next_defindex = 0
        done = False
        item_schema = []
        while not done:
            # Make request
            try:
                response = requests.get(SCHEMA_ITEMS_URL.format(self.config['api']['steam_api_key'], next_defindex),
                                        timeout=30)
            except:
                self.show_error('There was an error updating the item schema.\nTry again in a few minutes.')
                return False

            # Check request status
            if response.status_code != 200:
                self.show_error('There was an error updating the item schema.\n'
                                'Your API key may be invalid. Double check your config file.\n'
                                '\n'
                                'Response:\n'
                                '\n'
                                '%s' % response.text)
                return False

            # Decode response and extend schema by items on current page
            try:
                raw_schema_items_page = response.json()
                item_schema.extend(raw_schema_items_page['result']['items'])
            except:
                self.show_error('There was an error updating the item schema.\n'
                                'Try again in a few minutes.')
                return False

            # Check for next item index
            if 'next' in raw_schema_items_page['result']:
                next_defindex = raw_schema_items_page['result']['next']
            else:
                done = True

        # Cache results
        with open('Resources/ItemSchema.txt', 'wb') as write_item_schema:
            write_item_schema.write(json.dumps(item_schema).encode())

        return True

    def update_particle_effects(self):
        # Make request
        try:
            response = requests.get(SCHEMA_OVERVIEW_URL % self.config['api']['steam_api_key'], timeout=30)
        except:
            self.show_error('There was an error updating the item schema.\n'
                            'Try again in a few minutes.')
            return False

        # Check request status
        if response.status_code != 200:
            self.show_error('There was an error updating the item schema.\n'
                            'Your API key may be invalid. Double check your config file.\n'
                            '\n'
                            'Response:\n'
                            '\n'
                            '%s' % response.text)
            return False

        # Decode response and extract particle effects
        try:
            raw_schema_overview = response.json()
            particle_effect_schema = raw_schema_overview['result']['attribute_controlled_attached_particles']
        except:
            self.show_error('There was an error updating the item schema.\n'
                            'Try again in a few minutes.')
            return False

        # Cache particle effects
        with open('Resources/ParticleEffectSchema.txt', 'wb') as write_particle_effect_schema:
            write_particle_effect_schema.write(json.dumps(particle_effect_schema).encode())

        return True

    def update_pricelist(self):
        # Only update if cached version is more than 5 minutes old
        if os.path.isfile('Resources/PriceList.txt'):
            if os.path.getmtime('Resources/PriceList.txt') > (time.time() - 300):
                return True

        # Make request
        try:
            response = requests.get(PRICELIST_URL % self.config['api']['backpack_tf_api_key'], timeout=30)
        except:
            self.show_error('There was an error updating the price list.\n'
                            'Try again in a few minutes.')
            return False

        # Check request status
        if response.status_code != 200:
            self.show_error('There was an error updating the price list.\n'
                            'Your API key may be invalid.\n'
                            '\n'
                            'Response:\n'
                            '\n'
                            '%s' % response.text)
            return False


        # Decode response and extract pricelist
        try:
            raw_prices = response.json()
            price_list = raw_prices['response']['items']
        except:
            self.show_error('There was an error updating the price list.\n'
                            'Try again in a few minutes.')
            return False

        # Cache results
        with open('Resources/PriceList.txt', 'wb') as write_price_list:
            write_price_list.write(json.dumps(price_list).encode())

        return True

    def read_schema(self, schema_name):
        with open('Resources/{0}'.format(schema_name), 'rb') as read_schema:
            try:
                schema = json.loads(read_schema.read().decode())
            except ValueError:
                self.show_error('There was an error reading %s.\nTry deleting the file and restarting.' % schema_name)
                sys.exit(1)
        return schema

    def process_schemas(self):
        self.item_schema = {item['defindex']: item for item in self.item_schema}
        self.particle_effect_schema = {effect['id']: effect for effect in self.particle_effect_schema}

    def report_finished_scan_monitor(self, scan_monitor):
        pass

    def update_progress(self):
        pass
