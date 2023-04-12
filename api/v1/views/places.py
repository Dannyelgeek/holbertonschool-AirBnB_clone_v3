#!/usr/bin/python3
'''places app connect file.'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_list(city_id):
    '''Retrieves the list of all Place objects'''
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    places = [places.to_dict() for places in ct.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_obj(place_id):
    '''Retrieves a Place object'''
    pl = storage.get(Place, place_id)
    if pl:
        return jsonify(pl.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a City object'''
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)
    pl.delete()
    storage.save()
    return jsonify(), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    '''Creates a Place'''
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)

    new_request = request.get_json()
    if not new_request:
        abort(400, 'Not a JSON')

    if 'user_id' not in new_request.keys():
        abort(400, 'Missing user_id')

    valid_user = storage.get(User, new_request['user_id'])
    if not valid_user:
        abort(404)

    if 'name' not in new_request.keys():
        abort(400, 'Missing name')

    new_pl = Place(**new_request)
    setattr(new_pl, 'city_id', city_id)
    new_pl.save()
    return jsonify(new_pl.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_now(place_id):
    '''Updates a State object'''
    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)

    new_request = request.get_json()
    if not new_request:
        abort(400, 'Not a JSON')

    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(pl, key, value)
    storage.save()
    return make_response(jsonify(pl.to_dict()), 200)
