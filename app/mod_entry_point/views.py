from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import AdvertiserForm, PublisherForm
from app import mongo_utils

mod_entry_point = Blueprint('entrypoint', __name__)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                error.replace('This', 'The %s' % getattr(form, field).label.text)
            )

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
        form = PublisherForm(request.form)

        # If errors, stay on the same page and display errors
        if form.validate() == False:
            flash_errors(form)
            return render_template('mod_entry_point/publisher.html', form=form)
        else:
            publisher = {
                'name': form.name.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'password': form.password.data,
                'registrationNumber': form.registration_number.data,
                'fiscalNumber': form.fiscal_number.data,
            }

            publisher_id = mongo_utils.insert_one_publisher(publisher)

            return redirect(url_for('publisher.index', pid=publisher_id))