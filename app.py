# ----------------------------- Initialization ------------------------------ #
from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from flask import redirect

import os
import json
import urllib.request
import pandas as pd
import numpy as np
import json as json
from spleeter.separator import Separator

# initialize Flask app
app = Flask(__name__)
app.config['DEBUG'] = True

# ---------------------------- GLOBAL VARIABLES ----------------------------- #
root_folder = os.path.dirname(os.path.realpath('__file__'))
hostname = 'localhost'
domain = ''
port = ':5000'
settings_file = 'settings.json'

# -------------------------------- Templates -------------------------------- #
@app.route('/')
def home():
    return render_template('home.html')


# ------------------------------ Backend Requests --------------------------- #

@app.route('/split', methods=['GET'])
def split():
    settings = open_settings()
    splitter = Separator('spleeter:5stems')
    splitter.separate_to_file('data/input/new_song'+settings['file_extension'], 'data/output/new_song'+settings['file_extension'])
    return render_template('home.html')
    
@app.route('/upload', methods=['POST'])
def upload():
    # read file from post request
    new_song = request.files['new_song']
    file = new_song.filename
    file_name, file_extension = os.path.splitext(file)
    # save details in settings
    write_setting('file_name',file_name)
    write_setting('file_extension', file_extension)
    # save upload on server
    new_song.save('data/input/new_song'+file_extension)
    # return success
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
    
    
# ------------------------------Backend Functions --------------------------- #
def write_setting(key, value):
    global settings_file
    settings_dict = open_settings()
    settings_dict[key] = value
    # re-write json file
    with open('data/' + settings_file, 'w+') as json_file:
        json.dump(settings_dict, json_file)

def open_settings():
    global settings_file
    with open('data/' + settings_file) as json_file:
        settings = json.load(json_file)
    return settings

# ------------------------------- Run Server -------------------------------- #
run_on_local_ip = False
if __name__ == '__main__':
    if run_on_local_ip:
        app.run(port=5000, 
                debug=True,
                host='0.0.0.0')
    else:
        app.run(port=5000, 
                debug=False)

    