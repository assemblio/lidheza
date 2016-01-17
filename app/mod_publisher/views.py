from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from app import mongo_utils
from forms import ImpressionRateForm, CampaignForm, AssetForm, SettingsForm
import datetime
import os

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

    # Before display the default index page, check if the publisher has defined his available ad spaces
    # If none have been set, then redirect the user to the settings page
    if len(publisher['adSpaces']) == 0:
        return redirect(url_for('publisher.settings_adspaces', pid=pid))
    else:
        # Get the ongoing campaigns
        published_campaigns = mongo_utils.get_publisher_published_campaigns(pid)
        draft_campaigns = mongo_utils.get_publisher_draft_campaigns(pid)

        # Render template
        return render_template('mod_publisher/index.html',
                               publisher=publisher,
                               rateform=rateform,
                               published_campaigns=published_campaigns,
                               draft_campaigns=draft_campaigns)

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
    publisher = mongo_utils.find_one_user(pid)

    if request.method == 'GET':
        # Create form and set default impression rate
        form = CampaignForm()
        form.impression_rate.data = publisher['impressionRate']

        return render_template('mod_publisher/campaign/create.html', publisher=publisher, form=form)

    else: # POST
        form = CampaignForm(request.form)

        # If errors, stay on the same page and display errors
        if form.validate() == False:
            flash_errors(form)
            return render_template('mod_publisher/campaign/create.html', publisher=publisher, form=form)
        else:

            campaign = {
                'publisherId': pid,
                'status': 'draft',
                'name': form.campaign_name.data,
                'url': form.url.data,
                'start': datetime.datetime.combine(form.start_date.data, datetime.time(00, 00)),
                'end': datetime.datetime.combine(form.end_date.data, datetime.time(23, 59)),
                'impressions': {
                    'rate': float(form.impression_rate.data),
                    'goal': int(form.impression_goal.data),
                    'count': 0
                }
            }

            campaign_id = mongo_utils.insert_one_campaign(campaign)

            # Move on the loading assets
            return redirect(url_for('publisher.campaign_assets', pid=pid, campaign_id=campaign_id))


@mod_publisher.route('/<pid>/campaign/<campaign_id>/assets', methods=['GET'])
def campaign_assets(pid, campaign_id):
    publisher = mongo_utils.find_one_user(pid)
    form = AssetForm()
    return render_template('mod_publisher/campaign/assets_essentials.html', publisher=publisher, campaign_id=campaign_id, form=form)

@mod_publisher.route('/<pid>/campaign/<campaign_id>/delete', methods=['POST'])
def campaign_delete(pid, campaign_id):
    mongo_utils.delete_one_campaign(campaign_id)
    return redirect(url_for('publisher.index', pid=pid))

@mod_publisher.route('/<pid>/campaign/<campaign_id>/save-as-draft', methods=['POST'])
def campaign_save_as_draft(pid, campaign_id):
    mongo_utils.set_campaign_as_draft(campaign_id)
    return redirect(url_for('publisher.index', pid=pid))

@mod_publisher.route('/<pid>/campaign/<campaign_id>/publish', methods=['POST'])
def campaign_publish(pid, campaign_id):
    mongo_utils.set_campaign_as_published(campaign_id)
    return redirect(url_for('publisher.index', pid=pid))

@mod_publisher.route('/<pid>/settings/ad-spaces', methods=['GET', 'POST'])
def settings_adspaces(pid):
    if request.method == 'GET':
        publisher = mongo_utils.find_one_user(pid)

        form = SettingsForm()
        form.available_ad_spaces.data = publisher['adSpaces']

        return render_template('mod_publisher/settings/adspaces.html', publisher=publisher, form=form)
    else: # POST
        form = SettingsForm(request.form)

        avalailable_ad_spaces = []
        if form.available_ad_spaces.data != None:
            avalailable_ad_spaces = form.available_ad_spaces.data

        mongo_utils.update_publisher_available_ad_spaces(pid, avalailable_ad_spaces)

        return redirect(url_for('publisher.index', pid=pid))


@mod_publisher.route('/<pid>/campaign/<campaign_id>/assets/upload', methods=['POST'])
def upload_campaign_asset(pid, campaign_id):
    file = request.files['file']

    try:
        if file and allowed_file(file.filename):

            form = AssetForm(request.form)
            asset_id = form.asset_id.data

            ext = file.filename[file.filename.rfind('.'):]
            filename = asset_id + ext

            # Create and save the ad asset file
            asset_path = ((current_app.config['UPLOAD_FOLDER'] + '%s/%s/') % (pid, campaign_id)).replace('//','/')

            # Create the directories that do not exist
            if not os.path.exists(os.path.dirname(asset_path)):
                os.makedirs(os.path.dirname(asset_path))

            try:
                file.save(os.path.join(asset_path, filename))

            except Exception,e:
                current_app.logger.error("Failed to save ad asset file '%s': %s", file.filename, str(e))
                return ('An unexpected error has occured. Please contact site administrator.', 500)

            # Update document with asset url
            asset_url = ((current_app.config['AD_ASSET_REL_FOLDER_URL'] + '%s/%s/%s') % (pid, campaign_id, filename)).replace('//','/')

            mongo_utils.insert_asset_url(campaign_id, asset_id, asset_url)
            return ('', 204)

    except Exception,e:
        current_app.logger.error("Ad asset upload error while attempting to upload '%s': %s", file.filename, str(e))
        return ('An unexpected error has occured. Please contact site administrator.', 500)

def allowed_file(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@mod_publisher.route('/<pid>/ad-tags', methods=['GET'])
def ad_tags(pid):
    publisher = mongo_utils.find_one_user(pid)
    return render_template('mod_publisher/adtags.html', publisher=publisher)






