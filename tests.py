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
collection_name = 'event'
db_info = {
  'app_name': app_name,
}

anonymous_simida = {'uid': '', 'cookie': 'kimgee'}
simida = {'uid': 'simida', 'cookie': 'kimgee'}

event1 = {'collection_name': collection_name, 'clip': 'clip1', 'board': 'board1', 'origin': '1',
          'text': 'I love zixiao', 'datetime': py_time.now().strftime('%Y-%m-%d %H:%M:%S')}

time.sleep(0.1)

event2 = {'collection_name': collection_name, 'clip': 'clip2', 'board': 'board2', 'origin': '2',
          'text': 'Zixiao, do you love me?', 'datetime': py_time.now().strftime('%Y-%m-%d %H:%M:%S')}

time.sleep(0.1)

event3 = {'collection_name': collection_name, 'clip': 'clip3', 'board': 'board3', 'origin': '2',
          'text': 'Zixiao, We are in love'}

delta_day = datetime.timedelta(days=1)
delta_hour = datetime.timedelta(hours=1)

now = datetime.datetime.now()
yesterday = now - delta_day
two_days_ago = now - delta_day*2
three_days_ago = now - delta_day*3
tomorrow = now + delta_day
two_days_later = now + delta_day*2
half_a_day_before = now - delta_hour*12

def random_hour():
  return int(random.uniform(0, 24))

def random_day():
  return random.choice(range(6))

def random_datetime():
  now = py_time.now()
  delta = random_day()
  date = now - timedelta(days=delta)
  return py_time(year=date.year, month=date.month, day=date.day, hour=random_hour())

def random_event():
  return {
    'collection_name': collection_name,
    'clip': random.choice(['clip1', 'clip2', 'clip3']),
    'board': random.choice(['board1', 'board2', 'board3']),
    'origin': random.choice(['1', '2']),
    'datetime':two_days_later.strftime('%Y-%m-%d %H:%M:%S'),
    'text': str(int(random.random()*10000)),
  }

def base_test():
  api.post(app_name, simida, [random_event()])

def query_test():
  from_date = yesterday
  to_date = now
  query = {
    'collection_name': collection_name,
    'from_datetime': from_date.strftime('%Y-%m-%d %H:%M:%S'),
    'to_datetime': to_date.strftime('%Y-%m-%d %H:%M:%S'),
  }
  fields = [{'board': 'board1', 'clip': 'clip2'},]
  content = api.query(app_name, query, fields)
  print(content)

def events_test():
  from_date = yesterday.strftime('%Y-%m-%d %H:%M:%S')
  to_date = now.strftime('%Y-%m-%d %H:%M:%S')
  uid = 'simida'
  content = api.events(uid, from_date, to_date)
  print(content)
