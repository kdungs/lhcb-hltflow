def sanitize_prefix(p):
    import string
    return p.lower().translate(None, string.whitespace + string.punctuation)

def latex_sanitise(s):
    from functools import reduce
    escape = '%_&~'
    replacers = (lambda s: s.replace(e, '\{}'.format(e)) for e in escape)
    return reduce(lambda s, f: f(s), replacers, s)
