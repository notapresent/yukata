# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from pprint import pformat

from webapp2_extras import json

from models import taskmanager
from models.crawl import Crawl
from models.dataset import DataSet
from models.robot import Robot, SCHEDULES
from models.urlsource import URLSource
from models.datafield import NamedDataField
from models.job import Job
from . import basehandlers
from . import forms


class MainHandler(basehandlers.BaseHandler):
    def home(self):
        self.render_response('welcome.html')


class AdminHandler(basehandlers.AdminHandler):
    def index(self):
        self.render_response('admin/index.html')

    def env(self):
        ctx = {
            'os.environ': pformat(os.environ),
            'self.request.environ': pformat(self.request.environ),
            'self.request': str(self.request).replace('\\r\\n', "\n")
        }
        html = "\n".join("<b>%s</b>\n%s" % (k, v) for k, v in ctx.iteritems())
        self.response.write("<pre>{}</pre>".format(html))


class RobotHandler(basehandlers.UserHandler):
    def index(self):
        template_vars = {
            'robots': Robot.list(ancestor=self.current_user.key),
            'schedules': SCHEDULES
        }
        self.render_response('robot/index.html', **template_vars)

    def view(self, mid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        crawls = Crawl.query(ancestor=robot.key).order(-Crawl.started_at).fetch()
        datasets = DataSet.query(ancestor=robot.key).fetch()
        self.render_response('robot/view.html', robot=robot, mid=mid, crawls=crawls,
                             datasets=datasets, schedules=SCHEDULES)

    def delete(self, mid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        robot.key.delete()
        return self.redirect_to('robot-index')

    def show_form(self, mid=None):
        if mid:
            robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        else:
            robot = Robot()

        form = forms.RobotForm(data=robot.to_dict())
        self.render_response('robot/form.html', form=form, mid=mid, robot=robot)

    def process_form(self, mid=None):
        if mid:
            robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        else:
            robot = Robot(parent=self.current_user.key)

        form = forms.RobotForm(self.request.POST, obj=robot)

        if form.validate():
            # TODO better populate object
            robot.name = form.data['name']
            robot.schedule = form.data['schedule']
            robot.rps = form.data['rps']
            robot.timeout = form.data['timeout']

            robot.urlsource = URLSource.factory(form.urlsource.form.data)
            key = robot.put()
            return self.redirect_to('robot-view', mid=key.id())

        self.render_response('robot/form.html', form=form, mid=mid, robot=robot)

    def view_job(self, jid):
        job = Job.get_by_id(int(jid))
        crawl = job.crawl_key.get()
        robot = crawl.key.parent().get()
        self.render_response('robot/job.html', job=job, crawl=crawl, robot=robot)

    def view_crawl(self, mid, cid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        crawl = Crawl.get_by_id(int(cid), parent=robot.key)
        jobs = crawl.jobs
        self.render_response('robot/crawl.html', robot=robot, crawl=crawl, jobs=jobs)

    def run(self, mid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        taskmanager.enqueue_robot('/task/runrobot', robot)
        self.response.write(json.encode({'status': 'ok'}))


class DataSetHandler(basehandlers.UserHandler):
    def show_form(self, mid, dsid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        if dsid:
            dataset = DataSet.get_by_id(int(dsid), parent=robot.key)
        else:
            dataset = DataSet(parent=robot.key)

        form = forms.DataSetForm(data=dataset.to_dict())
        self.render_response('robot/datasetform.html', form=form, mid=mid, dsid=dsid,
                             dataset=dataset)

    def process_form(self, mid, dsid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        if dsid:
            dataset = DataSet.get_by_id(int(dsid), parent=robot.key)
        else:
            dataset = DataSet(parent=robot.key)

        form = forms.DataSetForm(self.request.POST)
        if form.validate():
            dataset.populate(**form.data)

            key = dataset.put()
            return self.redirect_to('dataset-edit', mid=mid, dsid=key.id())

        self.render_response('robot/datasetform.html', form=form, mid=mid, dsid=dsid,
                             dataset=dataset)

    def delete(self, mid, dsid):
        robot = Robot.get_by_id(int(mid), parent=self.current_user.key)
        dataset = DataSet.get_by_id(int(dsid), parent=robot.key)
        dataset.key.delete()
        return self.redirect_to('robot-view', mid=mid)
