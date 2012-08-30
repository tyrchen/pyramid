# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import json
import md5
import requests

__version__ = 1.1

HOST_DEFALUT = 'http://127.0.0.1:8000'
PYRAMID_SETTINGS = {'EASTER_HOST': HOST_DEFALUT}

try:
  from django.conf import settings
  HOST = getattr(settings, 'EASTER_HOST', HOST_DEFALUT)
except ImportError:
  settings = PYRAMID_SETTINGS
  HOST = HOST_DEFALUT

POST_URL = '%s/api/v1/event/' %HOST
QUERY_URL = POST_URL
EVENTS_URL = '%s/api/v1/user/' %HOST

def md5_sig(json_data):
  m = md5.new(json.dumps(json_data))
  sig = m.hexdigest()
  return sig

class API():
  def __init__(self):
    self.host = HOST

  def post(self, app_name, user_info, events):
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
    r = requests.post(url=POST_URL, data=json.dumps(info), headers=headers)
    return r.status_code

  def query(self, app_name, query, fields=[]):
    info = {
      'app_name': app_name,
      'query': json.dumps(query),
      'fields': json.dumps(fields)
    }
    r = requests.get(url=QUERY_URL, params=info)
    return r.content

  def events(self, uid, from_datetime, to_datetime):
    info = {
      'uid': uid,
      'from_datetime': from_datetime,
      'to_datetime': to_datetime
    }
    r = requests.get(url=EVENTS_URL, params=info)
    return r.content