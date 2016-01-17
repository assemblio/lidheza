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
                    'goal': int(form.impression_goal.data),
                    'count': 0
                }
            }

            campaign_id = mongo_utils.insert_one_campaign(campaign)

            # Move on the loading assets
            return redirect(url_for('publisher.campaign_assets', pid=pid, campaign_id=campaign_id))


@mod_publisher.route('/<pid>/campaign/<campaign_id>/assets', methods=['GET', 'POST'])
def campaign_assets(pid, campaign_id):
    if request.method == 'GET':
        publisher = mongo_utils.find_one_user(pid)
        form = AssetForm()
        return render_template('mod_publisher/campaign/assets_essentials.html', publisher=publisher, campaign_id=campaign_id, form=form)

    else: # POST
        pass


@mod_publisher.route('/<pid>/settings', methods=['GET', 'POST'])
def settings(pid):
    if request.method == 'GET':
        publisher = mongo_utils.find_one_user(pid)

        form = SettingsForm()
        form.available_ad_spaces.data = publisher['adSpaces']

        return render_template('mod_publisher/settings.html', pid=pid, form=form)
    else: # POST
        form = SettingsForm(request.form)

        #ad_spaces = {}
        #for available_ad_space in  form.available_ad_spaces.data:
        #    ad_spaces[available_ad_space] = True
        mongo_utils.update_publisher_available_ad_spaces(pid, form.available_ad_spaces.data)

        return render_template('mod_publisher/settings.html', pid=pid, form=form)


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



