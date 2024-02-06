# -*- coding: utf-8 -*-
"""
Created on Feb 6  2024

@author: Luis Cristóvão
"""

import flask as fl
from sys import argv
from datetime import datetime
import threading
import json
import time

app = fl.Flask(__name__, static_url_path='')

# Dictionary to store IP addresses and visit counts
visit_data = {}

def load_data():
    try:
        with open('visit_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data():
    while True:
        with open('visit_data.json', 'w') as f:
            json.dump(visit_data, f, indent=4)
        time.sleep(1)  # Save data every second


# Load initial data from file
visit_data = load_data()


save_thread = threading.Thread(target=save_data)
save_thread.daemon = True  # Set the thread as a daemon so it will be terminated when the main program exits
save_thread.start()




@app.route('/')
def count_visits():
    ip_address = fl.request.remote_addr
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if ip_address not in visit_data:
        visit_data[ip_address] = {'count': 1, 'time': [current_time]}
    else:
        visit_data[ip_address]['count'] += 1
        visit_data[ip_address]['time'].append(current_time)

    # print(visit_data)
    resp = fl.Response(str(visit_data[ip_address]['count']))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# @app.route('/getKey/<key>')
# def getKey(key):
	
# 	resp = fl.Response(map[key])
# 	resp.headers['Access-Control-Allow-Origin'] = '*'
# 	return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=argv[1])