# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import json
import hashlib
import requests
import logging

__version__ = 1.5

HOST_DEFALUT = 'http://127.0.0.1:8009'
PYRAMID_SETTINGS = {'EASTER_HOST': HOST_DEFALUT}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('log/pyramid.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
  from django.conf import settings
  HOST = getattr(settings, 'EASTER_HOST', HOST_DEFALUT)
except ImportError:
  settings = PYRAMID_SETTINGS
  HOST = HOST_DEFALUT

POST_URL = '%s/api/v1/event/' %HOST
QUERY_URL = POST_URL
EVENTS_URL = '%s/api/v1/user/' %HOST

def sorted_json(aim_item):
  if isinstance(aim_item, (basestring, int, long, float, bool)):
    return str(aim_item)
  elif isinstance(aim_item, (set, list, tuple)):
    return '&'.join([sorted_json(item) for item in aim_item])

  result = ''
  for key in sorted(aim_item.iterkeys()):
    result = result + '&' + json.dumps({key: sorted_json(aim_item[key])})
  return result

def md5_sig(json_data):
  m = hashlib.md5()
  m .update(sorted_json(json_data))
  sig = m.hexdigest()
  return sig

class API():
  def __init__(self):
    self.host = HOST

  def post(self, app_name, user_info, events):
    """
      Post event data to log server.
      :Params app_name str: The register app name.
      :Params user_info dict:  It contains uid & cookie. Like {'uid': 'ccy', 'cookie': 'abcdef'}
      :Params events list: It contains event info, likes event_name, origin, text, datetime etc
      @return status_code: Like 200, 400, 403, 404, same as Http response status.
    """
    json_data = {
      'app_name': app_name,
      'user_info': user_info,
      'events': events
    }
    sig = md5_sig(json_data)
    info = {
      'sig': sig,
      'app_name': app_name,
      'user_info': json.dumps(user_info),
      'events': json.dumps(events)
    }

    headers = {'content-type': 'application/json'}

    logger.info("Url: %s, app: %s, user_id %s " %
                (POST_URL, app_name, user_info.get('uid', '')))
    r = requests.post(url=POST_URL, data=json.dumps(info), headers=headers)
    logger.info("Status_code %r" % r.status_code)
    return r.status_code

  def query(self, app_name, query, fields=[]):
    """
      Get statistics data from log server.
      :Params app_name str: The register app name.
      :Params query dict: Query dict, which contains collection_name, from_datetime, to_datetime.
      :Params fields list: The fields wanted, return [] if fields is None.
      @return json_str with full info, use json.loads to decode them.
    """
    info = {
      'app_name': app_name,
      'query': json.dumps(query),
      'fields': json.dumps(fields)
    }
    r = requests.get(url=QUERY_URL, params=info)
    return r.content

  def events(self, uid, from_datetime, to_datetime):
    """
      Get user events falls from log server.
      :Params uid, which user's events. if uid = None, return everyone.
      :from_datetime str: From which time.
      :to_datetime str: To which time
      @return json_str with full info, use json.loads to decode them
    """
    info = {
      'uid': uid,
      'from_datetime': from_datetime,
      'to_datetime': to_datetime
    }
    r = requests.get(url=EVENTS_URL, params=info)
    return r.content
