from wtforms import (Form, BooleanField, StringField, HiddenField, validators,
                     IntegerField, SelectField)
from wtforms.widgets import HiddenInput
from wtforms_appengine.ndb import model_form

from models.account import Account
from models import SCHEDULES

class AccountForm(model_form(Account, exclude=['apikey'])):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        # FIXME: Is this correct way of doing it?
        self.display_name.validators = [validators.Length(min=3)]


class AccountRegisterForm(AccountForm):
    accept_tos = BooleanField('I accept terms and conditions',
                              [validators.DataRequired()])


class BaseURLSourceForm(Form):
    pass


class SingleURLSourceForm(BaseURLSourceForm):
    url = StringField('URL', [validators.URL()])


class MinerForm(Form):
    # mid = IntegerField(widget=HiddenInput())
    name = StringField('Miner name')
    schedule = SelectField('Schedule', default='m', choices=SCHEDULES.items())

