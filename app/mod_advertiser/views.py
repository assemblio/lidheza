from flask import Blueprint, render_template
import datetime
from app import mongo_utils
import pytz

mod_advertiser = Blueprint('advertiser', __name__, url_prefix='/admin/advertiser')

@mod_advertiser.route('/campaign/<campaign_id>', methods=['GET'])
def campaign(campaign_id):
    campaign = mongo_utils.find_one_campaign(campaign_id)

    #FIXME: Timezone needs to be configurable and retrived from the campaign object
    # Or convert everything in UTC before saving?
    #eastern_tz = pytz.timezone('Europe/Belgrade')
    #today = datetime.datetime.today().replace(tzinfo=eastern_tz)

    today = datetime.datetime.today().replace(tzinfo=pytz.utc)

    return render_template('mod_advertiser/campaign.html', campaign=campaign, today=today)
