from wtforms import Form, DecimalField, StringField, TextAreaField, SelectField, PasswordField
from utils import FormUtils

class AdvertiserForm(Form):
    email = StringField('E-mail')
    password = PasswordField('Password')
    retype_password = PasswordField('Retype Password')

    name = StringField('Name')

    # Address
    street = StringField('Street')
    city = StringField('City')
    municipality = StringField('Municipality')
    country = StringField('Country')

    phone = StringField('Phone')
    viber = StringField('Viber')

    industry = SelectField('Industry',
        choices=FormUtils.get_industries() + [('other', 'Other')],
        default='other')

    type = SelectField('type',
        choices=[
            ('business','Business'),
            ('government','Government'),
            ('individual','Individual'),
            ('non-profit','Non-Profit')
        ],
        default='business')


class PublisherForm(Form):
    name = StringField('Name')
    description = TextAreaField('Description')

    registration_number = StringField('Registration Number')
    tax_number = StringField('Tax Number')

    email = StringField('E-mail')
    password = PasswordField('Password')
    retype_password = PasswordField('Retype Password')

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