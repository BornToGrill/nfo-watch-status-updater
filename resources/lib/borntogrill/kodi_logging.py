# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from resources.lib.borntogrill.kodi_utils import get_setting_as_bool

import logging

import xbmc # pylint: disable=import-error
import xbmcaddon # pylint: disable=import-error


class KodiLogHandler(logging.StreamHandler):

    LEVELS = {
        logging.CRITICAL: xbmc.LOGFATAL,
        logging.ERROR: xbmc.LOGERROR,
        logging.WARNING: xbmc.LOGWARNING,
        logging.INFO: xbmc.LOGINFO,
        logging.DEBUG: xbmc.LOGDEBUG,
        logging.NOTSET: xbmc.LOGNONE,
    }

    def __init__(self):
        logging.StreamHandler.__init__(self)
        addon_id = xbmcaddon.Addon().getAddonInfo('id')
        prefix = b"[%s] " % addon_id
        formatter = logging.Formatter(prefix + b': %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        try:
            xbmc.log(self.format(record), self.LEVELS[record.levelno])
        except UnicodeEncodeError:
            xbmc.log(self.format(record).encode(
                'utf-8', 'ignore'), self.LEVELS[record.levelno])

    def flush(self):
        pass


def config():
    logger = logging.getLogger()
    logger.addHandler(KodiLogHandler())
    logger.setLevel(logging.DEBUG)
