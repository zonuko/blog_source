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
STATIC_PATHS = ['images', 'pdfs', 'extra', 'extra/youtube.css']
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
THEME = "../themes/pelican-bootstrap3"
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['i18n_subsites', 'pelican_youtube', 'assets', 'better_codeblock_line_numbering', 'render_math', 'related_posts', 'tag_cloud', 'tipue_search', 'sitemap']

# PelicanのバージョンアップによってJinjaの拡張の書き方は以下のように変わったようだ
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n', 'webassets.ext.jinja2.AssetsExtension', 'jinja2.ext.with_']
}

# pelican-bootstrap3関係の設定
BOOTSTRAP_THEME = "simplex"
PYGMENTS_STYLE = "solarizeddark"
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
TWITTER_CARDS = True
# ADDTHIS_FACEBOOK_LIKE  = True
# ADDTHIS_TWEET          = True
ADDTHIS_GOOGLE_PLUSONE = False
ADDTHIS_DATA_TRACK_ADDRESSBAR = True
ADDTHIS_PROFILE  = "ra-58ea037a1776945e"
# BOOTSTRAP_FLUID = True
# カスタムCSS関係
CUSTOM_CSS = 'static/youtube.css'
EXTRA_PATH_METADATA = {
    'extra/youtube.css': {'path': 'static/youtube.css'}
}

SITEMAP = {
    'format': 'xml'
}

RELATED_POSTS_MAX = 10
RELATED_POSTS_SKIP_SAME_CATEGORY = True

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

DIRECT_TEMPLATES = ('index', 'categories', 'archives', 'search') #, 'tipue_search')
FEED_ALL_ATOM = 'feeds/all.atom.xml'

TAGS_URL           = 'tags'
TAGS_SAVE_AS       = 'tags/index.html'
AUTHORS_URL        = 'authors'
AUTHORS_SAVE_AS    = 'authors/index.html'
CATEGORIES_URL     = 'categories'
CATEGORIES_SAVE_AS = 'categories/index.html'
ARCHIVES_URL       = 'archives'
ARCHIVES_SAVE_AS   = 'archives/index.html'

# 色々パスの設定
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

MENUITEMS = (
    ('HOME', '/'),
    ('ATOM', '/feeds/all.atom.xml')
)
