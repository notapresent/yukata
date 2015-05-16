# -*- coding: utf-8 -*-
import itertools

from wtforms import (Form, BooleanField, StringField, HiddenField, validators,
                     IntegerField, SelectField, FormField, RadioField, FieldList)
from wtforms_appengine.ndb import model_form, KeyPropertyField
from wtforms.utils import unset_value
from wtforms.compat import with_metaclass, iteritems, itervalues



from models.datafield import DataField, NamedDataField, SELECTOR_TYPES



class DataFieldForm(model_form(DataField)):
    pass


class NamedDataFieldForm(DataFieldForm):
    name = StringField('Field name')

