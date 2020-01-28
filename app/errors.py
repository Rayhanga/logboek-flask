from flask import make_response, jsonify

from app import app, auth

## 500 ##
@app.errorhandler(500)
def internal_server_error(err):
    return make_response(jsonify({
        'error': 'Internal Server Error',
        'error_code': '500'
    }))    

## 404 ##
@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({
        'error': 'Not Found',
        'error_code': '404'
    }))

## 400 ##
@app.errorhandler(400)
def bad_request(err):
    return make_response(jsonify({
        'error': 'Bad Request',
        'error_code': '400'
    }))

## 405 ##
@app.errorhandler(405)
def method_not_allowed(err):
    return make_response(jsonify({
        'error': 'Method Not Allowed',
        'error_code': '405'
    }))

## 409 ##
@app.errorhandler(409)
def data_conflict(err):
    return make_response(jsonify({
        'error': 'Data Conflict',
        'error_code': '409'
    }))    

## Auth Error ##
@auth.error_handler
def auth_error():
    return make_response(jsonify({
        'error': 'Unauthorized Access',
        'error_code': '401'
    }))