from wtforms import Form, BooleanField, StringField, validators
from wtforms_appengine.ndb import model_form

from models.account import Account


class AccountForm(model_form(Account, exclude=['apikey'])):
    pass


class AccountRegisterForm(AccountForm):
    accept_tos = BooleanField('I accept terms and conditions',
                              [validators.DataRequired()])
