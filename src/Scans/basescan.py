#!/usr/bin/env python3
import re
import threading
import time

from Core import baseprocessmanager, scanmonitor
from Core.globals import GET_SUMMARIES_URL
from Core.player import Player


class BaseScan(threading.Thread):
    def __init__(self, process_manager: baseprocessmanager.BaseProcessManager, scan_monitor: scanmonitor.ScanMonitor):
        super().__init__()
        self.process_manager = process_manager
        self.scan_monitor = scan_monitor

        self.end_ = False
        self.start_time = None

        self.done = 0
        self.total = 0

        self.steam_id64s = []

    def run(self):
        pass

    def end(self):
        if self.end_:
            return
        self.end_ = True
        self.scan_monitor.report_status('Ending...', 0, 0)

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

    def get_player_summaries(self, players):
        steam_id64s = [player.id64 for player in players]
        url = GET_SUMMARIES_URL.format(self.process_manager.config['api']['steam_api_key']) % steam_id64s
        raw_summaries = self.process_manager.request_manager.make_api_request(url, mode='json', priority=False, tags=(self.scan_monitor,))

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
        summary_thread = None
        hours_threads = []
        item_threads = []

        players = []
        pending = []
        ready = []
        current_items = []
        current_hours = []
        done = []

        self.done = 0
        self.total = len(self.steam_id64s)

        self.update_progress()

        while self.steam_id64s or players or pending or ready or current_items or current_hours or done:
            time.sleep(0.01)

            # Check end
            if self.end_:
                self.process_manager.request_manager.cancel_requests(self.scan_monitor)
                for player in current_items:
                    self.process_manager.request_manager.cancel_requests(player.id64)
                for player in current_hours:
                    self.process_manager.request_manager.cancel_requests(player.id64)

                if summary_thread is not None:
                    summary_thread.join()
                for hours_thread in hours_threads:
                    hours_thread.join()
                for item_thread in item_threads:
                    item_thread.join()
                self.scan_monitor.report_status('Ended - %s %s - %s' % (self.total, 'Player' if self.total == 1 else 'Players', self.run_time(self.start_time)), 0, 0)
                return

            # Finish players that are done
            for player in done[:]:
                done.remove(player)
                self.done += 1
                self.update_progress()
                if not player.check(self.scan_monitor.f2p, self.scan_monitor.status, self.scan_monitor.max_hours):
                    continue
                if not player.check_items(self.scan_monitor.item_requirements):
                    continue
                self.scan_monitor.report_finished_player(player)

            # Handle hours threads
            for player in current_hours[:]:
                if hours_threads[current_hours.index(player)].is_alive():
                    continue
                del hours_threads[current_hours.index(player)]
                current_hours.remove(player)
                done.append(player)

            # Handle items threads
            for player in current_items[:]:
                if item_threads[current_items.index(player)].is_alive():
                    continue
                del item_threads[current_items.index(player)]
                current_items.remove(player)
                if not player.items:
                    self.done += 1
                    self.update_progress()
                    continue
                if self.scan_monitor.collect_hours is False:
                    done.append(player)
                    continue
                current_hours.append(player)
                hours_threads.append(threading.Thread(target=player.get_hours))
                hours_threads[-1].start()

            # Check end
            if self.end_:
                continue

            # Start item threads as space is available
            running = len(current_items) + len(current_hours)
            if running < int(self.process_manager.config['technical']['simultaneous_scans']):
                for player in ready[:int(self.process_manager.config['technical']['simultaneous_scans']) - running]:
                    ready.remove(player)

                    current_items.append(player)
                    item_threads.append(threading.Thread(target=player.get_items))
                    item_threads[-1].start()

            # Handle finished summary thread
            if summary_thread is not None:
                if not summary_thread.is_alive():
                    for player in pending[:]:
                        pending.remove(player)
                        if player.status == -2:
                            self.done += 1
                            self.update_progress()
                            continue
                        if not player.check_status(self.scan_monitor.status):
                            self.done += 1
                            self.update_progress()
                            continue
                        if not player.check_last_online(self.scan_monitor.raw_minimum_last_online):
                            self.done += 1
                            self.update_progress()
                            continue
                        ready.append(player)

                    summary_thread = None

            # Start summary thread if necessary
            if len(ready) < 100:
                if players:
                    if summary_thread is None:
                        pending.extend(players[:100])
                        summary_thread = threading.Thread(target=self.get_player_summaries, args=(players[:100],))
                        summary_thread.start()
                        del players[:100]

            # Create player objects if necessary
            if len(players) < 100:
                for id64 in self.steam_id64s[:100]:
                    player = Player(self.process_manager, id64)
                    players.append(player)
                del self.steam_id64s[:100]

        self.scan_monitor.report_status('Success - %s %s - %s' % (self.total, 'Player' if self.total == 1 else 'Players', self.run_time(self.start_time)), 1, 1)

    def mark_time(self):
        self.start_time = time.time()

    def run_time(self, start_time):
        s = round(time.time() - start_time, 1)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        time_string = ''
        if h:
            time_string += '%s %s : ' % (h, 'Hour' if h == 1 else 'Hours')
        if m or h:
            time_string += '%s %s : ' % (m, 'Minute' if m == 1 else 'Minutes')
        time_string += '%s %s' % (s, 'Second' if s == 1 else 'Seconds')
        return time_string

    def update_progress(self):
        if not self.end_:
            self.scan_monitor.report_status('Players: %s of %s' % (self.done, self.total), self.done, self.total)
