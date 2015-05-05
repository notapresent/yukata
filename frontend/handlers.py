# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import urllib
from pprint import pformat

from google.appengine.api import users
from webapp2_extras.appengine.users import login_required, admin_required
from .basehandlers import UserAwareHandler

from models import SCHEDULES
from models.account import Account
from models.miner import Miner
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
            'miners': Miner.list(ancestor=self.current_account.key),
            'schedules': SCHEDULES
        }
        self.render_response('miner/index.html', **template_vars)

    @login_required
    def view(self, mid):
        miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        self.render_response('miner/view.html', miner=miner, mid=mid,
                             schedules=SCHEDULES)

    def delete(self, mid):
        self.check_login()
        miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        miner.key.delete()
        return self.redirect_to('miner-index')

    @login_required
    def show_form(self, mid=None):
        if mid is None:
            miner = Miner(name='')
        else:
            miner = Miner.get_by_id(int(mid), parent=self.current_account.key)

        form = forms.MinerForm(self.request.POST, miner)
        self.render_response('miner/form2.html', form=form, mid=mid)

    def process_form(self, mid=None):
        if mid is None:
            miner = Miner(name='', parent=self.current_account.key)
        else:
            miner = Miner.get_by_id(int(mid), parent=self.current_account.key)

        form = forms.MinerForm(self.request.POST, miner)

        if form.validate():
            form.populate_obj(miner)
            key = miner.put()
            return self.redirect_to('miner-view', mid=key.id())

        self.render_response('miner/form2.html', form=form, mid=mid)
