# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 01/14/2019
# Last Update: 25/10/2019
# Description: Server to show everything to received.
# https://blog.nearsoftjobs.com/crear-un-api-y-una-aplicación-web-con-flask-6a76b8bf5383
#########################################################################################
import sys, requests, json, ast
from utils import print_json
from datetime import datetime, timedelta
from flask import Flask, request, abort
#######################################################################################
URL_NGROK = "http://0c554f14.ngrok.io"
SERVER_PORT = 3002 #3009
SERVER_HOST = 'localhost' #'172.30.0.114'
app = Flask(__name__)
#######################################################################################
def print_everything(request):
    print("{0} [INFO ] print_everything | - - - len:{1} - - - |".format( datetime.utcnow().isoformat, len(request)))
    print("{0} [INFO ] print_everything | - - - HEADER  - - - |".format( datetime.utcnow().isoformat()))
    print_json(dict( request.headers ) )
    print("{0} [INFO ] print_everything | - - - FORM  - - - |".format( datetime.utcnow().isoformat()))
    print_json(dict( request.form ) )
    print("{0} [INFO ] print_everything | - - - ARGS  - - - |".format( datetime.utcnow().isoformat()))
    print_json(dict( request.args ) )
    
    return request
#######################################################################################
def print_parameters(request):
    rpt = None
    print("[INFO ] print_parameters | len = {0}".format(request))
    #try:
    multi_dict = request.args
    for key in multi_dict:
        print ("KEY\t:{0}".format( multi_dict.get(key) ))
        print ( multi_dict.getlist(key) )
    print("[INFO ] printing  form data: ")
    data_form = request.form
    print("[INFO ] printing headers: ")
    print_json( dict(request.headers) )
    print("[INFO ] printing form: ")
    print_json( dict(request.form) )
    print("[INFO ] printing args: ")
    print_json( dict(request.args) )
    print("[INFO ] printing content: ")
    print_json( request.json )
    #for key in data_form:/    print ( "{0}\t: {1}".format( key, data_form[key]  ))
    return rpt
#######################################################################################
def req_get(URL_API, data=None, timeout=None):
    try:
        headers =  {'Content-Type': 'application/json'}
        rpt = requests.get( url=URL_API, data=data, headers=headers, timeout=timeout)
        print("{0} [INFO ] req_get |{1}|{2}|{3}|".format( datetime.utcnow().isoformat(), rpt.status_code, rpt.reason, URL_API))
        print(rpt.text)
        return rpt.text
    except:
        print("{0} [ERROR] req_get |{1}|{2}|".format( datetime.utcnow().isoformat(), URL_API))
        return ""
#######################################################################################
def req_post(URL_API, data=None, timeout=None):
    try:
        headers =  {'Content-Type': 'application/json'}
        rpt = requests.post( url=URL_API, data=data, headers=headers , timeout=timeout)
        print("{0} [INFO ] req_post|{1}|{2}|{3}|".format( datetime.utcnow().isoformat(), rpt.status_code, rpt.reason, URL_API))
        print(rpt.text)
        return rpt.text
    except:
        print("{0} [ERROR] req_post|{1}|{2}|".format( datetime.utcnow().isoformat(), URL_API))
        return ""
#######################################################################################
def bytesELK2json(data_org,codification='utf-8'):
    d_dict = {}
    if (type(data_org)==bytes):
        print("[INFO] bytesELK2json | decoding <{0}:{1}>".format(len(data_org),codification))
        data_str = data_org.decode(codification)

    try:
       data_str = data_org.replace("false","False")
       data_str = data_org.replace("true","True")
       data_str = data_org.replace("null", "None")
       d_dict = eval(data_str)
    except:
       print("[ERROR] type={0} ".format( type(data_org) ))
       print(data_org)
    finally:
       return d_dict
#######################################################################################
#@app.route('/incidencias_elk', methods=['POST'])
@app.route('/bypass', methods=['POST'])
def webhook_elk():
    print("[alert_elk] webhook_post()-> "+ str(sys.stdout.flush()) )
    data_json = request.json
    url_bypass = data_json['metadata']['bypass']['url']
    rpt = req_post(url_bypass, data = data_json, timeout=None)
    #print_everything(data_json)
    return '', 200
#######################################################################################
@app.route('/webhook_whassapp', methods=['POST'])
def webhook_whassapp():
    #URL = "http://1855b969.ngrok.io"
    print("[alert_elk] webhook_post()-> "+ str(sys.stdout.flush()) )
    #print_json( bytesELK2json( request.data ))
    rpt = req_post(URL_NGROK, data = request.data, timeout=None)
    return '', 200
#######################################################################################
@app.route('/twilio_comes_in', methods=['POST'])
def webhook_twilio_comes_in():
    #URL = "http://1855b969.ngrok.io"
    print("[alert_elk] twilio_comes_in()-> "+ str(sys.stdout.flush()) )
    #print_json( bytesELK2json( request.data ))
    print_parameters(request)
    rpt = req_post(URL_NGROK, data = request.data, timeout=None)
    return '', 200
#######################################################################################
@app.route('/twilio_callback_url', methods=['POST'])
def webhook_twilio_callback_url():
    print("[alert_elk] twilio_callback_url()-> "+ str(sys.stdout.flush()) )
    #print_json( bytesELK2json( request.data ))
    print_json(request.json)
    print_parameters(request)
    rpt = req_post(URL_NGROK, data = request.data, timeout=None)
    return '', 200
#######################################################################################
@app.route('/get_aws', methods=['GET'])
def webhook_get():
    print("webhook_get()-> "+ str(sys.stdout.flush()) )
    print_json( bytesELK2json( request.data ))
    #rpt = req_get(URL_NGROK, data = request.data, timeout=None)
    return '', 200
#######################################################################################
@app.route('/hearbeat_ping_down', methods=['GET','POST'])
def solve_ping():
    print("DEF ping-----------------------")
    print( request.data )
    return '', 200
#######################################################################################
if __name__ == '__main__':
    app.run(host=SERVER_HOST,port=SERVER_PORT)
