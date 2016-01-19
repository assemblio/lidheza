from wtforms import Form, IntegerField, DecimalField, StringField, DateField, HiddenField, SelectMultipleField, validators, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ImpressionRateForm(Form):
    rate = DecimalField('Default Rate', [validators.Required()])

class CampaignForm(Form):
    id = HiddenField('ID')
    campaign_name = StringField('Campaign Name', [validators.Required()])
    url = StringField('URL', [validators.Required()])
    start_date = DateField('Start Date', [validators.Required()], format='%d/%m/%Y')
    end_date = DateField('End Date', [validators.Required()], format='%d/%m/%Y')
    impression_rate = DecimalField('Impression Rate', [validators.Required()])
    impression_goal = IntegerField('Impression Goal', [validators.Required()], default=10000)

class AssetForm(Form):
    campaign_id = HiddenField('Campaign ID')
    asset_id = HiddenField('Asset ID')

class SettingsForm(Form):
    available_ad_spaces = MultiCheckboxField('Available Ad Spaces',
        choices=[
            ('leaderboard-728x90', 'Leaderboard 728x90'),
            ('full-banner-468x60', 'Full Banner 468x60'),
            ('half-page-300x600', 'Half Page 300x600'),
            ('wide-skyscraper-160x160', 'Wide Skyscraper 160x160'),
            ('vertical-rectangle-240x400', 'Vertical Rectangle 240x400'),
            ('medium-rectangle-300x250', 'Medium Rectangle 300x250')])

