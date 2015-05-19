# -*- coding: utf-8 -*-
from wtforms import FormField, FieldList
from wtforms.compat import iteritems
from wtforms_appengine.ndb import model_form

from models.dataset import DataSet
from models.datafield import NamedDataField
from .datafield import NamedDataFieldForm


class DataSetForm(model_form(DataSet)):
    datafields = FieldList(FormField(NamedDataFieldForm, label=''), min_entries=1)

    @property
    def data(self):
        data = super(DataSetForm, self).data
        data['datafields'] = [field for field in data['datafields'] if field['name']]
        return data
