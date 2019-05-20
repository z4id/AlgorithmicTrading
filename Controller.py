from app import app
from flask import render_template, jsonify, redirect, request, url_for
from Database import Database
from Security import Security
import json, ast
import Globals as gb

db = Database()
Stocks = []

@app.route('/')
@app.route('/index')
def index():

    # print globals.stocks
    # news = Scrap().getNews()
    return render_template("/index.html", stocks=gb.Stocks, Records = [])

@app.route("/getStocksList",methods=['POST'])
def getStocksList():
    try:
        return jsonify(stocksList='stockList')

    except Exception,e:
        return jsonify(message='Failed')

@app.route('/stream_stock', methods=['POST'])
def stream_stock():
    
    global db
    global Stocks
    Stocks,predictions = db.get_lastn_records(request.form['selected'], 12)
    values = json.dumps(Stocks)
    predic = json.dumps(predictions)
    return render_template('streamLive.html',initialValues = json.loads(values), predictions = json.loads(predic))


@app.route('/getLatest', methods=['GET', 'POST'])
def getLatest():
    global db
    global Stocks
    Stock = db.get_last_record(request.args.get('symbol'))
    ldate = request.args.get('ldate')
    Stock = Stock.__dict__
    values = json.dumps([Stock])
    print "In Get Latest"
    if Stock["date"] == ldate:
        print Stock["date"],ldate
        return jsonify('')

    predic = json.dumps(db.get_lastn_pred_records(request.args.get('symbol'),12))

    return jsonify(actual=values,predicted=predic)


@app.route('/StreamLive', methods=['GET', 'POST'])
def StreamLive2():
    return render_template('streamLive.html',symbol='AAPL')


@app.route('/home', methods=['GET', 'POST'])
def home():
    global stocks
    return render_template("index.html", stocks=stocks)


@app.route('/historical_data', methods=['GET', 'POST'])
def historical_data():
    return render_template("historical_data.html")


@app.route('/finance_news', methods=['GET', 'POST'])
def finance_news():
    return render_template("finance_news.html")


@app.route('/twitter_feeds', methods=['GET', 'POST'])
def twitter_feeds():
    return render_template("twitter_feeds.html")


@app.route('/working', methods=['GET', 'POST'])
def working():
    return render_template("working.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")


# @app.route("/streamLive",methods=['POST'])
# def streamLive():
#    try:
#        obj = { 'Microsoft': globals.stockArray[0].currentP, 'Apple': globals.stockArray[1].currentP, 'Google': globals.stockArray[2].currentP, 'Facebook': globals.stockArray[3].currentP}
#        #print obj
#        return jsonify(obj)
#
#    except Exception,e:
#        print "In exception of streamLive ", e
#        print e.message
#        return jsonify(message='Failed')


# @app.route("/getChosenStockValues",methods=['POST'])
# def getChosenStockValues():
#    try:
#        for singlestock in globals.stockArray:
#            if globals.currentStock == singlestock.name:
#                return jsonify(title = globals.currentStock, currentP = singlestock.currentP)
#        return jsonify(title = ":-: StockStalker :-:",currentP="couldn't set it")
#
#    except Exception,e:
#        print "In exception of getChosenStockValues ", e
#        print e.message
#        return jsonify(message='Failed')


# @app.route("/updateOCHLV",methods=['POST'])
# def updateOCHLV():
#    try:
#        #print ":):):):):):):) ",_security.date, ",", _security.open, ",", _security.close, ",", _security.high, ",", _security.low, ",", _security.volume
#        if _security.date:
#                return jsonify(openP=_security.open, closeP=_security.close, highP=_security.high, lowP=_security.low, volume=_security.volume)
#        return jsonify(title = ":-: StockStalker :-:",currentP="couldn't set it")
#
#    except Exception,e:
#        print "In exception of updateOCHLV ", e
#        print e.message
#        return jsonify(message='Failed')
#
#
# @app.route("/getChartRecords",methods=['POST'])
# def getChartRecords():
#    try:
#        print "In Get Chart Records()...................."
#        #print "++++++++++++ ", liveData
#        #print "------------ ", predictedData
#        return jsonify(chartrecords = liveData, predictedValues = predictedData)
#
#    except Exception,e:
#        print "In exception of getChartRecords", e
#        print e.message
#        return jsonify(message='Failed')