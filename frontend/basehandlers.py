from __future__ import absolute_import
from google.appengine.ext import ndb
from google.appengine.api import users

import webapp2
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):
    """
        All other handlers will extend this handler
    """

    def __init__(self, request, response):
        self.initialize(request, response)
        self.is_admin = users.is_current_user_admin()
        self.login_url = users.create_login_url(self.request.uri)
        self.logout_url = users.create_logout_url(webapp2.uri_for('home'))

        self.jinja2_context = {
            'request': self.request,
            'user': self.current_user,
            'is_admin': self.is_admin,
            'login_url': self.login_url,
            'logout_url': self.logout_url
        }

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    @webapp2.cached_property
    def current_user(self):
        user = users.get_current_user()
        if user:
            user.key = ndb.Key('User', user.user_id())
        return user

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


class UserHandler(BaseHandler):
    def dispatch(self):
        if not self.current_user:
            return self.redirect(self.login_url)

        return super(UserHandler, self).dispatch()


class AdminHandler(BaseHandler):
    def dispatch(self):
        if not self.current_user:
            return self.redirect(self.login_url)

        if not self.is_admin:
            self.abort(403, detail="You need admin privileges to access this URL.")

        super(AdminHandler, self).dispatch()
