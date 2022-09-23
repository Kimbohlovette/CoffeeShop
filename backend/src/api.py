from crypt import methods
import os
from tokenize import String
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES


@app.route("/drinks", methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        short_drinks = [drink.short() for drink in drinks]
        return jsonify({'success': True, 'drinks': short_drinks})
    except BaseException:
        abort(422)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_long_drinks():
    try:
        drinks = Drink.query.all()
        long_drinks = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': long_drinks
        })
    except BaseException:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    new_drink = Drink(title=title, recipe=json.dumps(recipe))
    new_long_drink = new_drink.long()
    try:
        Drink.insert(new_drink)
        return jsonify({
            'success': True,
            'drinks': [new_long_drink]
        })
    except BaseException:
        abort(422)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except BaseException:
        abort(404)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id
        })
    except BaseException:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return (jsonify({"success": False, "error": 404,
                     "message": "resource not found"}), 404)


@app.errorhandler(405)
def not_found(error):
    return (jsonify({"success": False, "error": 405,
                     "message": "method Not Allowed"}), 405)


@app.errorhandler(AuthError)
def not_found(error):
    return (jsonify(error.error_dict()), error.status_code)
