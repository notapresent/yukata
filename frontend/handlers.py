# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from pprint import pformat

from webapp2_extras.appengine.users import login_required, admin_required
from .basehandlers import UserAwareHandler
from webapp2_extras import json

import models.robot
from models.urlsource import URLSource
import models.taskmanager
from models.dataset import DataSet
from models.datafield import NamedDataField
from . import forms


class MainHandler(UserAwareHandler):
    def home(self):
        self.render_response('welcome.html')


class AdminHandler(UserAwareHandler):
    @admin_required
    def index(self):
        self.render_response('admin/index.html')

    @admin_required
    def env(self):
        ctx = {
            'os.environ': pformat(os.environ),
            'self.request.environ': pformat(self.request.environ),
            'self.request': str(self.request).replace('\\r\\n', "\n")
        }
        html = "\n".join("<b>%s</b>\n%s" % (k, v) for k, v in ctx.iteritems())
        self.response.write("<pre>{}</pre>".format(html))


class RobotHandler(UserAwareHandler):
    @login_required
    def index(self):
        template_vars = {
            'robots': models.robot.Robot.list(ancestor=self.current_user.key),
            'schedules': models.robot.SCHEDULES
        }
        self.render_response('robot/index.html', **template_vars)

    @login_required
    def view(self, mid):
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        crawls = models.crawl.BaseCrawl.query(ancestor=robot.key).order(-models.crawl.BaseCrawl.started_at).fetch()
        self.render_response('robot/view.html', robot=robot, mid=mid, crawls=crawls,
                             schedules=models.robot.SCHEDULES)

    def delete(self, mid):
        self.check_login()
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        robot.key.delete()
        return self.redirect_to('robot-index')

    @login_required
    def show_form(self, mid=None):
        if mid:
            robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        else:
            robot = models.robot.Robot()

        form = forms.RobotForm(data=robot.to_dict())
        self.render_response('robot/form.html', form=form, mid=mid)

    def process_form(self, mid=None):
        if mid:
            robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        else:
            robot = models.robot.Robot(parent=self.current_user.key)

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

        self.render_response('robot/form.html', form=form, mid=mid,
                             po=self.request.POST)

    @login_required
    def show_datasets_form(self, mid):
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        datasets = robot.datasets

        new_field_template = NamedDataField()

        datasets.append({'name': '', 'fields': []})
        for ds in robot.datasets:
            if isinstance(ds, DataSet):
                ds.dsid = ds.key.id()
                ds.fields.append(new_field_template)
            else:
                ds['fields'].append(new_field_template.to_dict())
        form = forms.DataSetsForm(datasets=datasets)
        self.render_response('robot/datasetform.html', form=form, mid=mid,
                             po=self.request.POST, fo=form.data)

    def process_datasets_form(self, mid):
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        form = forms.DataSetsForm(self.request.POST)

        if form.validate():
            for ds in form.data['datasets']:
                if not ds['name']:
                    continue

                if ds['dsid']:
                    dataset = DataSet.get_by_id(int(ds['dsid']), parent=robot.key)
                    if ds['delete']:
                        dataset.key.delete()
                        continue

                    dataset.fields = []
                else:
                    dataset = DataSet(name=ds['name'], parent=robot.key)
                    dataset.fields = []

                for f in ds['fields']:
                    if f['name']:
                        field = NamedDataField(**f)
                        dataset.fields.append(field)
                dataset.put()

            return self.redirect_to('robot-view', mid=mid)

        self.render_response('robot/datasetform.html', form=form, mid=mid,
                             po=self.request.POST, fo=form.data)

    @login_required
    def view_job(self, jid):
        job = models.job.Job.get_by_id(int(jid))
        crawl = job.crawl_key.get()
        robot = crawl.key.parent().get()
        self.render_response('robot/job.html', job=job, crawl=crawl, robot=robot)

    @login_required
    def view_crawl(self, mid, cid):
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        crawl = models.crawl.BaseCrawl.get_by_id(int(cid), parent=robot.key)
        jobs = crawl.jobs
        self.render_response('robot/crawl.html', robot=robot, crawl=crawl, jobs=jobs)

    @login_required
    def run(self, mid):
        robot = models.robot.Robot.get_by_id(int(mid), parent=self.current_user.key)
        models.taskmanager.enqueue_robot('/task/runrobot', robot)
        self.response.write(json.encode({'status': 'ok'}))
