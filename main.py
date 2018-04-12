# -*- coding: utf-8 -*-

from resources.lib import kodilogging
from resources.lib import service

import xbmcaddon # pylint: disable=import-error

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
kodilogging.config()

service.run()