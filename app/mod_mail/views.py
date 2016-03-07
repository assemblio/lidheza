from flask import Blueprint, request, Response
from app import mail_utils

mod_mail = Blueprint('mail', __name__, url_prefix='/admin/mail')


@mod_mail.route('/campaign/stats', methods=['POST'])
def campaign_stats():

    # From request json body, get the to e-mail address and publisher name
    publisher_name = request.json['publisherName']
    to = request.json['to']
    campaign_id = request.json['campaignId']

    # TODO: Check if there is an advertiser account for the provided 'to' email
    # If there isn't, then prompt the visiting advertiser to create an Advertiser account.
    # When account is created, it is immediately affiliated with the campaign_id.
    # Only then can the advertiser look at the stats.

    sent = mail_utils.send_campaign_stats_to_advertiser(publisher_name, to, campaign_id)

    if not sent:
        return Response(status=500)

    return Response(status=200)
