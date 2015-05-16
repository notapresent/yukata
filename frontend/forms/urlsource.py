# -*- coding: utf-8 -*-
import itertools


from wtforms import (Form, BooleanField, StringField, HiddenField, validators,
                     IntegerField, SelectField, FormField, RadioField, FieldList)
from wtforms.compat import with_metaclass, iteritems, itervalues


from models.urlsource import (SingleURLSource, ChainedURLSource, URLSource,
                              URLSOURCE_TYPES)
from .datafield import DataFieldForm


class SingleURLSourceForm(Form):
    url = StringField()


class ChainedURLSourceForm(Form):
    url = StringField()
    nextpage = FormField(DataFieldForm)


class URLSourceForm(Form):
    class_name = RadioField('URL source type',
                            choices=URLSOURCE_TYPES.items(),
                            default=URLSOURCE_TYPES.items()[0][0])
    SingleURLSource = FormField(SingleURLSourceForm, default=None)
    ChainedURLSource = FormField(ChainedURLSourceForm, default=None)

    def validate(self):
        # TODO
        return True

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if data and data['class_']:
            class_name = data['class_'][-1]
            data['class_name'] = class_name
            data[class_name] = data
        elif kwargs and kwargs['class_']:
            class_name = kwargs['class_'][-1]
            kwargs['kind'] = class_name
            kwargs[class_name] = kwargs


        super(URLSourceForm, self).process(formdata=formdata, obj=obj,
                                           data=data, **kwargs)

    @property
    def data(self):
        class_name = self._fields['class_name'].data
        data = dict({'class_name': class_name})
        data.update(getattr(self, class_name).data)
        # return dict((name, f.data) for name, f in iteritems(self._fields))
        return data
