#!/usr/bin/python3
'''index.py documentation.'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def return_ok():
    '''return status OK'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def count_obj():
    ''''''
    classes = {"Amenity": Amenity,
               "BaseModel": BaseModel,
               "City": City,
               "Place": Place,
               "Review": Review,
               "State": State,
               "User": User}
    dict_obj = {}
    for cls_name, cls_count in classes.items():
        dict_obj[cls_name] = storage.count(cls_count)
    return jsonify(dict_obj)
