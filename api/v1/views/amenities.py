#!/usr/bin/python3
'''state app connect file.'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def amenities_list():
    '''Retrieves the list of all Amenity objects'''
    am_list = []
    for am in storage.all(Amenity).values():
        am_list.append(am.to_dict())
    return jsonify(am_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_obj(amenity_id):
    '''Retrieves a Amenity object'''
    for ind in storage.all(Amenity).values():
        if ind.id == amenity_id:
            return jsonify(ind.to_dict())
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Deletes a amenity object'''
    empty_dict = {}
    am = storage.get(Amenity, amenity_id)
    if not am:
        abort(404)
    am.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def new_amenity():
    '''Creates a Amenity'''
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'name' not in new_request.keys():
        abort(400, description='Missing name')
    am = Amenity(**new_request)
    am.save()
    return jsonify(am.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates a amenity object'''
    am = storage.get(Amenity, amenity_id)
    if not am:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(am, key, value)
    am.save()
    return make_response(jsonify(am.to_dict())), 200
