#!/usr/bin/python3
'''state app connect file.'''
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user_list():
    '''Retrieves the list of all State objects'''
    ur_list = [us.to_dict() for us in storage.all(User).values()]
    return jsonify(ur_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def usr_obj(user_id):
    '''Retrieves a State object'''
    for usr_sto in storage.all(User).values():
        if usr_sto.id == user_id:
            return jsonify(usr_sto.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''Deletes a State object'''
    empty_dict = {}
    ur = storage.get(User, user_id)
    if not ur:
        abort(404)
    ur.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
    '''Creates a user'''
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'name' not in new_request.keys():
        abort(400, description='Missing name')
    usr = User(**new_request)
    usr.save()
    return jsonify(usr.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''Updates a State object'''
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(usr, key, value)
    usr.save()
    return make_response(jsonify(usr.to_dict())), 200
