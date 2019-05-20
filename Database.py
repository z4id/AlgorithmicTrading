from pymongo import MongoClient
import numpy as np
import threading
import datetime
import copy
from datetime import date
from Security import Security
import pandas as pd
import Globals as gb
import json
from Predition import Prediction


class Database:
    def __init__(self):
        try:
            client = MongoClient('localhost:27017')
            self.db = client.stockstalker
            print 'Database Connection Opened successfully.'
        except:
            print 'Failed to open connection to database'
            return
        
        self.stocks = self.db.FiveMinuteStocks
        self.predictions = self.db.Predictions
        return None
    
    def insert_all(self, records):
        for x in records:
            self.fill_change(x)
    
    def remove_all_records(self, stock):
        self.stocks.remove({'symbol': stock.symbol})
        if gb.do_prediction:
            self.predictions.remove({'symbol': stock.symbol})
    
    def get_last_record(self, symbol):
        
        last = self.stocks.find({'symbol': symbol}).sort('date', -1).limit(1)
        if last.count() > 0:
            last = last[0]
            last.pop('_id', None)
            Security_record = Security()
            Security_record.to_class(**last)
            return Security_record
        print "No Record found for : ", symbol
        return
    
    def get_lastn_records(self, symbol, n):
        
        data = self.stocks.find({'symbol': symbol}).sort('date', -1).limit(n)
        data2 = self.predictions.find({'symbol': symbol}).sort('cdate', -1).limit(2*n)
        records = []

        for last in data:
            last.pop('_id', None)
            records.append(last)
        
        predictions = []
        for last in data2:
            last.pop('_id', None)
            predictions.append(last)

        # print "No Record found for : ", symbol
        # print records
        return records,predictions

    def get_lastn_pred_records(self, symbol, n):
    
        data2 = self.predictions.find({'symbol': symbol}).sort('cdate', -1).limit(2 * n)
        
        predictions = []
        for last in data2:
            last.pop('_id', None)
            predictions.append(last)

        return predictions
    
    def fill_change(self,security):
    

        self.stocks.insert(security.__dict__)
        last_records = self.stocks.find({'symbol':security.symbol}).sort('date',-1).limit(gb.lag+1)
        changed = ''
        if last_records.count(with_limit_and_skip=True) == gb.lag+1:
            df = pd.DataFrame(list(last_records)[::-1])
            id = df.iloc[-1]['_id']
            del df['_id']
            df['close'] = df['close'].astype(float)
            df['m5_change'] = df['close'].pct_change()
            df['m10_change'] = df['close'].pct_change(periods=2)
            df['m15_change'] = df['close'].pct_change(periods=3)
            df['m20_change'] = df['close'].pct_change(periods=4)
            df['m60_change'] = df['close'].pct_change(periods=12)
            df['rolling_mean'] = df['m5_change'].rolling(window=gb.rolling_mean).mean()

            df = df.fillna(0)
            df['m5_change'] = df['m5_change'].astype(str)
            df['m10_change'] = df['m10_change'].astype(str)
            df['m15_change'] = df['m15_change'].astype(str)
            df['m20_change'] = df['m20_change'].astype(str)
            df['m60_change'] = df['m60_change'].astype(str)
            df['rolling_mean'] = df['rolling_mean'].astype(str)
            mydict = df.T.to_dict()[len(df)-1]
            self.stocks.update({'_id':id}, {'$set': mydict})

            if gb.do_prediction:
                security = Security()
                security.to_class(**mydict)
                new_prediction = Prediction(security)
                new_prediction.update_prediction(self.predictions)
            
        
    def insert_records(self, security_array):
        for sa in security_array:
            self.fill_change(sa)
            
            
    def fill_all_changes(self,precords):
        
        records = [ x.__dict__ for x in precords]
        df = pd.DataFrame(records)
        # print df
        
        df['m5_change'] = df['close'].astype(float).pct_change()
        df['m10_change'] = df['close'].astype(float).pct_change(periods=2)
        df['m15_change'] = df['close'].astype(float).pct_change(periods=3)
        df['m20_change'] = df['close'].astype(float).pct_change(periods=4)
        df['m60_change'] = df['close'].astype(float).pct_change(periods=12)
        df['rolling_mean'] = df['m5_change'].rolling(window=gb.rolling_mean).mean().astype(float)
        df = df.fillna(0)
        df['m5_change'] = df['m5_change'].astype(str)
        df['m10_change'] = df['m10_change'].astype(str)
        df['m15_change'] = df['m15_change'].astype(str)
        df['m20_change'] = df['m20_change'].astype(str)
        df['m60_change'] = df['m60_change'].astype(str)
        df['rolling_mean'] = df['rolling_mean'].astype(str)

        mydict = df.T.to_dict()
        df_len = len(mydict)
        mypredictions = [0]*df_len
        
        if gb.do_prediction:
            for i in range(0,df_len):
                security = Security()
                security.to_class(**mydict[i])
                new_prediction = Prediction(security)
                
                # if new_prediction.is_present(new_prediction,self.predictions):
                #     continue
                    
                if i >= gb.lag:
                    
                    mypredictions[i-gb.lag].next_closing = float(new_prediction.current_closing)
                    
                    if float(new_prediction.current_closing) >= float(mypredictions[i-gb.lag].current_closing):
                        mypredictions[i-gb.lag].actual_movement = 1
                    else:
                        mypredictions[i - gb.lag].actual_movement = 0
                
                mypredictions[i] = new_prediction
                
                if np.mod(i, 500) == 0:
                    print i
        
        for d in range(0,df_len):
            self.stocks.insert(mydict[d])
            if gb.do_prediction:
                print "Inserting Predictions"
                self.predictions.insert(mypredictions[d].__dict__)
            
            
    def update_security(self, current, updated):
        
        self.stocks.update(current.__dict__, {'$set': updated.__dict__})
        # print "Previous Record Updated ! "
    
    def is_present(self, stock):
        
        record = self.stocks.find({'symbol': stock.symbol, 'date': stock.date})
        if record.count(with_limit_and_skip=True) > 0:
            # print "Previously Found Similar Record, Updated !"
            # self.stocks.update({'_id': record[0].pop('_id')}, {'$set': stock.__dict__})
            # last_pred = Prediction(stock)
            # last_pred.update_prediction(self.predictions)
            print "Found Previously : ",stock.date
            return True
        
        return False
    
    def proper_insert(self, stock):
        
        missing = []
        last_record = self.get_last_record(stock.symbol)
        current_record = stock
        
        if self.is_present(stock):
            return True

        print "Found New Record : ", stock.name
        
        if last_record and current_record:
            
            if current_record.date == last_record.date:
                self.update_security(last_record, current_record)
            
            if gb.days_between(last_record.date, current_record.date) < 1:
                
                diff = gb.minutes_between(last_record.date, current_record.date)
                # print diff
                if diff > 5:
                    for i in range(5, diff, 5):
                        newdate = gb.add_minute(str(last_record.date), i)
                        new_record = copy.deepcopy(last_record)
                        new_record.date = newdate
                        new_record.volume = 0
                        # self.stocks.insert(copy.deepcopy(new_record.__dict__))
                        missing.append(new_record)
            
            missing.append(current_record)
            self.insert_records(missing)
            
            # self.stocks.insert(copy.deepcopy(current_record.__dict__))
        
        else:
            print "Entering Initial Record for : ", stock.symbol
            self.insert_records([stock])
    
    def proper_insert_all(self, stocks):
    
        missing = []
        for s in range(0, len(stocks)):
            
            if s  < 1:
                missing.append(stocks[s])
                continue
            
            stock = stocks[s]
            last_record = stocks[s-1]
            current_record = stock
                # self.get_last_record(stock.symbol)
            
    
            if self.is_present(stock):
                continue
            #
            # print "Entering New Records"
            if last_record and current_record:
        
                if current_record.date == last_record.date:
                    self.update_security(last_record, current_record)
        
                if gb.days_between(last_record.date, current_record.date) < 1:
            
                    diff = gb.minutes_between(last_record.date, current_record.date)
                    # print diff
                    if diff > 5:
                        for i in range(5, diff, 5):
                            newdate = gb.add_minute(str(last_record.date), i)
                            new_record = copy.deepcopy(last_record)
                            new_record.date = newdate
                            new_record.volume = 0
                            # self.stocks.insert(copy.deepcopy(new_record.__dict__))
                            missing.extend([new_record])
        
                missing.extend([current_record])
        # self.insert_records(missing)
        print "Missing dates filled for  :",stocks[0].symbol
        self.fill_all_changes(missing)