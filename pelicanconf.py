#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)

from themeconf import *

AUTHOR = 'Ajoo'
SITENAME = 'Wintermute Dev Logs'
SITEURL = ''
#GITHUB_URL = 'https://github.com/Ajoo/ajoo.github.io-src'

TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'English'

PATH = 'content'

DEFAULT_CATEGORY = 'General'
STATIC_PATHS = ['images', 'audio']
TYPOGRIFY = True
PLUGIN_PATHS = ['plugins']
PLUGINS = ['render_math', 'liquid_tags.img', 'liquid_tags.fig', 'liquid_tags.audio', 'liquid_tags.include_code']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (('email', 'mailto:ajoo@outlook.pt'),
		  ('kaggle', 'https://www.kaggle.com/ajoo88'))

# Social widget
SOCIAL = (('github', 'https://github.com/Ajoo'),)
		  

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
