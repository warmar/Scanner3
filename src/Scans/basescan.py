#!/usr/bin/env python3

from Core.player import Player
import threading
import time
import re

GET_SUMMARIES_URL = 'http://api.steampowered.com/isteamuser/getplayersummaries/v2/?key={0}&steamids=%s'


class BaseScan(threading.Thread):
    name = 'base'

    def __init__(self, process_manager):
        threading.Thread.__init__(self)
        self.process_manager = process_manager

        self.end_ = False
        self.start_time = None

        self.done = 0
        self.total = 0

        self.players_processor = None
        self.steam_id64s = []
        self.requirements = {}

    def run(self):
        pass

    def finish(self):
        self.reset_button()
        self.process_manager.finish_scan(self)

    def end(self):
        if self.end_:
            return
        self.end_ = True
        self.configure_ending()

    def find_ids(self, input_text):
        default_id = (1 << 56) | (1 << 52) | (1 << 32)
        steam_id64s = []

        raw_ids = re.findall('[\d]+', input_text)
        for id64 in raw_ids:
            if (int(id64) & default_id) == default_id:
                steam_id64s.append(int(id64))

        steam_id32s = re.findall('STEAM_0:[\d]:[\d]+', input_text, re.VERBOSE)
        for id32 in steam_id32s:
            x, y, z = re.findall('[\d]+', id32)
            id64 = default_id | (int(z) << 1) | int(y)
            steam_id64s.append(id64)

        steam_id3s = re.findall('([U:[\d]:[\d]+])', input_text, re.VERBOSE)
        for id3 in steam_id3s:
            id64 = default_id | int(re.findall('[\d]+', id3)[1])
            steam_id64s.append(id64)

        return list(set(steam_id64s))

    def get_max_hours(self):
        if not self.process_manager.config[self.name]['max_hours']:
            return None
        return int(self.process_manager.config[self.name]['max_hours'])

    def get_minimum_item_value(self):
        return float(self.process_manager.config[self.name]['raw_minimum_item_value'])

    def get_minimum_player_value(self):
        return float(self.process_manager.config[self.name]['raw_minimum_player_value'])

    def get_player_summaries(self, players):
        steam_id64s = [player.id64 for player in players]
        url = GET_SUMMARIES_URL.format(self.process_manager.config['api']['steam_api_key']) % steam_id64s
        raw_summaries = self.process_manager.request_manager.make_api_request(url,
                                                                              mode='json',
                                                                              priority=False,
                                                                              tags=(self.name,))

        if self.end_:
            return

        summaries = {int(summary['steamid']): summary for summary in raw_summaries['response']['players']}
        for player in players:
            if player.id64 in summaries:
                if summaries[player.id64]['communityvisibilitystate'] == 1:
                    continue
                if 'lastlogoff' not in summaries[player.id64]:
                    continue
                player.name = summaries[player.id64]['personaname']
                player.avatar = summaries[player.id64]['avatarmedium']
                player.status = summaries[player.id64]['personastate'] if 'gameid' not in summaries[player.id64] else -1
                player.last_online = summaries[player.id64]['lastlogoff']

    def scan(self):
        start_time = time.time()
        summary_thread = None
        hours_threads = []
        item_threads = []
        display_threads = []

        ids = self.steam_id64s[:]
        players = []
        pending = []
        ready = []
        current_items = []
        current_hours = []
        done = []

        self.done = 0
        self.total = len(ids)

        self.update_progress()

        while ids or players or pending or ready or current_items or current_hours or done:
            time.sleep(0.01)
            if self.end_:
                request_cancel_threads = [threading.Thread(target=self.process_manager.request_manager.cancel_requests,
                                                           args=(self.name,))]
                request_cancel_threads[-1].start()
                for id64 in self.steam_id64s:
                    request_cancel_threads.append(threading.Thread(
                            target=self.process_manager.request_manager.cancel_requests, args=(id64,)))
                    request_cancel_threads[-1].start()

                for request_cancel_thread in request_cancel_threads:
                    request_cancel_thread.join()
                if summary_thread is not None:
                    summary_thread.join()
                for hours_thread in hours_threads:
                    hours_thread.join()
                for item_thread in item_threads:
                    item_thread.join()
                for display_thread in display_threads:
                    display_thread.join()
                self.set_status('Ended - %s %s - %s' % (self.total,
                                                        'Player' if self.total == 1 else 'Players',
                                                        self.run_time(start_time)),
                                0, 0)
                return

            for player in done[:]:
                done.remove(player)
                if self.process_manager.config[self.name]['display_players'] == 'True':
                    if not player.check(self.process_manager.config[self.name]['f2p'],
                                        self.process_manager.config[self.name]['status'],
                                        self.get_max_hours()):
                        continue
                    if not player.check_items(self.requirements,
                                              self.get_minimum_item_value(),
                                              self.get_minimum_player_value()):
                        continue
                    display_threads.append(threading.Thread(target=self.process_manager.gui.display_player,
                                                            args=(self.name, player)))
                    display_threads[-1].start()
                self.done += 1
                self.update_progress()

            for player in current_hours[:]:
                if hours_threads[current_hours.index(player)].is_alive():
                    continue
                del hours_threads[current_hours.index(player)]
                current_hours.remove(player)
                done.append(player)

            for player in current_items[:]:
                if item_threads[current_items.index(player)].is_alive():
                    continue
                del item_threads[current_items.index(player)]
                current_items.remove(player)
                if not player.items:
                    self.done += 1
                    self.update_progress()
                    continue
                if not self.process_manager.config[self.name]['collect_hours'] == 'True':
                    done.append(player)
                    continue
                current_hours.append(player)
                hours_threads.append(threading.Thread(target=player.get_hours))
                hours_threads[-1].start()

            if self.end_:
                continue

            running = len(current_items)+len(current_hours)
            if running < int(self.process_manager.config['technical']['simultaneous_scans']):
                for player in ready[:int(self.process_manager.config['technical']['simultaneous_scans'])-running]:
                    ready.remove(player)

                    current_items.append(player)
                    item_threads.append(threading.Thread(target=player.get_items))
                    item_threads[-1].start()

            if summary_thread is not None:
                if not summary_thread.is_alive():
                    for player in pending[:]:
                        pending.remove(player)
                        if player.status == -2:
                            self.done += 1
                            self.update_progress()
                            continue
                        if not player.check_status(self.process_manager.config[self.name]['status']):
                            self.done += 1
                            self.update_progress()
                            continue
                        if not player.check_last_online(
                                float(self.process_manager.config[self.name]['raw_last_online'])):
                            self.done += 1
                            self.update_progress()
                            continue
                        ready.append(player)

                    summary_thread = None

            if len(ready) < 100:
                if players:
                    if summary_thread is None:
                        pending.extend(players[:100])
                        summary_thread = threading.Thread(target=self.get_player_summaries, args=(players[:100],))
                        summary_thread.start()
                        del players[:100]

            if len(players) < 200:
                for id64 in ids[:200]:
                    player = Player(self.process_manager, id64)
                    ids.remove(id64)
                    players.append(player)

        for display_thread in display_threads:
            display_thread.join()
        self.set_status('Success - %s %s - %s' % (self.total,
                                                  'Player' if self.total == 1 else 'Players',
                                                  self.run_time(self.start_time)),
                        1, 1)

    def mark_time(self):
        self.start_time = time.time()

    def run_time(self, start_time):
        s = round(time.time()-start_time, 1)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        time_string = ''
        if h:
            time_string += '%s %s : ' % (h, 'Hour' if h == 1 else 'Hours')
        if m or h:
            time_string += '%s %s : ' % (m, 'Minute' if m == 1 else 'Minutes')
        time_string += '%s %s' % (s, 'Second' if s == 1 else 'Seconds')
        return time_string

    def configure_ending(self):
        self.set_status('Ending...', 0, 0)

    def set_status(self, message, value, maximum):
        pass

    def reset_button(self):
        pass

    def update_progress(self):
        if not self.end_:
            self.set_status('Players: %s of %s' % (self.done, self.total), self.done, self.total)
