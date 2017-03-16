#!/usr/bin/env python3

from GUI import idsoptions, basetab
from Scans import idsprocessor


class IDsTab(basetab.BaseTab):
    name = 'ids'

    def __init__(self, process_manager):
        super().__init__(process_manager)

    def create_options(self):
        self.options = idsoptions.IDsOptions(self)
        self.options.apply()

    def start_scan(self):
        self.update_requirements()

        self.scan = idsprocessor.IDsProcessor(self.process_manager, self, self.input_text.get('0.0', 'end-1c'))
        self.scan_button.config(image=self.process_manager.gui.xshark, command=self.scan.end)
        self.scan.start()
