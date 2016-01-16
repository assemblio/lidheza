from wtforms import Form, DecimalField, StringField, DateField, HiddenField, validators

class ImpressionRateForm(Form):
    rate = DecimalField('Rate', [validators.Required()])

class CampaignForm(Form):
    campaign_name = StringField('Campaign Name', [validators.Required()])
    url = StringField('URL', [validators.Required()])
    start_date = DateField('Start Date', [validators.Required()], format='%d/%m/%Y')
    end_date = DateField('End Date', [validators.Required()], format='%d/%m/%Y')

class AssetForm(Form):
    campaign_id = HiddenField('Campaign ID')
    asset_id = HiddenField('Asset ID')