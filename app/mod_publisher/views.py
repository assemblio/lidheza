from flask import Blueprint, render_template, flash, request, redirect, url_for
from app import mongo_utils
from forms import ImpressionRateForm, CampaignForm, AssetForm
import datetime

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

@mod_publisher.route('/<pid>/update/rate', methods=['POST'])
def update_impression_rate(pid):
    rateform = ImpressionRateForm(request.form)
    if rateform.validate() == False:
        flash_errors(rateform)
        return redirect(url_for('publisher.index', pid=pid))
    else:
        mongo_utils.update_impression_rate(pid, float(rateform.rate.data))
        return redirect(url_for('publisher.index', pid=pid))


@mod_publisher.route('/<pid>/campaign', methods=['GET', 'POST'])
def campaign_create(pid):

    if request.method == 'GET':
        form = CampaignForm()
        return render_template('mod_publisher/campaign/create.html', pid=pid, form=form)

    else: # POST
        form = CampaignForm(request.form)

        # If errors, stay on the same page and display errors
        if form.validate() == False:
            flash_errors(form)
            return render_template('mod_publisher/campaign/create.html', pid=pid, form=form)
        else:

            campaign = {
                'publisherId': pid,
                'status': 'draft',
                'name': form.campaign_name.data,
                'url': form.url.data,
                'start': datetime.datetime.combine(form.start_date.data, datetime.time(00, 00)),
                'end': datetime.datetime.combine(form.end_date.data, datetime.time(23, 59)),
                'impressions': {
                    'goal': 0,
                    'count': 0
                }
            }

            campaign_id = mongo_utils.insert_one_campaign(campaign)

            # Move on the loading assets
            return redirect(url_for('publisher.campaign_assets', pid=pid, campaign_id=campaign_id))


@mod_publisher.route('/<pid>/campaign/<campaign_id>/assets', methods=['GET', 'POST'])
def campaign_assets(pid, campaign_id):
    if request.method == 'GET':
        form = AssetForm()
        return render_template('mod_publisher/campaign/assets_essentials.html', pid=pid, campaign_id=campaign_id, form=form)

    else: # POST
        pass


@mod_publisher.route('/<pid>/settings', methods=['GET'])
def settings(pid):
    return render_template('mod_publisher/settings.html', pid=pid)