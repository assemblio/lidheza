from flask import Blueprint, render_template, request, redirect, url_for
from forms import CampaignForm, AdvertiserForm, PublisherForm, AdAssetForm
from flask import current_app
from slugify import slugify
from app import mongo_utils
import time
import os

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/', methods=['GET'])
def index():
    campaigns = mongo_utils.all()
    return render_template('mod_admin/index.html', campaigns=campaigns)

@mod_admin.route('/adv/<advertiser_slug>/campaign/create', methods=['GET', 'POST'])
def campaign(advertiser_slug):

    if request.method == 'GET':
        form = CampaignForm()
        return render_template('mod_admin/campaign/campaign.html', form=form)

    else:
        form = CampaignForm(request.form)

        campaign = {
            'advertiser': {
                'name': form.advertiser.data,
                'slug': slugify(form.advertiser.data, to_lower=True),
            },
            'domain': form.domain.data,
            'name': form.campaign_name.data,
            'slug': slugify(form.campaign_name.data, to_lower=True),
            'start': form.start_date.data,
            'end': form.end_date.data,
            'description': form.description.data,
            'impressions': {
                'goal': int(form.impression_goal.data),
                'count': 0
            }
        }

        mongo_utils.save(campaign)

    return redirect(url_for('admin.campaign_assets'))

@mod_admin.route('/adv/<advertiser_slug>/campaign/<campaign_id>/create/assets', methods=['GET'])
def campaign_assets(advertiser_slug, campaign_id):
    return render_template('mod_admin/campaign/assets_essentials.html',
                           advertiser_slug=advertiser_slug,
                           campaign_id=campaign_id)


@mod_admin.route('/adv/campaign/create/assets/upload', methods=['POST'])
def upload_campaign_asset():
    file = request.files['file']

    try:
        if file and allowed_file(file.filename):

            form = AdAssetForm(request.form)

            advertiser_slug = form.advertiser_slug.data
            campaign_id = form.campaign_id.data
            asset_id = form.asset_id.data

            # Get campaign object
            campaign_slug = 'nye-2015'

            ext = file.filename[file.filename.rfind('.'):]
            filename = asset_id + ext

            # Create and save the ad asset file
            asset_path = (current_app.config['UPLOAD_FOLDER'] + '/%s/%s-%s/') % (advertiser_slug, campaign_slug, campaign_id)

            # Create the directories that do not exist
            if not os.path.exists(os.path.dirname(asset_path)):
                os.makedirs(os.path.dirname(asset_path))

            file.save(os.path.join(asset_path, filename))

            #TODO: Update Mongo campaign doc

            return ('', 204)

    except Exception,e:
        current_app.logger.error("Ad asset upload error while attempting to upload '%s': %s", file.filename, str(e))
        return ('An unexpected error has occured. Please contact site administrator.', 500)

def allowed_file(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@mod_admin.route('/adv/create', methods=['GET', 'POST'])
def advertiser():
    if request.method == 'GET':
        form = AdvertiserForm()
        return render_template('mod_admin/advertiser.html', form=form)
    else:
        return 'TODO: Persistence'

@mod_admin.route('/publisher/create', methods=['GET', 'POST'])
def publisher():
    if request.method == 'GET':
        form = PublisherForm()
        return render_template('mod_admin/publisher.html', form=form)
    else:
        return 'TODO: Persistence'

@mod_admin.route('/publisher/search', methods=['GET', 'POST'])
def pub_search():
    pass

@mod_admin.route('/advertiser/search', methods=['GET', 'POST'])
def ad_search():
    pass

