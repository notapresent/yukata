# -*- coding: utf-8 -*-
from wtforms import Form, StringField, FormField, RadioField

from models.urlsource import URLSOURCE_TYPES
from .datafield import DataFieldForm


class SingleURLSourceForm(Form):
    url = StringField()


class ChainedURLSourceForm(Form):
    url = StringField()
    next_page = FormField(DataFieldForm)


class URLSourceForm(Form):
    kind = RadioField('URL source type',
                      choices=URLSOURCE_TYPES.items(),
                      default=URLSOURCE_TYPES.items()[0][0])
    single = FormField(SingleURLSourceForm)
    chained = FormField(ChainedURLSourceForm)

    def validate(self):
        # TODO
        return True

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if data is not None:
            kwargs = dict(data, **kwargs)

        if obj is not None and hasattr(obj, 'kind'):
            kind = getattr(obj, 'kind')
            kwargs[kind] = obj.to_dict()
        elif kwargs is not None and 'kind' in kwargs:
            kind = kwargs.get('kind')
            kwargs[kind] = kwargs

        super(URLSourceForm, self).process(formdata=formdata, obj=obj, data=data,
                                           **kwargs)

    @property
    def data(self):
        kind = self._fields['kind'].data
        data = dict({'kind': kind})
        data.update(getattr(self, kind).data)
        return data
