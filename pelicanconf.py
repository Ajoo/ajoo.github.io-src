#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Ajoo'
SITENAME = 'Wintermute Dev Logs'
SITEURL = ''
GITHUB_URL = 'https://github.com/Ajoo/ajoo.github.io-src'

TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'English'

PATH = 'content'

DEFAULT_CATEGORY = 'General'
TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('kaggle', 'https://www.kaggle.com'),
         ('Python.org', 'http://python.org/'),
         ('Pelican', 'http://getpelican.com/'),)

# Social widget
SOCIAL = (('email', 'mailto:ajoo@outlook.pt'),
		  ('github', 'https://github.com/Ajoo'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
