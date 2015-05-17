# -*- coding: utf-8 -*-
from wtforms import SelectField, FormField
from wtforms_appengine.ndb import model_form

from models.robot import Robot, SCHEDULES
from . import urlsource


class RobotForm(model_form(Robot)):
    schedule = SelectField('Schedule',
                           choices=SCHEDULES.items(),
                           default=SCHEDULES.items()[0][0])
    urlsource = FormField(urlsource.URLSourceForm, 'URL source settings')
