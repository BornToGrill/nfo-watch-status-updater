# -*- coding: utf-8 -*-

import xbmc # pylint: disable=import-error
import xbmcaddon # pylint: disable=import-error
import xbmcgui # pylint: disable=import-error
import sys
import logging
import json as json


# read settings
ADDON = xbmcaddon.Addon()

def notification(header, message, time=5000, icon=ADDON.getAddonInfo('icon'), sound=True):
    xbmcgui.Dialog().notification(header, message, icon, time, sound)

def dialog(header, message, line2=None, line3=None):
    return xbmcgui.Dialog().ok(header, message, line2, line3)


def show_settings():
    ADDON.openSettings()

def get_setting(setting):
    return ADDON.getSetting(setting).strip().decode('utf-8')

def _get_setting_as(setting, as_type):
    value = get_setting(setting)
    return as_type(value)

def get_setting_as_bool(setting):
    return get_setting(setting).lower() == 'true'

def get_setting_as_float(setting):
    return _get_setting_as(setting, float)

def get_setting_as_int(setting):
    return _get_setting_as(setting, int)

def set_setting(setting, value):
    ADDON.setSetting(setting, str(value))


def get_string(string_id):
    return ADDON.getLocalizedString(string_id).encode('utf-8', 'ignore')


def kodi_json_request(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)

    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))

    # 'result' key may not exist. Error handling needs to be done by consumer
    return response['result']
