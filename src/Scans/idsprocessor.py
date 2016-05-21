#!/usr/bin/env python3

from Scans import basescan


class IDsProcessor(basescan.BaseScan):
    def __init__(self, process_manager, tab):
        super().__init__(process_manager, tab)

        self.input_text = self.tab.input_text.get('0.0', 'end-1c')

    def run(self):
        self.tab.scan_button.config(image=self.process_manager.gui.xshark, command=self.end)

        self.steam_id64s = self.find_ids(self.input_text)
        self.mark_time()

        if not self.steam_id64s:
            self.set_status('No IDs Found', 0, 0)
            self.finish()
            return

        self.tab.clear_output(self.steam_id64s)
        self.scan()

        self.finish()

    def set_status(self, message, value, maximum):
        self.tab.progress_label.config(text=message)
        self.tab.progressbar.config(value=value, maximum=maximum)

    def reset_button(self):
        self.tab.scan_button.config(image=self.process_manager.gui.shark, command=self.tab.start_scan)
