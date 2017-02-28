""" ROUTES """
from flask import Blueprint, jsonify, request

blueprint = Blueprint('/api', __name__, url_prefix='/api')

@blueprint.route('/test', methods=['POST'])
def test():
    request_data = request.json
    return jsonify({
        "received": request_data,
    })
