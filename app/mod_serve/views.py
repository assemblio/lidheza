from flask import Blueprint, jsonify
from app import mongo_utils

mod_serve = Blueprint('serve', __name__)

@mod_serve.route('/fetch/<width>/<height>', methods=['GET'])
def fetch(width, height):
    #TODO: Check that the request is coming for a valid publisher.
    #TODO: fetch an add asset
    return 'https://placehold.it/%sx%s' % (width, height)