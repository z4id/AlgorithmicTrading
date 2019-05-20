from Security import Security
from Database import Database
from Scrap import Scrap
import threading
import time
import pytz
import datetime as datetime2
import re
import Globals as gb



globaldb = Database()
        
class ScrapThread(threading.Thread):
    def __init__(self, stock):
        threading.Thread.__init__(self)
        self.stock = stock
        global globaldb
        self.db = globaldb
        self.data_file = ''
        self.selection = 0
        self.source_zone = ''
        self.from_file = False
        self.from_cloud = False
        self.getLive = False
        self.max_from_google = False
        self.max_days = 1

    def parse_date(dtime, targetZone, sourceZone):
        dtime = pytz.timezone(sourceZone).localize(
            datetime2.datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')).astimezone(
            pytz.timezone(targetZone))
        dtime = dtime.replace(tzinfo=None)
        dtime = dtime.strftime('%Y-%m-%d %H:%M')
        return dtime

    def fill_data_file(self,filename, targetZone, sourceZone='Europe/Warsaw', selection=1):
        f = open(filename)
        records = f.readlines()
        records = records[1:len(records)]
        li = list()
        for line in records:
            values = line.split(",")
            new = Security()
            new.name = self.stock.name
            new.symbol = self.stock.symbol
            new.zone = self.stock.zone
            date = values[0]
            time = values[1]
            
            new.open = float(values[2])
            new.high = float(values[3])
            new.low = float(values[4])
            new.close = float(values[5])
            volume = re.findall("\d+",values[6])
            new.volume = volume[0]
            
            if selection == 1:
                dt = pytz.timezone(sourceZone).localize(
                    datetime2.datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')).astimezone(pytz.timezone(targetZone))
            elif selection == 2:
                dt = pytz.timezone(sourceZone).localize(
                    datetime2.datetime.strptime(date + " " + time, '%d/%m/%y %H:%M')).astimezone(pytz.timezone(targetZone))
        
            dt = dt.replace(tzinfo=None)
            dt = dt.strftime('%Y-%m-%d %H:%M')
            new.date = dt
            li.append(new)
    
        return li
    
    def fill_from_cloud(self):
        
        print "Inserting Complete Data of ", self.stock.symbol
        cloud = Scrap()
        records = cloud.get_complete_data(self.stock)
        # self.db.remove_all_records(self.stock)
        self.db.proper_insert_all(records)
        # for record in records:
        #     self.db.proper_insert(record)
        print "All Data Inserted for ", self.stock.symbol
        print "-----------------------"
    
    def fill_from_file(self):
        
        print "From File Inserting Complete Data of ", self.stock.symbol
        self.db.remove_all_records(self.stock)
        records = self.fill_data_file(self.data_file, self.stock.zone, self.source_zone, selection=self.selection)
        self.db.proper_insert_all(records)
        # for record in records:
        #     self.db.proper_insert(record)
        print "All Data Inserted for ", self.stock.symbol
        print "---------------------------------"

    def get_new(self):
        
        latest = Scrap()
        print "In Live Data of : ",self.stock.name
        while (True):
            data = latest.get_latest(self.stock)
            for d in data:
                self.db.proper_insert(d)
            time.sleep(50)
            
    def get_max_from_google(self):
        
        max = Scrap()
        print "Getting N days Records from Google for  :", self.max_days, self.stock.name
        data = max.get_from_google(self.stock,300,self.max_days,False)
        if self.max_days > 10:
            self.db.remove_all_records(self.stock)
        if len(data) > 0:
            self.db.proper_insert_all(data)

        
    def get_live_from_google(self):
        
        latest = Scrap()
        print "Getting Live Data from Google (Infinte Loop) : ",self.stock.name
        while (True):
            data = latest.get_from_google(self.stock, 300, 1,True)
            for d in data:
                self.db.proper_insert(d)
            time.sleep(30)
    
    def run(self):
        print "New Thread Started for ", self.stock.symbol
        
        if self.from_file:
            self.fill_from_file()
        
        if self.from_cloud:
            self.fill_from_cloud()
            
        if self.max_from_google:
            self.get_max_from_google()
        
        if self.getLive:
            self.get_live_from_google()
            




for s in gb.Stocks:
    
    stock = Security()
    stock.symbol = s['symbol']
    stock.name = s['name']
    stock.zone = s['zone']
    stockthread = ScrapThread(stock)
    stockthread.selection = s['selection']
    stockthread.data_file = s['data_file']
    stockthread.source_zone = s['source_zone']
    stockthread.getLive = s['getLive']
    stockthread.from_file = s['from_file']
    stockthread.from_cloud = s['from_cloud']
    stockthread.max_from_google = s['max_from_google']
    stockthread.max_days = s['max_days']
    stockthread.start()