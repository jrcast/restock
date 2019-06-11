#!flask/bin/python
from collections import OrderedDict
from flask import Flask, jsonify
from flask import request as f_req
import logging
import os
import requests


class Restock():

    def __init__(self):
        self.healthy = False
        self.query_url = "https://www.alphavantage.co/query"
        self.logger = logging.getLogger("restock")
        logformat = logging.Formatter('%(levelname)-8s %(message)s')
        handler = logging.StreamHandler() #logging to stdout
        handler.setFormatter(logformat)
        self.logger.addHandler(handler)

        self.app = Flask(__name__)
        self.app.add_url_rule(rule='/', view_func=self.get_price, methods=['GET'])
        self.app.add_url_rule(rule='/healthz', view_func=self.health_check, methods=['GET'])

        self.api_key = os.environ.get("APIKEY", None)
        if "APIKEY" is None:
            self.logger.exception("APIKEY not found. Please define environ APIKEY")
            raise Exception()

        self.healthy = True

    def get_price(self):
        data = []
        avg = 0
        symbol = f_req.args.get('symbol', default=os.environ.get("SYMBOL", None), type=str)
        ndays = f_req.args.get('ndays', default=int(os.environ.get('NDAYS', 4)), type=int) #if no ndays provided default to 4 days
        qpayload = {"apikey": self.api_key, "function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": symbol}
        q = requests.get(self.query_url, params = qpayload)
        try:
            q.raise_for_status()
            q = q.json(object_pairs_hook=OrderedDict) #Maintain order of elements

            if 'Time Series (Daily)' not in q:
                self.logger.error(q)
                return jsonify({"success": False}), 500
            else:
                for day in list(q['Time Series (Daily)'].keys())[0:ndays]:
                    data.append(float(q['Time Series (Daily)'][day]['4. close']))
                    avg = sum(data) / len(data)
        except Exception as e:
            self.logger.error(e)
        return jsonify({'success': True, 'symbol': symbol.upper(), 'ndays': ndays, "data": data, "avg": avg}), 200

    def health_check(self):
        if self.healthy:
            return jsonify({"Health": "OK"}), 200
        else:
            return jsonify({"Health": "NOT_OK"}), 500


app = Restock().app
if __name__ == "__main__":
    app.run(port = 10000, debug = True) #run directly to run debug mode ON
