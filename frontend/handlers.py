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
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))

        form = forms.AccountForm(obj=self.current_account)
        context = {
            'form': form,
            'create': False
        }
        self.render_response('account/form.html', **context)

    def save(self):
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))
        
        form = forms.AccountForm(self.request.POST)
        if form.validate():
            acc = Account.get_by_id(self.current_user.user_id())
            acc.populate(display_name=form.display_name.data)
            acc.put()
            self.redirect_to('account-view')

        self.render_response('account/form.html', form=form, create=False)

    def register(self):
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))

        account = Account(display_name=self.current_user.nickname())
        context = {
            'form': forms.AccountRegisterForm(obj=account),
            'next': urllib.unquote_plus(self.request.get('next')),
            'create': True
        }
        self.render_response('account/form.html', **context)

    def create(self):
        form = forms.AccountRegisterForm(self.request.POST)
        next_url = self.request.get('next') or self.uri_for('home')
        if form.validate():
            acc = Account(id=self.current_user.user_id())
            acc.populate(display_name=form.display_name.data)
            acc.put()
            return self.redirect(next_url, abort=True)
        else:
            raise ValueError(form.errors)

        context = {'form': form, 'create': True, 'next': next_url }
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

    @login_required
    def edit(self, mid):
        miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        self.render_response('miner/form.html', miner=miner,
                             schedules=SCHEDULES)

    @login_required
    def create(self):
        # Show form
        if self.request.method == 'GET':
            miner = Miner(parent=self.current_account.key)
            self.render_response('miner/form.html', miner=miner,
                                 schedules=SCHEDULES)

    def save(self):
        self.check_login()

        mid = self.request.get('id')
        if mid:
            miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        else:
            miner = Miner(parent=self.current_account.key)

        miner.populate(
            name=self.request.get('name'),
            schedule=self.request.get('schedule'),
        )
        key = miner.put()
        return self.redirect_to('miner-view', mid=key.id())

    def delete(self, mid):
        self.check_login()
        miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        miner.key.delete()
        return self.redirect_to('miner-index')
