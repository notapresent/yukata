# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from webapp2 import WSGIApplication, Route, uri_for
from webapp2_extras.routes import PathPrefixRoute

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
        'globals': {'uri_for': uri_for}
    },
}

routes = [
    # Home page
    Route('/', 'frontend.handlers.MainHandler:home', 'home'),

    # Admin pages
    PathPrefixRoute('/admin', [
        Route('/', 'frontend.handlers.AdminHandler:index',
              'admin-index'),

        Route('/env', 'frontend.handlers.AdminHandler:env',
              'admin-env'),
    ]),

    # Robot pages
    PathPrefixRoute('/robot', [
        Route('/', 'frontend.handlers.RobotHandler:index',
              'robot-index', methods=['GET']),
        Route('/<mid:\d+>', 'frontend.handlers.RobotHandler:view',
              'robot-view', methods=['GET']),
        Route('/create', 'frontend.handlers.RobotHandler:show_form',
              'robot-create', methods=['GET'], defaults={'mid': None}),
        Route('/save', 'frontend.handlers.RobotHandler:process_form',
              'robot-save', methods=['POST'], defaults={'mid': None}),
        Route('/<mid:\d+>/edit',
              'frontend.handlers.RobotHandler:show_form',
              'robot-edit', methods=['GET']),
        Route('/<mid:\d+>/edit',
              'frontend.handlers.RobotHandler:process_form',
              'robot-edit', methods=['POST']),
        Route('/<mid:\d+>/delete',
              'frontend.handlers.RobotHandler:delete',
              'robot-delete'),
        Route('/<mid:\d+>/run',
              'frontend.handlers.RobotHandler:run',
              'robot-run'),

        # DataSet pages
        PathPrefixRoute('/<mid:\d+>/dataset', [
            Route('/create',
                  'frontend.handlers.DataSetHandler:show_form',
                  'dataset-create', methods=['GET'], defaults={'dsid': None}),
            Route('/save',
                  'frontend.handlers.DataSetHandler:process_form',
                  'dataset-save', methods=['POST'], defaults={'dsid': None}),

            Route('/edit/<dsid:\d+>',
                  'frontend.handlers.DataSetHandler:show_form',
                  'dataset-edit', methods=['GET']),
            Route('/edit/<dsid:\d+>',
                  'frontend.handlers.DataSetHandler:process_form',
                  'dataset-edit', methods=['POST']),
            Route('/delete/<dsid:\d+>',
                  'frontend.handlers.DataSetHandler:delete',
                  'dataset-delete', methods=['POST']),
        ]),
        Route('/<mid:\d+>/crawl/<cid:\d+>',
              'frontend.handlers.RobotHandler:view_crawl',
              'robot-view-crawl'),

        Route('/job/<jid:\d+>',
              'frontend.handlers.RobotHandler:view_job',
              'robot-view-job')
    ]),
]

application = WSGIApplication(routes, debug=DEBUG, config=config)
