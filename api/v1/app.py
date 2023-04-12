#!/usr/bin/python3
'''API app connect file.'''
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    '''calls storage.close()'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''404 error message'''
    err = {"error": "Not found"}
    return jsonify(err), 404


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
