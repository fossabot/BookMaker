from mistune.scanner import escape_url
from mistune.inline_parser import ESCAPE
from mistune.scanner import escape, escape_html
from mistune.renderers import HTMLRenderer
import re

__all__ = ['plugin_my_extra']

PUNCTUATION = r'''\\!"#$%&'()*+,./:;<=>?@\[\]^`{}|_~-'''
ESCAPE_CHAR = re.compile(r'\\([' + PUNCTUATION + r'])')

# Implement underscore emphasis
# underscore_emphasis syntax looks like: '_word_'

# The pattern '__word__' is now reserved for Python "dunder" methods
# (and not specially handled so it appears literally in the HTML)
USCORE_PATTERN = (
    r'\b_(?=[^_])([\s\S]*?)_\b'
)

#: alternative image syntax::
#  I don't understand all the regex; all I want is an alternative
#  syntax to insert images inline with text, so just use # instead
#  of the normal ! introducer, and parse normal as 'image' in the
#  inline_parser and this as 'inline_image'.
#:
#: #[alt](/src)
INLINE_IMAGE_PATTERN = (
        r'#?\[([\s\S]*?)\]\(([A-Za-z0-9./_]+)\)')

def parse_uscore(self, m, state):
    text = m.group(1)
    return 'uscore', self.render(text, state)

def render_html_uscore(text):
    return '<u>' + text + '</u>'

def parse_inline_image(self, m, state):
    text = m.group(1)
    link = m.group(2)
    return 'inline_image', link, text

def render_inline_image(src, alt):
    s = '<img src="' + src + '" alt="' + alt + '" style="vertical-align:middle"'
    return s + ' />'

def plugin_my_extra(md):
    md.inline.register_rule(
        'uscore', USCORE_PATTERN, parse_uscore)
    md.inline.register_rule(
        'inline_image', INLINE_IMAGE_PATTERN, parse_inline_image)

    # allow for asterisk_emphasis only; subvert previous underscore_emphasis
    md.inline.rules.remove('underscore_emphasis')
    md.inline.rules.append('uscore')

    md.inline.rules.append('inline_image')

    if md.renderer.NAME == 'html':
        md.renderer.register('uscore', render_html_uscore)
        md.renderer.register('inline_image', render_inline_image)
