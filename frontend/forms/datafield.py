# -*- coding: utf-8 -*-

from wtforms import StringField, SelectField
from wtforms_appengine.ndb import model_form

from models.datafield import DataField, SELECTOR_TYPES


class DataFieldForm(model_form(DataField)):
    selector_type = SelectField('Schedule', choices=SELECTOR_TYPES.items(),
                                default=SELECTOR_TYPES.items()[0][0])


class NamedDataFieldForm(DataFieldForm):
    name = StringField('Field name')
