import zipfile
import configparser
import sys
import os

version = input('Version: ')

config = configparser.ConfigParser()
config.read('distwin/config.ini')
if config['api']['steam_api_key'] != '' or config['api']['backpack_tf_api_key'] != '':
    print('API Key Not Blank')
    sys.exit()

os.chdir('distwin/')

distribution = zipfile.ZipFile('../distwin%s.zip' % version, 'w', zipfile.ZIP_LZMA)
for root, dirs, files in os.walk('.'):
    for file in files:
        distribution.write(os.path.join(root, file))
