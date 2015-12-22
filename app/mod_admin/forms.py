# coding=utf-8
from wtforms import Form, IntegerField, DecimalField, StringField, TextAreaField, SelectField, SelectMultipleField, PasswordField, HiddenField
from utils import FormUtils

class CampaignForm(Form):
    advertiser = StringField('Advertiser')
    domain = StringField('Domain')
    campaign_name = StringField('Campaign Name')
    start_date = StringField('Start Date')
    end_date = StringField('End Date')
    description = TextAreaField('Description')
    impression_goal = IntegerField('Impression Goal')

    target_business_type = SelectMultipleField('Type',
        choices=FormUtils.get_business_types() + [('all', 'All')],
        default='all')

    taget_industry = SelectMultipleField('Industry',
        choices=FormUtils.get_industries() + [('all', 'All')],
        default='all')

    target_website_type = SelectMultipleField('Subtype',
        choices=FormUtils.get_website_types() + [('all', 'All')],
        default='all')

    # target location?
    # target publisher?

class AdvertiserForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

    name = StringField('Name')

    # Address
    street = StringField('Street')
    city = StringField('City')
    municipality = StringField('Municipality')
    country = StringField('Country')

    email = StringField('E-mail')
    phone = StringField('Phone')
    viber = StringField('Viber')

    industry = SelectField('Industry',
        choices=FormUtils.get_industries() + [('other', 'Other')],
        default='other')

    type = SelectField('type',
        choices=[
            ('business','Business'),
            ('individual','Individual'),
            ('non-profit','Non-Profit')
        ],
        default='business')


class PublisherForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

    name = StringField('Name')
    description = TextAreaField('Description')

    registration_number = StringField('Registration Number')
    tax_number = StringField('Tax Number')

    type = SelectField('Type',
        choices=FormUtils.get_business_types() + [('other', 'Other')],
        default='website')

    industry = SelectField('Industry',
        choices=FormUtils.get_industries() + [('other', 'Other')],
        default='media')

    website_type = SelectField('Subtype',
        choices=FormUtils.get_website_types() + [('other', 'Other')],
        default='news')

    # Contact
    email = StringField('E-mail')
    phone = StringField('Phone')
    viber = StringField('Viber')

    # Address
    street = StringField('Street')
    city = StringField('City')
    municipality = StringField('Municipality')
    country = StringField('Country')

    # Social Media
    website = StringField('Website')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    linked_in = StringField('LinkedIn')

    # Impression rate and currency
    rate = DecimalField('Impression Rate', default=0.01)
    currency = SelectField('Currency',
        choices=[
            ('EUR','EUR')
        ],
        default='EUR')

class AdAssetForm(Form):
    #advertiser_id = HiddenField('Advertiser ID')
    advertiser_slug = HiddenField('Advertiser Slug')

    campaign_id = HiddenField('Campaign ID')
    #campaign_slug = HiddenField('Campaign Slug')

    asset_id = HiddenField('Asset ID')
    #timestamp = HiddenField('Timestamp')
