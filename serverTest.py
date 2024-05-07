
# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 19/11/2018
# Description: Server to show everything to received.
#########################################################################################
import sys, requests
from datetime import datetime, timedelta
from flask import Flask, request, abort
#######################################################################################
app = Flask(__name__)
#######################################################################################
@app.route('/', methods=['GET','POST'])
def webhook():
    print("DEF webhook()-> "+ str(sys.stdout.flush()) )
    #print( request.data )
    if request.method == 'GET':
        print("GET->")
        print(request.data)
        return '', 200
    if request.method == 'POST':
        print("POST->")
        print(request.data)
        #print(request.json)
        return '', 200
    else:
        abort(400)
#######################################################################################
if __name__ == '__main__':
    app.run(host="172.30.0.35",port=8080)
