#!/usr/bin/env python3

import idsprocessor
import requestmanager
import configparser
import threading
import time
import gui
import sys


class ProcessManager:
    def __init__(self):
        self.item_schema = self.read_schema('ItemSchema.txt')
        self.particle_effect_schema = self.read_schema('ParticleEffectSchema.txt')
        self.process_schemas()

        self.price_list = self.read_schema('PriceList.txt')
        self.refined_price = (self.price_list['Refined Metal']['prices']['6']['Tradable']['Craftable']['0']['value'])
        self.key_price = (self.price_list['Mann Co. Supply Crate Key']['prices']
                          ['6']['Tradable']['Craftable']['0']['value_raw'])

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.gui = gui.GUI(self)
        self.request_manager = requestmanager.RequestManager(self)

        self.running_scans = []

        self.request_manager.start()
        self.gui.mainloop()

        self.config.write(open('config.ini', 'w'))

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
