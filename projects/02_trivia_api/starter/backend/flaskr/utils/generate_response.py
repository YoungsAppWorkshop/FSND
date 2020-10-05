from flask import jsonify


def generate_response(status=200, message='OK', data={}):
    """Utility function to generate JSON body for API response
    """
    return jsonify({
        'status': status,
        'message': message,
        'data': data
    }), status
