#!/usr/bin/env python3

from Core import baseprocessmanager
from Core.globals import SKINS, WEARS, QUALITIES


class Item:
    def __init__(self, process_manager: baseprocessmanager.BaseProcessManager, data=None):
        if not data:
            data = {}
        self.process_manager = process_manager

        self.current_id = data.get('id', None)
        self.original_id = data.get('original_id', None)
        if self.original_id is None:
            self.original_id = data.get('_id', None)
        self.defindex = data.get('defindex', None)
        self.level = data.get('level', None)
        self.quantity = data.get('quantity', None)
        self.quality = data.get('quality', None)
        self.origin = data.get('origin', None)
        self.attributes = data.get('attributes', {})
        self.craftable = data.get('craftable', None)
        self.tradable = data.get('tradable', None)

    def is_traded(self):
        return not self.original_id == self.current_id

    def is_australium(self):
        if [attribute for attribute in self.attributes if attribute['defindex'] == 2027]:
            return True
        return False

    def get_name(self):
        if self.is_australium():
            return 'Australium %s' % self.process_manager.item_schema[self.defindex]['item_name']

        if self.defindex in SKINS:
            name = SKINS[self.defindex]
            wear = None
            festive = False
            for attribute in self.attributes:
                if attribute['defindex'] == 725:
                    wear = WEARS[round(attribute['float_value'], 1)]
                if attribute['defindex'] == 2053:
                    festive = True
            if festive:
                name = 'Festive ' + name
            return '%s (%s)' % (name, wear)

        return self.process_manager.item_schema[self.defindex]['item_name']

    def get_display_name(self):
        name = ''
        if self.quality in (0, 1, 3, 5, 7, 8, 9, 11, 13, 14):
            name += QUALITIES[self.quality]['name'] + ' '

        if self.defindex in SKINS:
            wear = None
            festive = False
            for attribute in self.attributes:
                if attribute['defindex'] == 725:
                    wear = WEARS[round(attribute['float_value'], 1)]
                if attribute['defindex'] == 2053:
                    festive = True
            if festive:
                name += 'Festive '
            name += SKINS[self.defindex]
            return '%s (%s)' % (name, wear)

        name += self.process_manager.item_schema[self.defindex]['item_name']

        for attribute in self.attributes:
            if attribute['defindex'] == 187:
                name += ' #%s' % attribute['float_value']

        return name

    def get_price_index(self):
        for attribute in self.attributes:
            # Attach Particle Effect
            if attribute['defindex'] == 134:
                return str(attribute['float_value'])
            # Set Supply Crate Series
            if attribute['defindex'] == 187:
                return str(attribute['float_value'])
            # Tool Target Item
            if attribute['defindex'] == 2012:
                return str(attribute['float_value'])
            # Taunt Particle Effect
            if attribute['defindex'] == 2041:
                return str(attribute['value'])
            # Chemistry Sets
            if attribute['defindex'] in range(2000, 2010):
                if attribute['is_output']:
                    return '{0}-{1}'.format(attribute['itemdef'], attribute['quality'])
        return '0'

    def get_prices(self):
        if self.get_name() not in self.process_manager.price_list:
            return self.get_market_prices()
        prices = self.process_manager.price_list[self.get_name()]['prices']

        if str(self.quality) not in prices:
            return None
        prices = prices[str(self.quality)]

        if ('Tradable' if self.tradable else 'Non-Tradable') not in prices:
            return None
        prices = prices['Tradable' if self.tradable else 'Non-Tradable']

        if ('Craftable' if self.craftable else 'Non-Craftable') not in prices:
            return None
        prices = prices['Craftable' if self.craftable else 'Non-Craftable']

        if isinstance(prices, dict):
            if self.get_price_index() not in prices:
                return None
            prices = prices[self.get_price_index()]
        else:
            prices = prices[0]

        return prices

    def get_market_prices(self):
        return None # TODO: Add new implementation of market prices
        if self.quality in (6, 15):
            full_name = self.get_name()
        else:
            full_name = QUALITIES[self.quality]['name'] + ' ' + self.get_name()

        if full_name not in self.process_manager.market_price_list:
            return None

        usd_value = self.process_manager.market_price_list[full_name]['value']
        key_value = round(usd_value / self.process_manager.market_price_list['Mann Co. Supply Crate Key']['value'], 2)
        refined_value = key_value * self.process_manager.key_price

        prices = {'currency': 'keys', 'value': key_value, 'value_raw': refined_value}

        return prices

    def get_raw_price(self):
        prices = self.get_prices()
        if prices is None:
            return None
        return prices['value_raw']

    def get_price(self, currency):
        prices = self.get_prices()
        if not prices:
            return 'None'

        if currency == 'Refined':
            return '%s Refined' % prices['value_raw']
        elif currency == 'Keys':
            if prices['value_raw'] == self.process_manager.key_price:
                return '1 Key'
            else:
                return '%s Keys' % round((prices['value_raw'] / self.process_manager.key_price), 2)
        else:
            if prices['value'] == 1 and prices['currency'] == 'keys':
                return '1 Key'
            else:
                if prices['currency'] == 'keys':
                    return '%s Keys' % prices['value']
                if prices['currency'] == 'metal':
                    return '%s Refined' % prices['value']
                if prices['currency'] == 'usd':
                    return '%s USD' % prices['value']

    def check(self, requirements):
        if 'defindex' in requirements:
            if self.defindex not in requirements['defindex']:
                return False
        if 'value' in requirements:
            if (self.get_raw_price() or 0) < requirements['value']:
                return False
        if 'quality' in requirements:
            if self.quality != requirements['quality']:
                return False
        if 'index' in requirements:
            if self.get_price_index() != requirements['index']:
                return False
        if 'level' in requirements:
            if self.level != requirements['level']:
                return False
        if 'craftable' in requirements:
            if self.craftable != requirements['craftable']:
                return False
        if 'tradable' in requirements:
            if self.tradable != requirements['tradable']:
                return False
        if 'traded' in requirements:
            if self.is_traded() != requirements['traded']:
                return False
        if 'australium' in requirements:
            if self.is_australium() != requirements['australium']:
                return False
        return True
