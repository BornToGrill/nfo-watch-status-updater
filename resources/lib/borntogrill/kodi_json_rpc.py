# -*- coding: utf-8 -*-

from resources.lib.borntogrill.kodi_utils import kodi_json_request

import json

import xbmc # pylint: disable=import-error

def construct_request(method, params):
    return {
        'jsonrpc': '2.0',
        'id': '1',
        'method': method,
        'params': params
    }

def send_request(method, params):
    message = construct_request(method, params)
    return kodi_json_request(message)


class VideoLibrary():

    @staticmethod
    def get_movie_details(id):
        return send_request('VideoLibrary.GetMovieDetails', {
            'movieid': id,
            'properties': [
                'file'
            ]
        })
    
    @staticmethod
    def get_episode_details(id):
        return send_request('VideoLibrary.GetEpisodeDetails', {
            'episodeid': id,
            'properties': [
                'file'
            ]
        })