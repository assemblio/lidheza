from flask import current_app
import requests


class MailUtils(object):

    def send_campaign_created(self, publisher_name, to, campaign_id):

        app_host = current_app.config['SERVER_HOST']
        frm = 'Lidheza@lidheza.com'
        subject = '%s is publishing your ads.'

        # Build text
        message = """
            Dear Advertiser,

            %s is using lidheza.com to publish your ads on their website.
            Using lidheza.com guarantees that you only pay for the exact number of times people have seen your ads.

            You can create an account at lidheza.com to track how your ads are performing and how much you will be invoiced:
            %s/admin/advertiser/register/%s

            Happy advertising,

            The Lidheza Team
        """ % (publisher_name, app_host, campaign_id)

        return self.send(frm, to, subject, message)

    def send_campaign_stats_to_advertiser(self, publisher_name, to, campaign_id):

        app_host = current_app.config['SERVER_HOST']
        frm = 'Lidheza@lidheza.com'
        subject = "Here's how your ads are doing at %s." % publisher_name

        # TODO: %s/admin/advertiser/campaign/%s should be %s/admin/advertiser/<advertiser_id>/campaign/%s

        # Build text
        message = """
            Dear Advertiser,

            Click on the following link to see how your ads are doing at %s:
            %s/admin/advertiser/campaign/%s

            Happy advertising,

            The Lidheza Team
        """ % (publisher_name, app_host, campaign_id)

        return self.send(frm, to, subject, message)

    def send(self, frm, to, subject, message):

        # Get MailGun API key and Base URL.
        mg_api_key = current_app.config['MAIL_GUN_API_KEY']
        mg_base_url = current_app.config['MAIL_GUN_API_BASE_URL']

        req = requests.post(
            mg_base_url + "/messages",
            auth=('api', mg_api_key),
            data={'from': frm,
                  'to': to,
                  'subject': subject,
                  'text': message
            })

        if req.status_code != 200:
            current_app.logger.error(req.text)
            return False

        return True

