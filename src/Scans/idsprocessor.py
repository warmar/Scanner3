#!/usr/bin/env python3

from Scans import basescan


class IDsProcessor(basescan.BaseScan):
    name = 'ids'

    def __init__(self, process_manager):
        basescan.BaseScan.__init__(self, process_manager)

        self.input_text = self.process_manager.gui.ids_input_text.get('0.0', 'end-1c')

    def run(self):
        self.process_manager.gui.ids_scan_button.config(image=self.process_manager.gui.xshark, command=self.end)

        self.steam_id64s = self.find_ids(self.input_text)
        self.mark_time()

        if not self.steam_id64s:
            self.set_status('No IDs Found', 0, 0)
            self.finish()
            return

        self.process_manager.gui.clear_output('ids', self.steam_id64s)
        self.scan()

        self.finish()

    def set_status(self, message, value, maximum):
        self.process_manager.gui.ids_progress_label.config(text=message)
        self.process_manager.gui.ids_progressbar.config(value=value, maximum=maximum)

    def reset_button(self):
        self.process_manager.gui.ids_scan_button.config(image=self.process_manager.gui.shark,
                                                        command=self.process_manager.start_ids_scan)
