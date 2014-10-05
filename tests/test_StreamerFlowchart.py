import unittest

from hltflow.core import StreamerFlowchart


class TestStreamerFlowchartDefaults(unittest.TestCase):
    def setUp(self):
        """
            Instantiate a test fixture.
        """
        self.sf = StreamerFlowchart('Test % 1', 'SomeCode >> SomeMoreCode')

    def testPrefix(self):
        """
            If no prefix is specified, it defaults to a lowercase stripped
            version of the name.
        """
        self.assertEqual(self.sf.prefix, 'test1')

    def testMakeTikzNode(self):
        """
            Test all (intended) cases of StreamerFlowchart._makeTikzNode.
        """
        # Start
        self.assertEqual(
            r'\node [start] (test1-0) {Start};',
            self.sf._makeTikzNode('Start', 0)
        )
        # Tool
        self.assertEqual(
            r'\node [block, below=of test1-0] (test1-1) {Something};',
            self.sf._makeTikzNode('Something', 1)
        )
        # Cut
        self.assertEqual(
            r'\node [block, cut, below=of test1-1] (test1-2) '
            '{( X > 500 * MeV )};',
            self.sf._makeTikzNode('( X > 500 * MeV )', 2)
        )
        # Sink
        self.assertEqual(
            r"\node [block, sink, below=of test1-2] (test1-3) "
            r"{SINK( 'Hlt1\%(name)sDecision' )};",
            self.sf._makeTikzNode("SINK( 'Hlt1%(name)sDecision' )", 3)
        )

    def testMakeLine(self):
        """
            Test the basic functionality of StreamerFlowchart._makeLine.
        """
        self.assertEqual(
            r'\path [line] (test1-0) -- (test1-1);',
            self.sf._makeLine(0, 1)
        )

    def testTikz(self):
        """
            Test whether generating the TikZ code for a very simple example
            works.
            A more detailed example can be found in
            test_StreamerFlowchartOnFile.py
        """
        print(self.sf.tikz)
        self.assertMultiLineEqual(
            r'''\node [start] (test1-0) {SomeCode};
\node [block, below=of test1-0] (test1-1) {SomeMoreCode};
\path [line] (test1-0) -- (test1-1);''',
            self.sf.tikz
        )
