from wtforms import Form, DecimalField, validators

class ImpressionRateForm(Form):
    rate = DecimalField('Rate', [validators.Required()])
