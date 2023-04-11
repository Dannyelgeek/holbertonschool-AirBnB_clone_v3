#!/usr/bin/python3
'''index.py documentation.'''
from api.v1.views import app_views


@app_views.route('/status')
def return_ok():
    status_ok = {"status": "OK"}
    return status_ok.json()
