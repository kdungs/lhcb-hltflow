"""
    Add functionality to make LaTeX figures from the raw TikZ code produced by
    core.StreamerFlowchart.

    @author: Kevin Dungs <kevin.dungs@cern.ch>
    @version: 1.0.0
    @date: 2014-10-05
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
    """
        Indent a given multi line string by a given number of spaces.
        This is used to produce properly formatted LaTeX documents.

        @param spaces number of spaces prepended to every line
        @param multilinestring the string to indent
        @return multilinestring with each line indented by spaces spaces
    """
    indentation = ' ' * spaces
    return '\n{}'.format(indentation).join(multilinestring.split('\n'))


def make_figure(sf, tikzoptions='node distance=.75cm and 2.75cm'):
    """
        Generate a LaTeX figure from a given hltflow.core.StreamerFlowchart.

        @param sf the hltflow.core.StreamerFlowchart
        @param tikzoptions options for the tikzdocument
        @return string of a LaTeX figure containing the flowchart
    """
    from .core import StreamerFlowchart
    assert type(sf) is StreamerFlowchart
    return FIGURE.format(tikz=indent(4, sf.tikz), name=sf.name,
                         tikzoptions=tikzoptions)


def make_document(figures):
    """
        Generate a LaTeX document from a given list of figures produced by
        hltflow.latex.make_figure.

        @param figures a list of strings containing LaTeX figures
        @return a string containing a LaTeX document
    """
    return DOCUMENT.format(figures='\n\n'.join(figures))
