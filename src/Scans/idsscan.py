#!/usr/bin/env python3

from Scans import basescan


class IDsScan(basescan.BaseScan):
    def __init__(self, process_manager, scan_monitor, input_text):
        super().__init__(process_manager, scan_monitor)

        self.input_text = input_text

    def run(self):
        self.steam_id64s = self.find_ids(self.input_text)
        self.mark_time()

        if not self.steam_id64s:
            self.scan_monitor.report_status('No IDs Found', 0, 0)
            self.scan_monitor.report_finished_scan(self)
            return

        self.scan_monitor.report_steam_id64s(self.steam_id64s)
        self.scan()
        self.scan_monitor.report_finished_scan(self)
