""" A collection of helper functions for sanitizing text. """


def sanitize_prefix(prefix):
    """ Sanitizes a prefix to be used for TiKz coordinates. Allowed characters
    are lower case ASCII letters, digits and the hyphen.
    """
    import string as s
    allowed = s.ascii_lowercase + s.digits + '-'
    return ''.join(c for c in prefix.lower() if c in allowed)


def sanitize_for_latex(text):
    """ Sanitzes text for use within LaTeX. Escapes LaTeX special characters in
    order to prevent errors.
    """
    from functools import reduce
    escape = '%_&~'
    replacers = (lambda s: s.replace(e, r'\{}'.format(e)) for e in escape)
    return reduce(lambda s, f: f(s), replacers, text)

def sanitize_code(code):
    """ Remove unnecessary whitespace in code. """
    import re
    code = code.replace('( ', '(')).replace(' )', ')')
    code = re.replace(r'\s+', '', code)
    return code
