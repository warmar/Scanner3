#! python3

import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['api']['backpack_tf_api_key']

raw_prices = requests.get('http://backpack.tf/api/IGetPrices/v4/?key={0}&raw=1'.format(api_key)).json()
price_list = raw_prices['response']['items']

with open('Resources/PriceList.txt', 'wb') as write_price_list:
    write_price_list.write(repr(price_list).encode('utf-8'))
