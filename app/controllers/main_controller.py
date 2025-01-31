from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('', methods=['GET'])
def main():
    return jsonify('hello world'), 200

