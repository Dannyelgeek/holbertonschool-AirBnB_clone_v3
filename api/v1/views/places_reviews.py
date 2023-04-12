#!/usr/bin/python3
'''reviews app connect file.'''
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def review_list(place_id):
    '''Retrieves the list of all Review objects'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    rw_list = [rw_list.to_dict() for rw_list in place.reviews]
    return jsonify(rw_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_obj(review_id):
    '''Retrieves a Review object'''
    rw = storage.get(Review, review_id)
    if rw:
        return jsonify(rw.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_Review(review_id):
    '''Deletes a Review object'''
    empty_dict = {}
    rw = storage.get(Review, review_id)
    if not rw:
        abort(404)
    rw.delete()
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    '''Creates a review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    if 'name' not in new_request.keys():
        abort(400, description='Missing name')
    rw = Review(**new_request)
    setattr(rw, 'state_id', place_id)
    rw.save()
    return jsonify(rw.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def uodate_city(review_id):
    '''Updates a Review object'''
    rw = storage.get(Review, review_id)
    if not rw:
        abort(404)
    new_request = request.get_json()
    if not new_request:
        abort(400, description='Not a JSON')
    for key, value in new_request.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(rw, key, value)
    rw.save()
    return make_response(jsonify(rw.to_dict())), 200
