# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import urllib
from pprint import pformat

from google.appengine.api import users
from webapp2_extras.appengine.users import login_required, admin_required
from .basehandlers import UserAwareHandler
from webapp2_extras import json

from models.account import Account
import models.miner
from models.urlsource import build_urlsource
import models.taskmanager
from models.dataset import DataSet
from models.datafield import NamedDataField
import forms


class MainHandler(UserAwareHandler):
    def home(self):
        self.render_response('welcome.html')


class AdminHandler(UserAwareHandler):
    def dispatch(self):
        self.check_admin()
        super(AdminHandler, self).dispatch()

    def index(self):
        self.render_response('admin/index.html')

    def env(self):
        ctx = {
            'os.environ': pformat(os.environ.copy()),
            'self.request.environ': pformat(self.request.environ.copy()),
            'self.request': str(self.request).replace('\\r\\n', "\n")
        }
        html = "\n".join("<b>%s</b>\n%s" % (k, v) for k, v in ctx.iteritems())
        self.response.write("<pre>{}</pre>".format(html))


class AccountHandler(UserAwareHandler):
    @login_required
    def view(self):
        acc = self.current_account
        self.render_response('account/view.html', account=acc)

    @login_required
    def edit(self):
        accform = forms.AccountForm(obj=self.current_account)
        self.render_response('account/form.html', form=accform)

    def save(self):
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))
        account = self.current_account
        # Populate form values from POST, then add missing fields from account
        accform = forms.AccountForm(self.request.POST, account)

        if accform.validate():
            accform.populate_obj(account)
            account.put()
            self.redirect_to('account-view')

        self.render_response('account/form.html', form=accform)

    @login_required
    def regform(self):
        account = Account(display_name=self.current_user.nickname())
        context = {
            'form': forms.AccountRegisterForm(obj=account),
            'next': urllib.unquote_plus(self.request.get('next')),
        }
        self.render_response('account/form.html', **context)

    def create(self):
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))

        form = forms.AccountRegisterForm(self.request.POST)
        next_url = self.request.get('next') or self.uri_for('home')

        if form.validate():
            acc = Account(id=self.current_user.user_id())
            acc.display_name = form.display_name.data
            acc.put()
            return self.redirect(next_url, abort=True)

        context = {'form': form, 'next': next_url}
        self.render_response('account/form.html', **context)


class MinerHandler(UserAwareHandler):
    @login_required
    def index(self):
        template_vars = {
            'miners': models.miner.Miner.list(ancestor=self.current_account.key),
            'schedules': models.miner.SCHEDULES
        }
        self.render_response('miner/index.html', **template_vars)

    @login_required
    def view(self, mid):
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        crawls = models.crawl.BaseCrawl.query(ancestor=miner.key).order(-models.crawl.BaseCrawl.started_at).fetch()
        self.render_response('miner/view.html', miner=miner, mid=mid, crawls=crawls,
                             schedules=models.miner.SCHEDULES)

    def delete(self, mid):
        self.check_login()
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        miner.key.delete()
        return self.redirect_to('miner-index')

    @login_required
    def show_form(self, mid=None):
        if mid is None:
            miner = models.miner.Miner(name='')
        else:
            miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)

        form = forms.MinerForm(obj=miner)
        self.render_response('miner/form.html', form=form, mid=mid)

    def process_form(self, mid=None):
        if mid is None:
            miner = models.miner.Miner(name='', parent=self.current_account.key)
        else:
            miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)

        form = forms.MinerForm(self.request.POST, obj=miner)

        if form.validate():
            miner.name = form.data['name']
            miner.schedule = form.data['schedule']

            ustype = form.data['urlsource']['kind']
            miner.urlsource = build_urlsource(ustype,
                                              form.data['urlsource'][ustype])
            key = miner.put()
            return self.redirect_to('miner-view', mid=key.id())

        self.render_response('miner/form.html', form=form, mid=mid,
                             po=self.request.POST)

    @login_required
    def show_datasets_form(self, mid):
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        datasets = miner.datasets

        new_field_template = NamedDataField()

        datasets.append({'name': '', 'fields': []})
        for ds in miner.datasets:
            if isinstance(ds, DataSet):
                ds.dsid = ds.key.id()
                ds.fields.append(new_field_template)
            else:
                ds['fields'].append(new_field_template.to_dict())
        form = forms.DataSetsForm(datasets=datasets)
        self.render_response('miner/datasetform.html', form=form, mid=mid,
                             po=self.request.POST, fo=form.data)

    def process_datasets_form(self, mid):
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        form = forms.DataSetsForm(self.request.POST)

        if form.validate():
            for ds in form.data['datasets']:
                if not ds['name']:
                    continue

                if ds['dsid']:
                    dataset = DataSet.get_by_id(int(ds['dsid']), parent=miner.key)
                    if ds['delete']:
                        dataset.key.delete()
                        continue

                    dataset.fields = []
                else:
                    dataset = DataSet(name=ds['name'], parent=miner.key)
                    dataset.fields = []

                for f in ds['fields']:
                    if f['name']:
                        field = NamedDataField(**f)
                        dataset.fields.append(field)
                dataset.put()

            return self.redirect_to('miner-view', mid=mid)

        self.render_response('miner/datasetform.html', form=form, mid=mid,
                             po=self.request.POST, fo=form.data)

    @login_required
    def view_job(self, jid):
        job = models.job.Job.get_by_id(int(jid))
        crawl = job.crawl_key.get()
        miner = crawl.key.parent().get()
        self.render_response('miner/job.html', job=job, crawl=crawl, miner=miner)

    @login_required
    def view_crawl(self, mid, cid):
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        crawl = models.crawl.BaseCrawl.get_by_id(int(cid), parent=miner.key)
        jobs = crawl.jobs
        self.render_response('miner/crawl.html', miner=miner, crawl=crawl, jobs=jobs)

    @login_required
    def run(self, mid):
        miner = models.miner.Miner.get_by_id(int(mid), parent=self.current_account.key)
        models.taskmanager.run_miner(miner)
        self.response.write(json.encode({'status': 'ok'}))
