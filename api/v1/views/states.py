#!/usr/bin/python3
'''state app connect file.'''
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states_list():
    '''Retrieves the list of all State objects'''
    st_list = []
    for st in storage.all(State).values():
        st_list.append(st.to_dict())
    return jsonify(st_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_obj(state_id):
    '''Retrieves a State object'''
    for ind in storage.all(State).values():
        if ind.id == state_id:
            return jsonify(ind.to_dict())
        else:
            abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    st.delete()
    st.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def new_state():
    '''Creates a State'''
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'name' not in new_request.keys():
        abort(400, description='Missing name')
    state = State(**new_request)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def uodate_state(state_id):
    '''Updates a State object'''
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(st, key, value)
    st.save()
    return make_response(jsonify(st.to_dict())), 200
