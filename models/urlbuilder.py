# -*- coding: utf-8 -*-


def make_urls(urlsource, *args, **kwargs):
    if urlsource.kind == 'single':
        return urlsource.url
    raise NotImplementedError
