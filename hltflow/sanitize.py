""" @file sanitize.py
    A collection of helper functions for sanitizing text.

    @author: Kevin Dungs <kevin.dungs@cern.ch>
    @version: 0.1.0
    @date: 2014-09-06
"""


def sanitize_prefix(prefix):
    """
        Sanitizes a prefix to be used for TiKz coordinates.
        Allowed characters are lower case ASCII letters, digits and the hyphen.

        @param prefix the prefix to be sanitized
        @return the sanitized prefix string
    """
    import string as s
    allowed = s.ascii_lowercase + s.digits + '-'
    return ''.join(c for c in prefix.lower() if c in allowed)


def sanitize_for_latex(text):
    """
        Sanitze text for use within LaTeX.
        Espace LaTeX special characters in order to prevent errors.

        @param text the text to be sanitized
        @return text with special characters escaped
    """
    from functools import reduce
    escape = '%_&~'
    replacers = (lambda s: s.replace(e, r'\{}'.format(e)) for e in escape)
    return reduce(lambda s, f: f(s), replacers, text)
