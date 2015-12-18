# coding=utf-8
from wtforms import Form, IntegerField, StringField, TextAreaField

class CampaignForm(Form):
    advertiser = StringField('Advertiser')
    domain = StringField('Domain')
    campaign_name = StringField('Campaign Name')
    start_date = StringField('Start Date')
    end_date = StringField('End Date')
    description = TextAreaField('Description')
    impression_goal = IntegerField('Impression Goal')

