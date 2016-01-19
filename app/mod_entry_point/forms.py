from wtforms import Form, DecimalField, StringField, TextAreaField, SelectField, PasswordField, validators
from utils import FormUtils

class LoginForm(Form):
    email = StringField('Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class AdvertiserForm(Form):
    name = StringField('Name', [validators.Required()])
    description = TextAreaField('Description')

    registration_number = StringField('Business Registration Number', [validators.Required()])
    fiscal_number = StringField('Fiscal Number', [validators.Required()])

    email = StringField('E-mail', [validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password', [validators.Required()])

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
    name = StringField('Name', [validators.Required()])
    website = StringField('Website', [validators.Required()])
    description = TextAreaField('Description')

    registration_number = StringField('Business Registration Number', [validators.Required()])
    fiscal_number = StringField('Fiscal Number', [validators.Required()])

    email = StringField('E-mail', [validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password', [validators.Required()])

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
    phone = StringField('Phone', [validators.Required()])
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