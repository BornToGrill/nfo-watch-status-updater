# -*- coding: utf-8 -*-

from resources.lib.borntogrill import kodi_logging
from resources.lib import service

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this

kodi_logging.config()

service.run()