# -*- coding: utf-8 -*-

import json

import xbmc # pylint: disable=import-error

class MonitorMethod():
    VIDEO_LIBRARY_ON_UPDATE = 'VideoLibrary.OnUpdate'


class KodiMonitor(xbmc.Monitor):

    def __init__(self):
        self.listeners = { }

    def on(self, method, callback):
        method_listeners = self.listeners.get(method, [])
        method_listeners.append(callback)
        self.listeners[method] = method_listeners

    def run_till_abort(self, wait_time):
        while not self.abortRequested():
        # Sleep/wait for abort for `wait_time` seconds
            if self.waitForAbort(wait_time):
                # Abort was requested while waiting. We should exit
                break

    def onScanStarted(self, library):
        pass

    def onScanFinished(self, library):
        pass

    def onNotification(self, sender, method, data):
        if sender != 'xbmc':
            return
        json_data = json.loads(data)
        callbacks = self.listeners.get(method, [])
        for callback in callbacks:
            callback(json_data)


    def onPlayerStopped(self, item_id):
        pass