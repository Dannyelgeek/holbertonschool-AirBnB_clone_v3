#!/usr/bin/python3
'''cities app connect file.'''
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities/', methods=['GET'],
                 strict_slashes=False)
def City_list(state_id):
    '''Retrieves the list of all City objects'''
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    ct_list = [ct_list.to_dict() for ct_list in st.cities]
    return jsonify(ct_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_obj(city_id):
    '''Retrieves a City object'''
    ct = storage.get(City, city_id)
    if ct:
        return jsonify(ct.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''Deletes a City object'''
    empty_dict = {}
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    ct.delete()
    storage.save()
    return jsonify(empty_dict), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    '''Creates a City'''
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'name' not in new_request.keys():
        abort(400, description='Missing name')
    city = City(**new_request)
    setattr(city, 'state_id', state_id)
    city.save()
    return jsonify(city.to_dict()), 201
