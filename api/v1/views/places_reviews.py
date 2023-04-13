#!/usr/bin/python3
'''reviews app connect file.'''
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def review_list(place_id):
    '''Retrieves the list of all Review objects'''
    pl = storage.get("Place", place_id)
    if pl is None:
        abort(404)
    reviews = []
    for review in pl.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_obj(review_id):
    '''Retrieves a Review object'''
    rw = storage.get(Review, review_id)
    if rw is None:
        abort(404)
    return jsonify(rw.to_dict())


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
    pl = storage.get("Place", place_id)
    if pl is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_request = request.get_json()
    if 'user_id' not in new_request:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    usr = storage.get("User", new_request['user_id'])
    if usr is None:
        abort(404)
    if 'text' not in new_request:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    new_request['place_id'] = place_id
    review = Review(**new_request)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_Review(review_id):
    '''Updates a Review object'''
    rw = storage.get(Review, review_id)
    if rw is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(rw, attr, val)
    rw.save()
    return jsonify(rw.to_dict())
