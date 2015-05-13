import itertools

from wtforms import (Form, BooleanField, StringField, HiddenField, validators,
                     IntegerField, SelectField, FormField, RadioField)
from wtforms_appengine.ndb import model_form, KeyPropertyField
from wtforms.utils import unset_value
from wtforms.compat import with_metaclass, iteritems, itervalues

from models.account import Account
from models.miner import Miner, SCHEDULES
from models.urlsource import (SingleURLSource, ChainedURLSource, BaseURLSource,
                              DatasetURLSource, URLSOURCE_TYPES)
from models.datafield import DataField, NamedDataField, SELECTOR_TYPES
from models.dataset import DataSet


class AccountForm(model_form(Account, exclude=['apikey'])):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        # FIXME: Is this correct way of doing it?
        self.display_name.validators.append(validators.Length(min=3))


class AccountRegisterForm(AccountForm):
    accept_tos = BooleanField('I accept terms and conditions',
                              [validators.DataRequired()])


class SingleURLSourceForm(model_form(SingleURLSource, exclude=['kind'])):
    pass


class DataFieldForm(model_form(DataField)):
    pass


class ChainedURLSourceForm(model_form(ChainedURLSource, exclude=['kind'])):
    nextpage = FormField(DataFieldForm)


class DataSetURLSourceForm(model_form(DatasetURLSource,  exclude=['kind'])):
    field_name = SelectField('Source field', choices=[])


class NamedDataFieldForm(DataFieldForm):
    """
    Form for single datafield
    """
    name = StringField('Field name')


class DataSetForm(model_form(DataSet)):
    pass


class ExtraFormField(FormField):
    def validate(self, form, extra_validators=tuple()):
        # Only run extra validators, since normal validators are forbidden
        chain = itertools.chain(extra_validators)
        stop_validation = self._run_validation_chain(form, chain)

        if stop_validation:
            return not self.errors

        return self.form.validate()


class URLSourceForm(Form):
    kind = RadioField('URL source type',
                                choices=URLSOURCE_TYPES.items(),
                                default=URLSOURCE_TYPES.items()[0][0])
    single = ExtraFormField(SingleURLSourceForm, default=None)
    chained = ExtraFormField(ChainedURLSourceForm, default=None)
    dataset = ExtraFormField(DataSetURLSourceForm, default=None)

    def validate_single(form, field):
        if form.data['kind'] != u'single':
            raise validators.StopValidation

    def validate_chained(form, field):
        if form.data['kind'] != u'chained':
            raise validators.StopValidation

    def validate_dataset(form, field):
        if form.data['kind'] != u'dataset':
            raise validators.StopValidation

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if data is None:
            data = dict()

        if obj and obj.kind:
            data['kind'] = obj.kind
            data[obj.kind] = obj.to_dict()

        super(URLSourceForm, self).process(formdata=formdata, obj=obj,
                                           data=data, **kwargs)


class MinerForm(model_form(Miner)):
    # mid = IntegerField(widget=HiddenInput())
    # name = StringField('Miner name', [validators.Length(min=4)])
    schedule=SelectField('Schedule',
                           choices=SCHEDULES.items(),
                           default=SCHEDULES.items()[0][0])
    urlsource=FormField(URLSourceForm, 'URL source settings')
    datasets=FormField(DataSetForm, 'Dataset')
