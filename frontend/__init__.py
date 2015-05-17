# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import webapp2
from webapp2_extras.routes import PathPrefixRoute, RedirectRoute

import frontend.filters as filters

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

config = {
    'webapp2_extras.jinja2': {
        'template_path': 'templates',
        'filters': {
            'timesince': filters.timesince,
            'datetimeformat': filters.datetimeformat,
            'urlencode': filters.urlencode_filter
        },
        'globals': {'uri_for': webapp2.uri_for}
    },
}

routes = [
    # Frontend routes
    RedirectRoute('/', 'frontend.handlers.MainHandler:home', 'home'),

    PathPrefixRoute('/admin', [
        RedirectRoute('/', 'frontend.handlers.AdminHandler:index',
                      'admin-index'),

        RedirectRoute('/env', 'frontend.handlers.AdminHandler:env',
                      'admin-env'),
    ]),

    PathPrefixRoute('/robot', [
        RedirectRoute('/', 'frontend.handlers.RobotHandler:index',
                      'robot-index', methods=['GET']),
        RedirectRoute('/<mid:\d+>', 'frontend.handlers.RobotHandler:view',
                      'robot-view', methods=['GET']),
        RedirectRoute('/<mid:\d+>/edit',
                      'frontend.handlers.RobotHandler:show_form',
                      'robot-edit', methods=['GET']),
        RedirectRoute('/<mid:\d+>/edit',
                      'frontend.handlers.RobotHandler:process_form',
                      'robot-edit', methods=['POST']),
        RedirectRoute('/create', 'frontend.handlers.RobotHandler:show_form',
                      'robot-create', methods=['GET'], defaults={'mid': None}),
        RedirectRoute('/save', 'frontend.handlers.RobotHandler:process_form',
                      'robot-save', methods=['POST'], defaults={'mid': None}),
        RedirectRoute('/<mid:\d+>/delete',
                      'frontend.handlers.RobotHandler:delete',
                      'robot-delete'),
        RedirectRoute('/<mid:\d+>/run',
                      'frontend.handlers.RobotHandler:run',
                      'robot-run'),
        RedirectRoute('/<mid:\d+>/crawl/<cid:\d+>',
                      'frontend.handlers.RobotHandler:view_crawl',
                      'robot-view-crawl'),
        RedirectRoute('/<mid:\d+>/edit-datasets',
                      'frontend.handlers.RobotHandler:show_datasets_form',
                      'robot-datasets-form', methods=['GET']),
        RedirectRoute('/<mid:\d+>/edit-datasets',
                      'frontend.handlers.RobotHandler:process_datasets_form',
                      'robot-datasets-save', methods=['POST']),
        RedirectRoute('/job/<jid:\d+>',
                      'frontend.handlers.RobotHandler:view_job',
                      'robot-view-job')
    ]),
]

application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
