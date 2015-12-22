from flask import Blueprint, render_template, request, redirect, url_for
from forms import CampaignForm, AdvertiserForm, PublisherForm
from slugify import slugify
from app import mongo_utils

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/', methods=['GET'])
def index():
    campaigns = mongo_utils.all()
    return render_template('mod_admin/index.html', campaigns=campaigns)

@mod_admin.route('/campaign/create', methods=['GET', 'POST'])
def campaign():

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

    return redirect(url_for('admin.index'))

@mod_admin.route('/campaign/create/assets', methods=['GET', 'POST'])
def campaign_assets():
    return render_template('mod_admin/campaign/assets_essentials.html')

@mod_admin.route('/advertiser/create', methods=['GET', 'POST'])
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

