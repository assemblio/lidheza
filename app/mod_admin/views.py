from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import CampaignForm, AdvertiserForm, PublisherForm, AdAssetForm
from flask import current_app
from slugify import slugify
from app import mongo_utils
import datetime
import os

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                error.replace('This', 'The %s' % getattr(form, field).label.text)
            )

@mod_admin.route('/adv/<advertiser_slug>', methods=['GET'])
def index(advertiser_slug):
    campaigns = mongo_utils.all()
    return render_template('mod_admin/campaign/index.html', advertiser_slug=advertiser_slug, campaigns=campaigns)

@mod_admin.route('/adv/<advertiser_slug>/campaign/create', methods=['GET', 'POST'])
def campaign(advertiser_slug):

    if request.method == 'GET':
        form = CampaignForm()
        return render_template('mod_admin/campaign/campaign.html', advertiser_slug=advertiser_slug, form=form)

    else:
        form = CampaignForm(request.form)

        if form.validate() == False:
            flash_errors(form)
            return render_template('mod_admin/campaign/campaign.html', advertiser_slug=advertiser_slug, form=form)
        else:

            campaign_slug = slugify(form.campaign_name.data, to_lower=True)

            campaign = {
                'advertiser': advertiser_slug,
                'name': form.campaign_name.data,
                'slug': campaign_slug,
                'url': form.url.data,
                'start': datetime.datetime.combine(form.start_date.data, datetime.time(00, 00)),
                'end': datetime.datetime.combine(form.end_date.data, datetime.time(23, 59)),
                'impressions': {
                    'goal': 0,
                    'count': 0
                }
            }

            campaign_id = mongo_utils.insert_one(campaign)

    return redirect(url_for('admin.campaign_assets', advertiser_slug=advertiser_slug, campaign_slug=campaign_slug, campaign_id=campaign_id))

@mod_admin.route('/adv/<advertiser_slug>/campaign/<campaign_slug>/<campaign_id>/create/assets', methods=['GET'])
def campaign_assets(advertiser_slug, campaign_slug, campaign_id):
    return render_template('mod_admin/campaign/assets_essentials.html',
                           advertiser_slug=advertiser_slug,
                           campaign_slug=campaign_slug,
                           campaign_id=campaign_id)


@mod_admin.route('/adv/campaign/create/assets/upload', methods=['POST'])
def upload_campaign_asset():
    file = request.files['file']

    try:
        if file and allowed_file(file.filename):

            form = AdAssetForm(request.form)

            advertiser_slug = form.advertiser_slug.data
            campaign_slug = form.campaign_slug.data
            campaign_id = form.campaign_id.data
            asset_id = form.asset_id.data

            ext = file.filename[file.filename.rfind('.'):]
            filename = asset_id + ext

            # Create and save the ad asset file
            asset_path = ((current_app.config['UPLOAD_FOLDER'] + '%s/%s-%s/') % (advertiser_slug, campaign_slug, campaign_id)).replace('//','/')

            # Create the directories that do not exist
            if not os.path.exists(os.path.dirname(asset_path)):
                os.makedirs(os.path.dirname(asset_path))

            try:
                file.save(os.path.join(asset_path, filename))

            except Exception,e:
                current_app.logger.error("Failed to save ad asset file '%s': %s", file.filename, str(e))
                return ('An unexpected error has occured. Please contact site administrator.', 500)

            #Update document with asset url
            asset_url = ((current_app.config['AD_ASSET_REL_FOLDER_URL'] + '%s/%s-%s/%s') % (advertiser_slug, campaign_slug, campaign_id, filename)).replace('//','/')

            mongo_utils.insert_asset_url(campaign_id, asset_id, asset_url)
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


@mod_admin.route('/adv/search', methods=['GET', 'POST'])
def ad_search():
    pass

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


