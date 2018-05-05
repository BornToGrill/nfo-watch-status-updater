# -*- coding: utf-8 -*-

from resources.lib.borntogrill.kodi_monitor import KodiMonitor
from resources.lib.borntogrill.kodi_notification_handler import KodiNotificationHandler

import logging

import xbmcaddon # pylint: disable=import-error

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
logger = logging.getLogger(ADDON_ID)

def run():
    logger.debug('Starting monitor')

    monitor = KodiMonitor()
    handler = KodiNotificationHandler(monitor)

    wait_time = 60
    handler.run_till_abort(wait_time)

    logger.debug('Service closing down')
