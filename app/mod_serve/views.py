from flask import Blueprint, jsonify
from app import mongo_utils

mod_serve = Blueprint('serve', __name__)

@mod_serve.route('/fetch', methods=['GET'])
def fetch():
    campaign = mongo_utils.get()
    return jsonify(campaign)