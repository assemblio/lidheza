from flask import Blueprint, request, Response, current_app
from app import utils, mongo_utils

mod_serve = Blueprint('serve', __name__)

@mod_serve.route('/fetch/<ad_id>', methods=['GET'])
def fetch(ad_id):
    ''' Fetch and returns the advertisement HTML element.
    Process:
        1) Check where the request is coming from (a host, e.g. example.com).
        2) Get ongoing ad campaigns associated with the author of the request
        3) If there are no ongoing ad campaigns, return an empty ad div.
        4) If there are ongoing ad campaigns, return an ad dive with add asset and the target URL.
    :param ad_id:
    :return:
    '''

    # TODO: detect which device the request is coming from.
    # If it's from a website, then get the host as an identifier.
    # If it's from an mobile app, then get app id?
    # For now, we just need to worry about a website
    host_origin = utils.get_host(request.environ['HTTP_ORIGIN'])

    campaign = mongo_utils.get_ongoing_campaign_asset_url_for_publisher(host_origin, True)

    # If there are no on-going campaigns, return an empty ad block
    if campaign is None:
        empty_ad = '''
            <div id="ldz-empty" align="center">
            </div>
            '''
        return Response(empty_ad, mimetype='text/xml')

    # Else, return the randomly selected on-going ad campaign
    else:
        # Check if the publisher supports serving that ad size.
        # We want to avoid service ad sizes that were supported in the past but are now no longer supported.
        # This happens when the publisher removed support for the ad size from the lidheza config for his profile
        # but forgot or couldn't remove the ad container tag on his website.
        publisher_id = campaign['publisher']['id']
        publisher = mongo_utils.find_one_user(publisher_id)
        if ad_id not in publisher['adSpaces']:
            empty_ad = '''
            <div id="ldz-empty" align="center">
            </div>
            '''
            return Response(empty_ad, mimetype='text/xml')

        else:
            ad_asset_url = current_app.config['SERVER_HOST'] + '/' + campaign['assets'][ad_id]
            ad_url = campaign['url']

            ad = '''
                <div id="ldz" align="center">
                    <script>
                        function ldz(){
                            var a=new XMLHttpRequest;
                            a.onreadystatechange = function(){
                                if (a.readyState == 4 && a.status == 200){
                                    location.href="%s";
                                }
                            };
                            a.open("GET","%s/click/publisher/%s/campaign/%s/%s",!1),a.send(null);
                        }
                    </script>
                    <a id="ldz-click" href="#" target="_self" onClick="ldz()">
                        <img id="ldz-img" src="%s"/>
                    </a>
                </div>
                ''' % (ad_url, current_app.config['SERVER_HOST'], publisher_id, campaign['_id'], ad_id, ad_asset_url)

            return Response(ad, mimetype='text/xml')

@mod_serve.route('/click/publisher/<publisher_id>/campaign/<campaign_id>/<ad_id>', methods=['GET'])
def click(publisher_id, campaign_id, ad_id):
    '''
    This is just to log a click on the ad so that we can, through a cron job,
    collect the number of times an ad has been clicked for a specific ad size
    from a specific ad campaign.
    :param campaign_id:
    :param ad_id
    :return:
    '''
    return ('', 200)