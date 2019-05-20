from pymongo import MongoClient
import pandas as pd
import Globals as gb
import Algorithms as algo

class Learning:
    
    def __init__(self,symbol):
        
        client = MongoClient('localhost:27017')
        db = client.stockstalker.FiveMinuteStocks
        self.symbol = symbol
        stocks = db.find({'symbol':symbol}).sort('date',1)
        self.df0 =  pd.DataFrame(list(stocks))
        
    def make_model(self):
    
    
        df = self.df0[["m5_change", "m10_change", "m15_change", "m20_change", "m60_change", "rolling_mean"]].astype(float)
        df['prediction'] = df['m60_change'].shift(-1)
    
        df = df.fillna(0)
        df.loc[df.prediction >= 0, 'prediction'] = 1
        df.loc[df.prediction < 0, 'prediction'] = 0
        df_len  = len(df)
        end = int(0.7 * df_len)
    
        features = df.columns[:-1]
        x = df[features]
        y = df.prediction
    
        x_train = x[:end]
        y_train = y[:end]
    
        x_test = x[end:]
        y_test = y[end:]
    
        algo.performRFClass(x_train, y_train, x_test, y_test, self.symbol, True)
        # performAdaBoostClass(x_train,y_train,x_test,y_test)
        # performGTBClass(x_train,y_train,x_test,y_test)
        

model = Learning('0941')
model.make_model()
model = Learning('AAPL')
model.make_model()