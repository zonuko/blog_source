#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'zonuko'
SITENAME = 'zonuko blog'
SITEURL = ''
SITESUBTITLE = "test"
PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'
THEME = "../themes/bootstrap"
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'render_math']
JINJA_EXTENSIONS = ['webassets.ext.jinja2.AssetsExtension', 'jinja2.ext.with_']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/zonuko'),
    ('Bitbucket', 'https://bitbucket.org/y_fujiwara/'),
    ('Twitter', 'https://twitter.com/nuhera'),
    ('Twitter', 'https://twitter.com/zonuko'),
)
# DISQUS_SITENAME = 'zonuko-github-io'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
