# -*- coding: utf-8 -*-

from wtforms import StringField
from wtforms_appengine.ndb import model_form

from models.datafield import DataField


class DataFieldForm(model_form(DataField)):
    pass


class NamedDataFieldForm(DataFieldForm):
    name = StringField('Field name')
