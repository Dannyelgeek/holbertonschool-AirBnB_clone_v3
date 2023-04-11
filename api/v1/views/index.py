#!/usr/bin/python3
'''index.py documentation.'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def return_ok():
    '''return status OK'''
    return jsonify(status='OK')
