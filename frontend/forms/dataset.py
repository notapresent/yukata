# -*- coding: utf-8 -*-
from wtforms import BooleanField, HiddenField, FormField, FieldList
from wtforms_appengine.ndb import model_form

from models.dataset import DataSet
from .datafield import NamedDataFieldForm


class DataSetForm(model_form(DataSet)):
    dsid = HiddenField()
    delete = BooleanField()
    fields = FieldList(FormField(NamedDataFieldForm))
