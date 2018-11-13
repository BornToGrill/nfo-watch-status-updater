# -*- coding: utf-8 -*-


from resources.lib.borntogrill import kodi_utils
from resources.lib.borntogrill.kodi_json_rpc import VideoLibrary
from resources.lib.borntogrill.kodi_nfo_updater import update_nfo
from resources.lib.borntogrill.kodi_monitor import MonitorMethod

import logging
import os

import xbmcaddon # pylint: disable=import-error

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID = ADDON.getAddonInfo('id')
logger = logging.getLogger(ADDON_ID)

class VideoInfo():
    def __init__(self, id, type, playcount):
        self.id = id
        self.type = type
        self.playcount = playcount

class KodiNotificationHandler():
    
    def __init__(self, monitor):
        self.monitor = monitor
        self.monitor.on(
			MonitorMethod.VIDEO_LIBRARY_ON_UPDATE, 
			self.on_video_library_update
		)
    
    def run_till_abort(self, wait_time):
        self.monitor.run_till_abort(wait_time)

    @staticmethod
    def _video_info_from_notification(msg):
        if not msg.has_key('item') or not msg.has_key('playcount'):
            return None

        item = msg['item']
        playcount = msg['playcount']

        if not item.has_key('id') or not item.has_key('type'):
            return None
        
        id = item['id']
        video_type = item['type']
        return VideoInfo(id, video_type, playcount)

    def on_video_library_update(self, obj):
        logger.info("Video library updated: %s", str(obj))
        video_info = self._video_info_from_notification(obj)
        if video_info is None:
            logger.warn('Could not parse video info from update notification')
            return
        
        fetch_strategies = {
            u'movie': {
                'fetch': VideoLibrary.get_movie_details,
                'file_path': lambda x: x['moviedetails']['file']
            },
            u'episode': {
                'fetch': VideoLibrary.get_episode_details,
                'file_path': lambda x: x['episodedetails']['file']
            }
        }
        
        try:
            strategy = fetch_strategies[video_info.type]
            video_details = strategy['fetch'](video_info.id)
            video_file_path = strategy['file_path'](video_details)
            
            nfo_file_path = video_file_path.replace(os.path.splitext(video_file_path)[1], '.nfo')
        except:
            error_message = 'Failed to get video info'
            logger.exception(error_message)
            kodi_utils.notification(ADDON_NAME, error_message)
        
        try:
            update_nfo(nfo_file_path, video_info.playcount)
        except IOError:
            error_message = 'Failed to update NFO. File could not be found'
            logger.exception(error_message)
            kodi_utils.notification(ADDON_NAME, error_message)
        except:
            error_message = 'Failed to update NFO. Check logs for more information'
            logger.exception(error_message)
            kodi_utils.notification(ADDON_NAME, error_message)