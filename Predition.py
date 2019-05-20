import Globals as gb
from Security import Security
import numpy as np
from collections import defaultdict
import pickle

# load_prediction models
RF_Models = defaultdict(str)

if gb.do_prediction:
    for s in gb.Stocks:
        RF_Models[s['symbol']] = pickle.load(open("Models/RF_"+s['symbol'] + ".pickle", 'rb'))

class Prediction:
    
    def __init__(self,stock):
        
        self.symbol = stock.symbol
        self.cdate = stock.date
        self.ndate = gb.add_minute(str(stock.date),gb.next_prediction)
        self.current_closing = stock.close
        self.predicted_movement = self.predict(stock)
        self.next_closing = ''
        self.actual_movement = ''
        self.profit = ''
        
        
    def predict(self,stock):
    
        global RF_Models
        loaded_model = RF_Models[self.symbol]
        X =  np.array([float(stock.m5_change),float(stock.m10_change),float(stock.m15_change),float(stock.m20_change),float(stock.m60_change),float(stock.rolling_mean)]).reshape(1,-1)
        result = loaded_model.predict(X)
        return int(result)
    
    def update_prediction(self,db):
        
        if self.is_present(self,db):
            return
        
        db.insert(self.__dict__)
        previous_update = db.find({'symbol': self.symbol, 'ndate': self.cdate}).sort('ndate',-1)
        if previous_update.count(with_limit_and_skip=True) > 0:
            previous = previous_update[0]
            id = previous.pop('_id')

            previous["next_closing"] = float(self.current_closing)
            if float(self.current_closing) >= float(previous["current_closing"]):
                previous['actual_movement'] = 1
            else:
                previous['actual_movement'] = 0
    
            db.update({'_id': id}, {'$set': previous})
        
    def to_class(self, **entries):
        self.__dict__.update(entries)

    def is_present(self, stock,db):
        
        record = db.find({'symbol': stock.symbol, 'cdate': stock.cdate})
        if record.count(with_limit_and_skip=True) > 0:
            db.update({'_id': record[0].pop('_id')}, {'$set': stock.__dict__})
            return True
    
        return False