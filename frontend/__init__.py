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
    RedirectRoute('/env', 'frontend.handlers.MainHandler:env', 'env'),

    PathPrefixRoute('/account', [
        RedirectRoute('/', 'frontend.handlers.AccountHandler:view',
                      'account-view'),
        RedirectRoute('/edit', 'frontend.handlers.AccountHandler:edit',
                      'account-edit')
    ]),
    PathPrefixRoute('/miner', [
        RedirectRoute('/', 'frontend.handlers.MinerHandler:index',
                      'miner-index'),
        RedirectRoute('/<mid:\d+>', 'frontend.handlers.MinerHandler:view',
                      'miner-view'),
        RedirectRoute('/create', 'frontend.handlers.MinerHandler:create',
                      'miner-create'),
        RedirectRoute('/edit/<mid:\d+>', 'frontend.handlers.MinerHandler:edit',
                      'miner-edit'),
    ]),
]


application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
