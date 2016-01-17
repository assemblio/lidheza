from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import AdvertiserForm, PublisherForm, LoginForm
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
    loginform = LoginForm()
    return render_template('mod_entry_point/index.html', loginform=loginform)


@mod_entry_point.route('/login', methods=['POST'])
def login():
    #TODO: session management - login

    loginform = LoginForm(request.form)

    # If errors, stay on the same page and display errors
    if loginform.validate() == False:
        flash_errors(loginform)
        return render_template('mod_entry_point/index.html', loginform=loginform)
    else:
        user = mongo_utils.find_one_user_by_email(loginform.email.data)
        if user != None and user['password'] == loginform.password.data:

            # logged in user can be either be of type publisher or advertiser
            return redirect(url_for('%s.index' % user['type'], pid=str(user['_id'])))
        else:
            return redirect(url_for('entrypoint.index'))


@mod_entry_point.route('/logout', methods=['POST'])
def logout():
    #TODO: session managemenet - logout.
    return redirect(url_for('entrypoint.index'))

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
                'type': 'publisher',
                'name': form.name.data,
                'phone': form.phone.data,
                'email': form.email.data,
                'password': form.password.data,
                'registrationNumber': form.registration_number.data,
                'fiscalNumber': form.fiscal_number.data,
                'impressionRate': 0.01,
                'adSpaces': []
            }

            publisher_id = mongo_utils.insert_one_user(publisher)

            return redirect(url_for('publisher.index', pid=publisher_id))