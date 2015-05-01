# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import urllib
from pprint import pformat

from google.appengine.api import users

from .basehandlers import UserAwareHandler, login_required, admin_required

from models import SCHEDULES
from models.account import Account
from models.miner import Miner


class MainHandler(UserAwareHandler):
    def home(self):
        self.render_response('welcome.html')

    @admin_required
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
        # acc = Account(id=self.current_user.user_id())

    def edit(self):
        if not self.current_user:
            return self.redirect(users.create_login_url(self.request.uri))

        if self.request.method == 'GET':
            acc = self.current_account
            next = urllib.unquote_plus(self.request.get('next'))
            self.render_response('account/form.html', account=acc, next=next)

        elif self.request.method == 'POST':
            acc_id = self.request.get('id')
            if acc_id:
                acc = Account.get_by_id(acc_id)
            else:
                acc = Account(id=self.current_user.user_id())
            # acc.populate()
            acc.put()

            next = self.request.get('next')
            if next:
                return self.redirect(str(next))
            else:
                return self.redirect_to('account-view')


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
    def create(self):
        miner = Miner(parent=self.current_account.key)
        miner.put()
        self.render_response('miner/form.html', miner=miner,
                             schedules=SCHEDULES)

    @login_required
    def form(self, mid):
        if mid:
            miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        else:
            miner = Miner()
        self.render_response('miner/form.html', miner=miner,
                             schedules=SCHEDULES)
    @login_required
    def save(self):
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

    @login_required
    def delete(self, mid):
        miner = Miner.get_by_id(int(mid), parent=self.current_account.key)
        miner.key.delete()
        return self.redirect_to('miner-index')
