#!/usr/bin/env python3

import threading
import time
import xml

import requests
import requests.exceptions
import xmltodict


class RequestManager(threading.Thread):
    def __init__(self, process_manager):
        super().__init__()
        self.process_manager = process_manager

        self.end_ = False
        self.available_requests = 0
        self.request_queue = []
        self.priority_queue = []
        self.running_requests = []

    def run(self):
        self.regulate_requests()

    def end(self):
        self.end_ = True

    def cancel_requests(self, tag=None):
        for request in self.request_queue:
            if (tag is None) or (tag in request['tags']):
                request['cancel'] = True
        for request in self.priority_queue:
            if (tag is None) or (tag in request['tags']):
                request['cancel'] = True
        for request in self.running_requests:
            if (tag is None) or (tag in request['tags']):
                request['cancel'] = True

    def regulate_requests(self):
        last_time = time.time() - int(self.process_manager.config['technical']['request_period'])
        while True:
            if self.end_:
                break
            if not self.process_manager.config['technical']['limit_requests'] == 'True':
                self.available_requests = float('inf')
                time.sleep(0.01)
                continue
            if self.process_manager.config['technical']['limit_requests'] == 'True' and self.available_requests == float('inf'):
                self.available_requests = int(self.process_manager.config['technical']['requests_per_period'])
                time.sleep(0.01)
                continue
            if time.time() - last_time < int(self.process_manager.config['technical']['request_period']):
                time.sleep(0.01)
                continue
            self.available_requests = int(self.process_manager.config['technical']['requests_per_period'])
            last_time = time.time()
            time.sleep(0.01)

    def make_api_request(self, url, mode, priority, tags=(), uses_request=True):
        request = {'tags': tags, 'cancel': False}
        request['id'] = id(request)
        if priority:
            self.priority_queue.append(request)
            while self.priority_queue.index(request) != 0 or self.available_requests < 1:
                if not uses_request:
                    break
                if request['cancel']:
                    self.priority_queue.remove(request)
                    return
                time.sleep(0.01)
            self.priority_queue.remove(request)
        else:
            self.request_queue.append(request)
            while self.priority_queue or self.request_queue.index(request) != 0 or self.available_requests < 1:
                if not uses_request:
                    break
                if request['cancel']:
                    self.request_queue.remove(request)
                    return
                time.sleep(0.01)
            self.request_queue.remove(request)

        if uses_request:
            self.available_requests -= 1
        self.running_requests.append(request)

        try:
            raw_response = requests.get(url, timeout=5)
        except (ConnectionError, TimeoutError, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.running_requests.remove(request)
            if request['cancel']:
                return
            return self.make_api_request(url, mode=mode, priority=priority, tags=tags)

        self.running_requests.remove(request)
        if request['cancel']:
            return

        if mode == 'text':
            return raw_response.text
        if mode == 'json':
            try:
                response = raw_response.json()
            except ValueError:
                return self.make_api_request(url, mode=mode, priority=priority, tags=tags)
            if not response:
                return self.make_api_request(url, mode=mode, priority=priority, tags=tags)
            return response
        elif mode == 'xml':
            try:
                response = xmltodict.parse(raw_response.text)
            except xml.parsers.expat.ExpatError:
                return self.make_api_request(url, mode=mode, priority=priority, tags=tags)
            return response
