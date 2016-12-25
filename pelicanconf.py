#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'zonuko'
SITENAME = 'ぞぬこBLOG'
SITEURL = 'https://zonuko.github.io'
SITESUBTITLE = "黒魔術師になりたいブログ"
DESCRIPTION = "好きな趣味とか技術とかを書き散らすブログ"
PATH = 'content/categorys'

# Favicon Settings
FAVICON = 'favicon.ico'
FAVICON_TYPE = 'image/vnd.microsoft.icon'
STATIC_PATHS = ['images', 'pdfs', 'extra']
EXTRA_PATH_METADATA = {
    'extra/' + FAVICON: {'path': FAVICON},
}

GOOGLE_ANALYTICS = 'UA-89443473-1'

TIMEZONE = 'Asia/Tokyo'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'ja': '%Y-%m-%d(%a)',
}

DEFAULT_LANG = 'ja'
THEME = "../themes/pelican-mg"
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'render_math', 'related_posts', 'tag_cloud', 'tipue_search', 'sitemap']
JINJA_EXTENSIONS = ['webassets.ext.jinja2.AssetsExtension', 'jinja2.ext.with_']

SITEMAP = {
    'format': 'xml'
}

# Plugins setting
RELATED_POSTS_MAX = 10
RELATED_POSTS_SKIP_SAME_CATEGORY = True

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

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
FEED_ALL_ATOM = 'feeds/all.atom.xml'
SHARE = True
TWITTER_USERNAME = 'nuhera'

# 色々パスの設定
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
