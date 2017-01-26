"""
Figure Tag
---------
This implements a Liquid-style figure tag for Pelican

Syntax
------
{% fig [class name(s)] [http[s]:/]/path/to/image [width [height]] [caption | "caption" ["legend"]] %}
"""
import re
from .mdx_liquid_tags import LiquidTags
import six

SYNTAX = '{% fig [class name(s)] [http[s]:/]/path/to/image [width [height]] [caption | "caption" ["legend"]] %}'

# Regular expression to match the entire syntax
ReFig = re.compile("""(?P<class>\S.*\s+)?(?P<src>(?:https?:\/\/|\/|\S+\/)\S+)(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?\s+(?P<quote>"|')(?P<alt>[^"']+)?(?P=quote)(?:\s+(?P=quote)(?P<caption>[^"']+)?(?P=quote)(?:\s+(?P=quote)(?P<legend>[^"']+)?(?P=quote))?)?\s*""")

@LiquidTags.register('fig')
def fig(preprocessor, tag, markup):
    attrs = None
    
    # Parse the markup string
    match = ReFig.search(markup)
    if match:
        attrs = dict([(key, val.strip())
                      for (key, val) in six.iteritems(match.groupdict()) if val])
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))
    
    print(attrs)
    html = '</div>\n'
    attrs.pop('quote')
    if 'legend' in attrs: html = '\t<div class="legend">{legend}</div>\n'.format(legend=attrs.pop('legend')) + html
    if 'caption' in attrs: html = '\t<p class="caption">{caption}</p>\n'.format(caption=attrs.pop('caption')) + html

    cls = 'figure'
    if 'class' in attrs: cls += ' ' + attrs.pop('class')
    
    html = '\t<img {0}>\n'.format(' '.join('{0}="{1}"'.format(key, val) for (key, val) in six.iteritems(attrs))) + html
    
    html = '\n<div class="{cls}">\n'''.format(cls=cls) + html
    
    print(html)
    return html
    
ReSourcedFig = re.compile("""(?P<class>\S.*\s+)?(?P<src>(?:https?:\/\/|\/|\S+\/)\S+)(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?\s+(?P<quote>"|')(?P<alt>[^"']+)?(?P=quote)(?:\s+(?P=quote)(?P<caption>[^"']+)?(?P=quote)(?:\s+(?P<ref>(?:https?:\/\/|\/|\S+\/)\S+))?)?\s*""")

    
@LiquidTags.register('sourced_fig')
def sourced_fig(preprocessor, tag, markup):
    attrs = None
    
    # Parse the markup string
    match = ReSourcedFig.search(markup)
    if match:
        attrs = dict([(key, val.strip())
                      for (key, val) in six.iteritems(match.groupdict()) if val])
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))
    
    print(attrs)
    attrs.pop('quote')
    
    caption = attrs.pop('caption', '')
    if 'ref' in attrs:
        caption += ' Image <a href={ref} >source</a>'.format(ref=attrs.pop('ref'))
    html = '\t<p class="caption">{caption}</p>\n</div>\n'.format(caption=caption)

    cls = 'figure'
    if 'class' in attrs: cls += ' ' + attrs.pop('class')
    
    html = '\t<img {0}>\n'.format(' '.join('{0}="{1}"'.format(key, val) for (key, val) in six.iteritems(attrs))) + html
    
    html = '\n<div class="{cls}">\n'''.format(cls=cls) + html
    
    print(html)
    return html
#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register

