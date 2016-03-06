from flask import Blueprint, request, Response, current_app

import requests

mod_mail = Blueprint('mail', __name__, url_prefix='/admin/mail')


@mod_mail.route('/campaign/stats', methods=['POST'])
def campaign_stats():

    # From request json body, get the to e-mail address and publisher name
    to = request.json['to']
    publisher = request.json['publisherName']
    campaign_id = request.json['campaignId']

    # TODO: Check if there is an advertiser account for the provided 'to' email
    # If there isn't, then prompt the visiting advertiser to create an Advertiser account.
    # When account is created, it is immediately affiliated with the campaign_id.
    # Only then can the advertiser look at the stats.

    app_host = current_app.config['SERVER_HOST']

    # Get MailGun API key and Base URL.
    mg_api_key = current_app.config['MAIL_GUN_API_KEY']
    mg_base_url = current_app.config['MAIL_GUN_API_BASE_URL']

    # TODO: %s/admin/advertiser/campaign/%s should be %s/admin/advertiser/<advertiser_id>/campaign/%s

    # Build text
    message = """
        Dear Advertiser,

        Click on the following link to see out how your ads are doing at %s:
        %s/admin/advertiser/campaign/%s

        Cheers,

        The Lidheza Team
    """ % (publisher, app_host, campaign_id)

    req = requests.post(mg_base_url, auth=('api', mg_api_key), data={
        'from': 'donotreply@lidheza.com',
        'to': to,
        'subject': "Here's how your ads are doing at %s." % publisher,
        'text': message
    })

    if req.status_code != 200:
        # log error
        current_app.logger.error(req.text)

    return Response(status=req.status_code)



