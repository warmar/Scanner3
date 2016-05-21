#!/usr/bin/env python3

from Scans import idsprocessor
from GUI import idsoptions
from GUI import basetab


class IDsTab(basetab.BaseTab):
    def __init__(self, process_manager):
        super().__init__(process_manager)

        self.scan = None

        self.create_widgets()

        self.create_options('ids')

    def open_options(self):
        idsoptions.IDsOptions(self)

    def start_scan(self):
        self.scan = idsprocessor.IDsProcessor(self.process_manager, self)
        self.scan.start()
