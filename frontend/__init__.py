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
    # Account routes
    PathPrefixRoute('/account', [
        RedirectRoute('/', 'frontend.handlers.AccountHandler:view',
                      'account-view'),
        RedirectRoute('/edit', 'frontend.handlers.AccountHandler:edit',
                      'account-edit', methods=['GET']),
        RedirectRoute('/edit', 'frontend.handlers.AccountHandler:save',
                      'account-edit', methods=['POST']),
        RedirectRoute('/create', 'frontend.handlers.AccountHandler:regform',
                      'account-create', methods=['GET']),
        RedirectRoute('/create', 'frontend.handlers.AccountHandler:create',
                      'account-create', methods=['POST'])
    ]),

    PathPrefixRoute('/miner', [
        RedirectRoute('/', 'frontend.handlers.MinerHandler:index',
                      'miner-index', methods=['GET']),
        RedirectRoute('/<mid:\d+>', 'frontend.handlers.MinerHandler:view',
                      'miner-view', methods=['GET']),
        RedirectRoute('/<mid:\d+>/edit',
                      'frontend.handlers.MinerHandler:show_form',
                      'miner-edit', methods=['GET']),
        RedirectRoute('/<mid:\d+>/edit',
                      'frontend.handlers.MinerHandler:process_form',
                      'miner-edit', methods=['POST']),
        RedirectRoute('/create', 'frontend.handlers.MinerHandler:show_form',
                      'miner-create', methods=['GET'], defaults={'mid': None}),
        RedirectRoute('/save', 'frontend.handlers.MinerHandler:process_form',
                      'miner-save', methods=['POST'], defaults={'mid': None}),
        RedirectRoute('/<mid:\d+>/delete',
                      'frontend.handlers.MinerHandler:delete',
                      'miner-delete'),
        RedirectRoute('/<mid:\d+>/run',
                      'frontend.handlers.MinerHandler:run',
                      'miner-run'),
        RedirectRoute('/<mid:\d+>/crawl/<cid:\d+>',
                      'frontend.handlers.MinerHandler:view_crawl',
                      'miner-view-crawl')
    ]),
]


application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
