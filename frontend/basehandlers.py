from __future__ import absolute_import
import urllib

from google.appengine.api import users

import webapp2
from webapp2_extras import jinja2

from models.account import Account


class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests all other handlers will
        extend this handler

    """
    def __init__(self, request, response):
        self.initialize(request, response)
        self.jinja2_context = {}

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        ctx = self.jinja2_context.copy()
        ctx.update(context)
        rv = self.jinja2.render_template(_template, **ctx)
        self.response.write(rv)

    def render_response_string(self, template_string, **context):
        ctx = self.jinja2_context.copy()
        ctx.update(context)
        self.response.write(self.jinja2.environment.from_string(
            template_string).render(**ctx))


def login_required(handler):
    """Requires that a user be logged in to access the resource"""
    def check_login(self, *args, **kwargs):
        if self.current_account:
            return handler(self, *args, **kwargs)
        elif self.current_user:     # We've got user but no account
            next = urllib.quote_plus(self.request.uri)
            return self.redirect_to('account-edit', next=next)
        else:
            return self.redirect(users.create_login_url(self.request.uri))

    return check_login


def admin_required(handler):
    """Requires that a current user is app administrator"""
    def check_admin(self, *args, **kwargs):
        if self.current_user and users.is_current_user_admin():
            return handler(self, *args, **kwargs)
        else:
            self.abort(403)

    return check_admin


class UserAwareHandler(BaseHandler):
    def __init__(self, request, response):
        super(UserAwareHandler, self).__init__(request, response)
        self.jinja2_context.update({
            'user': self.current_user,
            'account': self.current_account,
            'is_admin': users.is_current_user_admin(),
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url(webapp2.uri_for('home'))
        })

    @webapp2.cached_property
    def current_user(self):
        return users.get_current_user()

    @webapp2.cached_property
    def current_account(self):
        if self.current_user:
            return Account.get_by_id(self.current_user.user_id())
        else:
            return None
