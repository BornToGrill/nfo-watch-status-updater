# -*- coding: utf-8 -*-

import xbmc # pylint: disable=import-error
import json
from resources.lib.kodiutils import kodi_json_request


def construct_request(method, params):
    return {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': params
    }


class VideoLibrary():

    @staticmethod
    def get_movie_details(id):
        message = construct_request('VideoLibrary.GetMovieDetails', {
            'movieid': id,
            'properties': [
                'file'
            ]
        })
        return kodi_json_request(message)
    
    @staticmethod
    def get_episode_details(id):
        message = construct_request('VideoLibrary.GetEpisodeDetails', {
            'episodeid': id,
            'properties': [
                'file'
            ]
        })
        return kodi_json_request(message)