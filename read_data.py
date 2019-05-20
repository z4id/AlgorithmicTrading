import pandas as pd



# def changeTimeZone(filename, targetZone, sourceZone='Europe/Warsaw'):
#     f = open(filename)
#     records = f.readlines()
#     records = records[1:len(records)]
#     li = list()
#     for line in records:
#         values = line.split(",")
#         date = values[0]
#         time = values[1]
#         high = values[3]
#         low = values[4]
#         close = values[5]
#
#         dt = pytz.timezone(sourceZone).localize(datetime.strptime(date + " " + time, '%Y-%m-%d %H:%M:%S')).astimezone(pytz.timezone(targetZone))
#         li.append((dt.replace(tzinfo=None), high, low, close))
#
#     return li
#
# records = changeTimeZone('941.hk.txt', 'Asia/Hong_Kong', sourceZone='Europe/Warsaw')
# for record in records:
#     print record[0]

data = pd.read_csv("Data/AAPL.csv",header=None)

for d in range(0,len(data)):
    
    datetime = data.iloc[d,0]+" "+data.iloc[d,1]
    print datetime