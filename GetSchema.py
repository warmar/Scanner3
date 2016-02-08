#!/usr/bin/env python3

import configparser
import requests
import os

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['api']['steam_api_key']

raw_schema = requests.get('http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key={0}&language=en'.format(
        api_key)).json()
item_schema = raw_schema['result']['items']
particle_effect_schema = raw_schema["result"]["attribute_controlled_attached_particles"]

for item, index in zip(item_schema, range(len(item_schema))):
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

    if index % 10 == 0:
        print('%d of %d' % (index, len(item_schema)))

with open('Resources/ItemSchema.txt', 'wb') as write_item_schema:
    write_item_schema.write(repr(item_schema).encode())
with open('Resources/ParticleEffectSchema.txt', 'wb') as write_particle_effect_schema:
    write_particle_effect_schema.write(repr(particle_effect_schema).encode())
