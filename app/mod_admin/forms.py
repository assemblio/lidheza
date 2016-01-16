# coding=utf-8
from wtforms import Form, DateField, StringField, HiddenField, validators

class CampaignForm(Form):
    advertiser_slug = HiddenField('Advertiser', [validators.Required()])
    campaign_name = StringField('Campaign Name', [validators.Required()])
    url = StringField('URL', [validators.Required()])
    start_date = DateField('Start Date', [validators.Required()], format='%d/%m/%Y')
    end_date = DateField('End Date', [validators.Required()], format='%d/%m/%Y')


    #description = TextAreaField('Description')

    '''
    target_business_type = SelectMultipleField('Target Type',
        choices=FormUtils.get_business_types() + [('all', 'All')],
        default='all')

    target_website_type = SelectMultipleField('Target Subtype',
        choices=FormUtils.get_website_types() + [('all', 'All')],
        default='all')

    taget_industry = SelectMultipleField('Target Industry',
        choices=FormUtils.get_industries() + [('all', 'All')],
        default='all')
    '''

    # target location?
    # target publisher?

class AdAssetForm(Form):
    #advertiser_id = HiddenField('Advertiser ID')
    advertiser_slug = HiddenField('Advertiser Slug')
    campaign_slug = HiddenField('Campaign Slug')
    campaign_id = HiddenField('Campaign ID')


    asset_id = HiddenField('Asset ID')
    #timestamp = HiddenField('Timestamp')
