"""
Implement functionality to visualise an HLT streamer in a TiKz flowchart.

@author: Kevin Dungs <kevin.dungs@cern.ch>
@version: 0.1.0
@date: 2014-09-06
"""

class Operation:
    """ @class Operation
    A helper class that is never instantiated. Only has static methods to check
    for different kinds of operations.
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
        @return whether an operation is a call to sink (i.e. starts with the
                keyword SINK)
        """
        return op.startswith('SINK')

    @staticmethod
    def is_tee(op):
        """
        @return whether an operation is a call to tee
        """
        return op.startswith('tee')


class StreamerFlowchart:
    """ @class StreamerFlowchart
    Implement the structure for a flowchart.
    """
    nodestring = r'\node [{style}] ({prefix}-{index}) {{{op}}};'
    linestring = r'\path [line] ({prefix}-{source}) -- ({prefix}-{target});'

    def __init__(self, name, code, prefix=None, properties=None):
        """
        Constructor.

        @param name the streamer's name
        @param code the code specified in the streamer
        @param prefix the prefix used in the TiKz code; if None it defaults to
                      a sanitized version of name
        @param properties dictionary of properties used for formatting the
                          numerical constants in the code; if None defaults to
                          empty dictionary
        """
        from Sanitize import sanitize_prefix
        self.name = name
        self.code = code
        self.prefix = sanitize_prefix(prefix or name)
        self.properties = properties or {}
        self._tikz = None
    
    @property
    def tikz(self):
        """
        @return the generated TiKz code for this streamer; the TiKz code is
                generated on demand and then cached for future reference
        """
        if self._tikz is None:
            self._tikz = self.generateTikz()
        return self._tikz

    def generateTikz(self):
        """
        """
        operations = [self._makeTikzNode(op, index)
                      for index, op in enumerate(self.code.split('\n'))]
        operations = [op for op in operations if op]  # filter out empty strings
        nop = len(operations)
        lines = [self._makeLine(a, b)
                 for a, b in zip(range(nop), range(1, nop))]
        return '\n'.join(operations + lines)

    def _makeTikzNode(self, op, index):
        """
        Transform a string defining an operation into a TiKz node. The given
        index is used to order the blocks in the diagram.

        @param op the string specifying the operation
        @param id a number to specify the order of the operation within the flow
        """
        from Sanitize import sanitize_for_latex
        op = sanitize_for_latex(op.strip('> '))
        if Operation.is_tee(op):
            return ''
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
        """
        return self.linestring.format(prefix=self.prefix, source=source,
                                      target=target)
