import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import copy
import datetime as dt
import pytz

class Scrap:
    def __init__(self):
        site = "http://176.31.115.28/~feedscom"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        self.main_site = site
    
    def get_complete_data(self, stock):
        data = urllib2.urlopen(self.main_site + "/university/five_minute_data/Data/" + stock.symbol + ".csv").read()
        data = data.split("\n")
        current_date = ''
        array_len = data.__len__()
        Records = []
        for i in range(0, array_len):
            values = data[i].split(",")
            if values.__len__() < 6:
                continue
            if values[0] == " " or values[1] == " " or values[2] == " " or values[3] == " " or values[4] == " " or \
                            values[5] == " ":
                continue
            if i + 1 < array_len:
                if values[0] == data[i + 1].split(",")[0]:
                    continue
            
            security_record = copy.deepcopy(stock)
            security_record.date = values[0]
            
            if security_record.date == current_date:
                continue
            
            current_date = security_record.date
            security_record.symbol = stock.symbol
            security_record.name = stock.name
            security_record.open = values[1]
            security_record.close = values[2]
            security_record.high = values[3]
            security_record.low = values[4]
            security_record.volume = values[5]
            Records.append(security_record)
        
        # print Records)
        return Records
    
    def get_latest(self, stock):
        data = urllib2.urlopen(self.main_site + "/university/five_minute_data/Check/" + stock.symbol + ".txt").read()
        data = data.split("\n")[0:-1]  # then split it into lines
        latest = []
        for line in data:
            values = line.split(", ")
            
            security_record = copy.deepcopy(stock)
            security_record.symbol = stock.symbol
            security_record.name = stock.name
            security_record.date = values[0]
            security_record.open = values[1]
            security_record.close = values[2]
            security_record.high = values[3]
            security_record.low = values[4]
            security_record.volume = values[5]
            latest.append(security_record)
        
        return latest

    def get_from_google(self,stock, period, window,islast=True):
        url_root = 'http://www.google.com/finance/getprices?i='
        url_root += str(period) + '&p=' + str(window)
        url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + stock.symbol
        response = urllib2.urlopen(url_root)
        data = response.read().split('\n')
        # actual data starts at index = 7
        # first line contains full timestamp,
        # every other line is offset of period from timestamp
        parsed_data = []
        anchor_stamp = ''
        end = len(data)
        for i in range(7, end):
            cdata = data[i].split(',')
            if 'a' in cdata[0]:
                # first one record anchor timestamp
                anchor_stamp = cdata[0].replace('a', '')
                cts = int(anchor_stamp)
            else:
                try:
                    coffset = int(cdata[0])
                    cts = int(anchor_stamp) + (coffset * period)
                    parsed_data.append((dt.datetime.fromtimestamp(float(cts)), float(cdata[1]), float(cdata[2]),
                                        float(cdata[3]), float(cdata[4]), float(cdata[5])))
                except:
                    pass  # for time zone offsets thrown into data
                
        try:
            dataframe = pd.DataFrame(parsed_data)
            dataframe.columns = ['ts', 'Open', 'High', 'Low', 'Close', 'Volume']
            df_len = len(dataframe)
            
        except:
            return []

        if not islast:
            data = [0]*df_len
        
        for x in range(0,df_len):
     
            security_record = copy.deepcopy(stock)
 
            if islast:
                x = -1
     
            last = dataframe.iloc[[x]]
            date = pd.to_datetime(str(last['ts'].values[0]))
            date = dt.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')

            security_record.date = self.parse_date(date, stock.zone,'Asia/Karachi')
            security_record.open = last['Open'].values[0]
            security_record.close = last['Close'].values[0]
            security_record.high = last['High'].values[0]
            security_record.low = last['Low'].values[0]
            security_record.volume = int(last['Volume'].values[0])
            
            if islast:
                return [security_record]
            
            data[x] = security_record
        
        return data
    

    def parse_date(self,ptime, targetZone, sourceZone):
        ptime = pytz.timezone(sourceZone).localize(
            dt.datetime.strptime(ptime, '%Y-%m-%d %H:%M:%S')).astimezone(
            pytz.timezone(targetZone))
        ptime = ptime.replace(tzinfo=None)
        ptime = ptime.strftime('%Y-%m-%d %H:%M')
        return ptime
    
    def getNews(self):
        CityFalcon = self.main_site + "/todo/cityfalcon/News.csv"
        
        request1 = urllib2.Request(CityFalcon, headers=self.header)
        Parsed = BeautifulSoup(urllib2.urlopen(request1).read(), "lxml")
        currentP = Parsed.find_all("p")
        Records = currentP[0].contents[0].splitlines()
        
        MyRecords = []
        i = len(Records) - 6
        while (i < len(Records) - 1):
            Record = Records[i].split(" , ")
            single = {'link': Record[0], 'title': Record[1], 'description': Record[2], 'image': Record[3]}
            MyRecords.append(single)
            i += 1
        
        return MyRecords
