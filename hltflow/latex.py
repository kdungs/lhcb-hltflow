""" Adds functionality to make LaTeX figures from the raw TikZ code produced by
core.StreamerFlowchart.
"""


FIGURE = r'''\begin{{figure}}
  \centering
  \begin{{tikzpicture}}[{tikzoptions}]
    {tikz}
  \end{{tikzpicture}}
  \caption{{Flowchart of {name}}}
\end{{figure}}'''

DOCUMENT = r'''\documentclass{{scrartcl}}

\usepackage{{fontspec}}
\usepackage{{tikz}}
  \usetikzlibrary{{shapes, arrows, positioning}}
\usepackage{{xcolor}}

\input{{colors}}
\input{{tikzstyles}}

\begin{{document}}

{figures}

\end{{document}}
'''


def indent(spaces, multilinestring):
    """ Indents a given multilinestring by a given number of spaces. This is
    used to produce properly formatted LaTeX documents.
    """
    indentation = ' ' * spaces
    return '\n{}'.format(indentation).join(multilinestring.split('\n'))


def make_figure(sf, tikzoptions='node distance=.75cm and 2.75cm'):
    """ Generates a LaTeX figure from a given hltflow.core.StreamerFlowchart.
    Additionally, tikzoptions can be supplied manually.
    """
    from .core import StreamerFlowchart
    assert type(sf) is StreamerFlowchart
    return FIGURE.format(tikz=indent(4, sf.tikz), name=sf.name,
                         tikzoptions=tikzoptions)


def make_document(figures):
    """ Generates a LaTeX document from a given list of figures produced by
        hltflow.latex.make_figure.
    """
    return DOCUMENT.format(figures='\n\n'.join(figures))
