from flask import Blueprint, render_template, request
from forms import AdvertiserForm, PublisherForm


mod_entry_point = Blueprint('entrypoint', __name__)

@mod_entry_point.route('/', methods=['GET'])
def index():
    return render_template('mod_entry_point/index.html')


@mod_entry_point.route('/advertiser', methods=['GET', 'POST'])
def advertiser():
    if request.method == 'GET':
        form = AdvertiserForm()
        return render_template('mod_entry_point/advertiser.html', form=form)
    else:
        return 'TODO: Persistence'


@mod_entry_point.route('/publisher', methods=['GET', 'POST'])
def publisher():
    if request.method == 'GET':
        form = PublisherForm()
        return render_template('mod_entry_point/publisher.html', form=form)
    else:
        return 'TODO: Persistence'
