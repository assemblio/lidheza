from flask import Blueprint, render_template, flash
from app import mongo_utils

mod_publisher = Blueprint('publisher', __name__, url_prefix='/admin/publisher')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                error.replace('This', 'The %s' % getattr(form, field).label.text)
            )

@mod_publisher.route('/<pid>', methods=['GET'])
def index(pid):
    publisher = mongo_utils.find_one_publisher(pid)
    return render_template('mod_publisher/index.html', publisher=publisher)

@mod_publisher.route('/<pid>/settings', methods=['GET'])
def settings(pid):
    return render_template('mod_publisher/settings.html', pid=pid)