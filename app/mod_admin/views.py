from flask import Blueprint, render_template, request, redirect, url_for
from flask import Blueprint, render_template, request, redirect, url_for
from form import CampaignForm
from slugify import slugify
from app import mongo_utils

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/', methods=['GET'])
def index():
    campaigns = mongo_utils.all()
    return render_template('mod_admin/index.html', campaigns=campaigns)

@mod_admin.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        form = CampaignForm()
        return render_template('mod_admin/create.html', form=form)

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


