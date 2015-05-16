# -*- coding: utf-8 -*-
from wtforms import (Form, BooleanField, StringField, HiddenField, validators,
                     IntegerField, SelectField, FormField, RadioField, FieldList)
from wtforms_appengine.ndb import model_form, KeyPropertyField


from models.dataset import DataSet

from .datafield import NamedDataFieldForm


class DataSetForm(model_form(DataSet)):
    dsid = HiddenField()
    delete = BooleanField()
    fields = FieldList(FormField(NamedDataFieldForm))

