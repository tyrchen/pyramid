# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from datetime import datetime as py_time
from datetime import timedelta
from pyramid import API

import datetime
import time
import random

api = API()

app_name = 'cayman'
collection_name = 'create_clip'
db_info = {
  'app_name': app_name,
}

anonymous_simida = {'uid': '', 'cookie': 'kimgee'}
simida = {'uid': 'simida', 'cookie': 'kimgee'}
user_list = ['chiyuan', 'tchen', 'wxttt', 'simida', 'brain', 'du', 'hugh']

clip_list = ['tukeq', 'mafengwo', 'qiongyou', 'guluyu', 'ziyou', 'sina']
board_list = ['black', 'white', 'green', 'yellow', 'red', 'blue']

delta_day = datetime.timedelta(days=1)
delta_hour = datetime.timedelta(hours=1)

now = datetime.datetime.now()
yesterday = now - delta_day
two_days_ago = now - delta_day*2
three_days_ago = now - delta_day*3
tomorrow = now + delta_day
two_days_later = now + delta_day*2
half_a_day_before = now - delta_hour*12

def random_user():
  uid = random.choice(user_list)
  cookie = '%s_cookie' %uid
  return {
    'uid': uid,
    'cookie': cookie
  }

def random_choice(list):
  return random.choice(list)

def random_hour():
  return int(random.uniform(0, 24))

def random_day():
  return random.choice(range(6))

def random_datetime():
  now = py_time.now()
  delta = random_day()
  date = now - timedelta(days=delta)
  return py_time(year=date.year, month=date.month,
                 day=date.day, hour=random_hour()).strftime('%Y-%m-%d %H:%M:%S')

def random_event():
  clip = random_choice(clip_list)
  board = random_choice(board_list)
  user_info = random_user()
  uid = user_info['uid']
  text = '%s在%s上创建了%s' %(uid, board, clip)

  return user_info, {
    'collection_name': collection_name,
    'clip': clip,
    'board': board,
    'origin': random.choice(['1', '2']),
    'datetime': random_datetime(),
    'text': text,
  }

def base_test():
  user_info, event = random_event()
  api.post(app_name, user_info, [event])

def query_test():
  from_date = two_days_ago
  to_date = two_days_later  
  query = {
    'collection_name': collection_name,
    'from_datetime': from_date.strftime('%Y-%m-%d %H:%M:%S'),
    'to_datetime': to_date.strftime('%Y-%m-%d %H:%M:%S'),
  }
  fields = [{'uid': 'chiyuan', 'board': 'blue'},]
  content = api.query(app_name, query, fields)
  print(content)

def events_test():
  from_date = yesterday.strftime('%Y-%m-%d %H:%M:%S')
  to_date = now.strftime('%Y-%m-%d %H:%M:%S')
  uid = 'simida'
  content = api.events(uid, from_date, to_date)
  print(content)
