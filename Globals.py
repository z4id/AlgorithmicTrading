import datetime as datetime
from collections import defaultdict
import pickle

# 1 - Stooq
# 2 - Finam.ru

# As the data is in 5 min interval, so 12 * 5 would be next hour
# rolling mean 25 minutes, as the data is in 5 minute interval
rolling_mean = 5
next_prediction = 60
lag = 12
do_prediction = True

Stocks = []
Stocks.append({'name':'Apple Inc.','symbol':'AAPL','zone':'America/New_York',
               'selection':2,'data_file':'Data/AAPL.csv',
               'source_zone':'Europe/Moscow','from_file':False,
                'from_cloud' : False,'getLive' : True,'max_from_google':False,'max_days':1})
#
# Stocks.append({'name':'Chine Mobile Ltd','symbol':'0941','zone':'Asia/Hong_Kong',
#                'selection':1,'data_file':'Data/941.csv',
#                'source_zone':'Europe/Warsaw','from_file':False,
#                 'from_cloud' :False,'getLive' : True,'max_from_google':False,'max_days':1})

# Stocks.append({'name':'Chine Mobile Ltd','symbol':'0941','zone':'Asia/Hong_Kong',
#                'selection':1,'data_file':'Data/11B.csv',
#                'source_zone':'Europe/Warsaw','from_file':True,
#                 'from_cloud' : False,'getLive' : True})


def days_between(d1, d2):
    d3 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %I:%M")
    d4 = datetime.datetime.strptime(d2, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %I:%M")
    newd3 = datetime.datetime.strptime(d3, "%Y-%m-%d %I:%M")
    newd4 = datetime.datetime.strptime(d4, "%Y-%m-%d %I:%M")
    return (newd4 - newd3).days


def minutes_between(d1, d2):
    d3 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M")
    d4 = datetime.datetime.strptime(d2, "%Y-%m-%d %H:%M")
    return abs((d4 - d3).seconds / 60)


def add_minute(d1, m):
    d2 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M")
    update = d2 + datetime.timedelta(minutes=m)
    return update.strftime("%Y-%m-%d %H:%M")