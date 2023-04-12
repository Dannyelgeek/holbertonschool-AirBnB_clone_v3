#!/usr/bin/python3
'''places app connect file.'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places/', methods=['GET'],
                 strict_slashes=False)
def place_list(city_id):
    '''Retrieves the list of all City objects'''
    pl = storage.get(City, city_id)
    if not pl:
        abort(404)
    pl_list = [pl_list.to_dict() for pl_list in pl.cities]
    return jsonify(pl_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_obj(place_id):
    '''Retrieves a City object'''
    pl = storage.get(Place, place_id)
    if pl:
        return jsonify(pl.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a City object'''
    empty_dict = {}
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)
    pl.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_city(city_id):
    '''Creates a City'''
    pl = storage.get(City, city_id)
    if not pl:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'user_id' not in new_request.keys():
        abort(400, description='Missing user_id')
    user_vl = storage.get(User, pl['user_id'])
    if not user_vl:
        abort(404)
    if 'name' not in pl.keys():
        abort(400, 'Missing name')
    place_recent = Place(**pl)
    setattr(place_recent, 'city_id', city_id)
    place_recent.save()
    return jsonify(place_recent.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def place_now(place_id):
    '''Updates a State object'''
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(pl, key, value)
    storage.save()
    return make_response(jsonify(pl.to_dict())), 200
