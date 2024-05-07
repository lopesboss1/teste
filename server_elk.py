# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 19/11/2018
# Last update: 27/05/2019
# Description: Server to show everything to received.
#########################################################################################
import sys, requests, json, ast
from utils import print_json, save_yml
from datetime import datetime, timedelta
from flask import Flask, request, abort
#######################################################################################
app = Flask(__name__)
port = 3009
def bytesELK2json(data,codification='utf-8'):
    d_dict = {}
    #print(str(data))
    try:
       d_str = data.decode(codification)
       d_str = d_str.replace("false","False")
       d_str = d_str.replace("true","True")
       d_str = d_str.replace("null","None")
       d_dict = eval(d_str)
    except:
       print("[ERROR] type = %s ".format( type(data) ))
    finally:
       return d_dict
#######################################################################################
@app.route('/', methods=['POST'])
def webhook_elk():
    print("/ [post]]-> "+ str(sys.stdout.flush()) )
    data = request.data
    data_parse = bytesELK2json(data)
    print_json( data_parse )
    save_yml( data_parse , nameFile="alertas_elk.yml")
    return '', 200

@app.route('/hearbeat_ping_down', methods=['GET','POST'])
def solve_ping():
    print("DEF ping-----------------------")
    print( request.data )
    return '', 200



#######################################################################################
if __name__ == '__main__':
   print("[INI] server_elk.py")
   app.run(host='localhost',port=80)