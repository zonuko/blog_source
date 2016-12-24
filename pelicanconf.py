#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'zonuko'
SITENAME = 'zonuko blog'
SITEURL = 'https://zonuko.github.io'
SITESUBTITLE = "好きな趣味とか技術とかを書き散らす予定"
DESCRIPTION = "test"
PATH = 'content'
FAVICON = 'favicon.ico'
FAVICON_TYPE = 'image/vnd.microsoft.icon'

TIMEZONE = 'Asia/Tokyo'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ja': '%Y-%m-%d(%a)',
}

DEFAULT_LANG = 'ja'
THEME = "../themes/pelican-mg"
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'render_math', 'related_posts', 'tag_cloud']
JINJA_EXTENSIONS = ['webassets.ext.jinja2.AssetsExtension', 'jinja2.ext.with_']

# Plugins setting
RELATED_POSTS_MAX = 10
RELATED_POSTS_SKIP_SAME_CATEGORY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('github', 'https://github.com/zonuko'),
    ('bitbucket', 'https://bitbucket.org/y_fujiwara/'),
    ('twitter', 'https://twitter.com/nuhera'),
    ('twitter', 'https://twitter.com/zonuko'),
)

DISQUS_SITENAME = 'zonuko-blog'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
DIRECT_TEMPLATES = ('index', 'categories', 'archives', 'search', 'tipue_search')
TIPUE_SEARCH_SAVE_AS = 'tipue_search.json'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
SHARE = True
TWITTER_USERNAME = 'nuhera'
