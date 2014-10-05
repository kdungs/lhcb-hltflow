""" @file core.py
    Implement functionality to visualise an HLT streamer in a TiKz flowchart.

    @author: Kevin Dungs <kevin.dungs@cern.ch>
    @version: 1.0.0
    @date: 2014-10-05
"""


class Operation(object):
    """ @class Operation
        A helper class that is never instantiated. Only has static methods to
        check for different kinds of operations.
    """

    @staticmethod
    def is_cut(op):
        """
            @return whether an operation is a cut (i.e. starts with an opening
                    parenthesis)
        """
        return op.startswith('(')

    @staticmethod
    def is_sink(op):
        """
            @return whether an operation is a call to sink (i.e. starts with
                    the keyword SINK)
        """
        return op.startswith('SINK')

    @staticmethod
    def is_tee(op):
        """
            @return whether an operation is a call to tee
        """
        return op.startswith('tee')

    @staticmethod
    def is_op(op):
        """
            @return true if op does not show in flowchart
        """
        return not Operation.is_tee(op)


class StreamerFlowchart(object):
    """ @class StreamerFlowchart
        Implement the structure for a flowchart.
    """
    nodestring = r'\node [{style}] ({prefix}-{index}) {{{op}}};'
    linestring = r'\path [line] ({prefix}-{source}) -- ({prefix}-{target});'

    def __init__(self, name, code, prefix=None):
        """
            Initialise a new StreamerFlowchart object with given name and code
            block.

            @param name the streamer's name
            @param code the code block describing the streamer
            @param prefix an optional prefix used for naming TikZ coordinates
        """
        from .sanitize import sanitize_prefix
        self.name = name
        self.code = code
        self.prefix = sanitize_prefix(prefix or name)
        self._tikz = None

    @property
    def tikz(self):
        """
            Getter for the generated TikZ code representing the streamer.
            An internal variable is used to cache the value so the code is
            generated on demand and only once.

            @return TikZ code representing the streamer's flow
        """
        if self._tikz is None:
            self._tikz = self.generateTikz()
        return self._tikz

    def generateTikz(self):
        """
            Generate TikZ code for this streamer.
            This method is used internally and should (for performance reasons)
            not be called manually. Use the StreamerFlowchart.tikz property
            instead.

            @return generated TikZ code representing the streamer's flow
        """
        import re
        ops = re.split(r'\s*>>\s*', self.code)
        ops = (op.strip() for op in ops)
        ops = (op for op in ops if Operation.is_op(op))
        ops = [self._makeTikzNode(op, index) for index, op in enumerate(ops)]
        nop = len(ops)
        lines = [self._makeLine(a, b)
                 for a, b in zip(range(nop), range(1, nop))]
        return '\n'.join(ops + lines)

    def _makeTikzNode(self, op, index):
        """
            Transform a string defining an operation into a TiKz node. The
            given index is used to order the blocks in the diagram.

            @param op the string specifying the operation
            @param id a number to specify the order of the operation within the
                      flow
        """
        from .sanitize import sanitize_for_latex
        op = sanitize_for_latex(op)
        style = 'block'
        for name, checker in {
            'cut': Operation.is_cut,
            'sink': Operation.is_sink
        }.items():
            if checker(op):
                style += ', {}'.format(name)
        if index == 0:
            style = 'start'
        else:
            style += ', below=of {prefix}-{prev}'.format(prefix=self.prefix,
                                                         prev=index - 1)
        return self.nodestring.format(style=style, prefix=self.prefix,
                                      index=index, op=op)

    def _makeLine(self, source, target):
        """
            Build a line between two given coordinates.

            @param source index of the start of the line
            @param target index of the line's end
        """
        return self.linestring.format(prefix=self.prefix, source=source,
                                      target=target)
