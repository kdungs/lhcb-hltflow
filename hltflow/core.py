""" Implement functionality to visualise an HLT streamer in a TiKz flowchart.
"""

from enum import (
    Enum,
    unique
)

@unique
class Operation(Enum):
    NOOP = (None, None)
    OP = ('block, op', 'Op')
    SOURCE = ('block, source', 'Source')
    CUT = ('block, cut', 'Cut')
    SINK = ('block, sink', 'Sink')

    def __init__(self, style, color):
        self.style = style
        self.color = color

    @staticmethod
    def is_cut(opstr):
        """ Checks whether an operation is a cut (i.e. starts with an opening
        parenthesis).
        """
        return opstr.startswith('(')

    @staticmethod
    def is_sink(opstr):
        """ Checks whether an operation is a call to sink (i.e. starts with the
        keyword SINK).
        """
        return opstr.startswith('SINK')

    @staticmethod
    def is_tee(opstr):
        """ Check whether an operation is a call to tee. """
        return opstr.startswith('tee')

    @staticmethod
    def is_op(opstr):
        """ Checks whether opstr is supposed to show up in the flowchart. """
        return not Operation.is_tee(opstr) and not opstr == '~TC_EMPTY'

    @staticmethod
    def parse_op(opstr):
        if not Operation.is_op(opstr):
            return Operation.NOOP
        if Operation.is_cut(opstr):
            return Operation.CUT
        if Operation.is_sink(opstr):
            return Operation.SINK
        return Operation.OP


class StreamerFlowchart(object):
    """ Implement the structure for a flowchart. """
    nodestring = r'\node [{style}] ({prefix}-{index}) {{{opstr}}};'
    connectstring = r'\connect{{{prefix}-{source}}}{{{prefix}-{target}}}{{{sourcecolor}}}{{{targetcolor}}}'

    def __init__(self, name, code, prefix=None):
        """ Initialises a new StreamerFlowchart object with given name and code
        block. An optional prefix can be supplied otherwise a sanitized version
        of name is used.
        """
        from .sanitize import sanitize_prefix
        self.name = name
        self.code = code
        self.prefix = sanitize_prefix(prefix or name)
        self._tikz = None

    @property
    def tikz(self):
        """ Getter for the generated TikZ code representing the streamer.

            An internal variable is used to cache the value so the code is
            generated on demand and only once.
        """
        if self._tikz is None:
            self._tikz = self.generateTikz()
        return self._tikz

    def generateTikz(self):
        """ Generates TikZ code for this streamer.

            This method is used internally and should (for performance reasons)
            not be called manually. Use the StreamerFlowchart.tikz property
            instead.
        """
        import re
        ops = re.split(r'\s*>>\s*', self.code)
        ops = (opstr.strip() for opstr in ops)
        ops = ((opstr, Operation.parse_op(opstr)) for opstr in ops)
        ops = ((opstr, op) for (opstr, op) in ops if op is not Operation.NOOP)
        ops = [(index, opstr, op) for index, (opstr, op) in enumerate(ops)]
        ops[0] = (ops[0][0], ops[0][1], Operation.SOURCE)
        nodes = [self._makeTikzNode(index, opstr, op)
                 for index, opstr, op in ops]
        connects = [self._connect(a, b)
                    for a, b in zip(ops, ops[1:])]
        return '\n'.join(nodes + connects)

    def _makeTikzNode(self, index, opstr, op):
        """ Transforms a string defining an operation into a TiKz node. The
        given index is used to order the blocks in the diagram.
        """
        from .sanitize import sanitize_for_latex
        opstr = sanitize_for_latex(opstr)
        style = op.style
        if op is not Operation.SOURCE:
            style += ', below=of {}-{}'.format(self.prefix, index - 1)
        return self.nodestring.format(style=style, prefix=self.prefix,
                                      index=index, opstr=opstr)

    def _connect(self, source, target):
        """ Builds a connection between two given operations. """
        sindex, _, sop = source
        tindex, _, top = target
        return self.connectstring.format(
            prefix=self.prefix,
            source=sindex,
            target=tindex,
            sourcecolor=sop.color,
            targetcolor=top.color
        )
