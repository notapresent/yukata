from __future__ import absolute_import
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.appengine.users import login_required, admin_required   # TODO use this


class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests all other handlers will
        extend this handler
    """
    def __init__(self, request, response):
        self.initialize(request, response)
        self.jinja2_context = {
            'request': self.request,
            'getattr': getattr
        }

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


class UserAwareHandler(BaseHandler):
    def __init__(self, request, response):
        super(UserAwareHandler, self).__init__(request, response)
        self.login_url = users.create_login_url(self.request.uri)
        self.logout_url = users.create_logout_url(webapp2.uri_for('home'))
        self.is_admin = users.is_current_user_admin()
        self.jinja2_context.update({
            'user': self.current_user,
            'is_admin': self.is_admin,
            'login_url': self.login_url,
            'logout_url': self.logout_url
        })

    @webapp2.cached_property
    def current_user(self):
        user = users.get_current_user()
        if user:
            user.key = ndb.Key('User', user.user_id())
        return user

    def check_login(self):
        if not self.current_user:
            return self.redirect(self.login_url, abort=True)

    def check_admin(self):
        if not self.current_user:
            return self.redirect(self.login_url, abort=True)

        if not self.is_admin:
            self.abort(403, detail='You need admin privileges to access this')
