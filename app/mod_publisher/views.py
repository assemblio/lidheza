from flask import Blueprint, render_template, flash, request, redirect, url_for
from app import mongo_utils
from forms import ImpressionRateForm

mod_publisher = Blueprint('publisher', __name__, url_prefix='/admin/publisher')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                error.replace('This', 'The %s' % getattr(form, field).label.text)
            )

@mod_publisher.route('/<pid>', methods=['GET'])
def index(pid):
    rateform = ImpressionRateForm()
    publisher = mongo_utils.find_one_user(pid)
    return render_template('mod_publisher/index.html', publisher=publisher, rateform=rateform)

@mod_publisher.route('/<pid>/settings', methods=['GET'])
def settings(pid):
    return render_template('mod_publisher/settings.html', pid=pid)

@mod_publisher.route('/<pid>/update/rate', methods=['POST'])
def update_impression_rate(pid):
    rateform = ImpressionRateForm(request.form)
    if rateform.validate() == False:
        flash_errors(rateform)
        return redirect(url_for('publisher.index', pid=pid))
    else:
        mongo_utils.update_impression_rate(pid, float(rateform.rate.data))
        return redirect(url_for('publisher.index', pid=pid))