import unittest

from hltflow.core import StreamerFlowchart


class TestStreamerFlowchartDefaults(unittest.TestCase):
    def setUp(self):
        """
            Instantiate a test fixture.
        """
        self.sf = StreamerFlowchart('Test % 1', 'SomeCode')

    def testProperties(self):
        """
            If no properties parameter is supplied to the constructor the 
            attribute should default to empty dict.
        """
        self.assertDictEqual(self.sf.properties, {})

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
            self.sf._makeTikzNode('Start', 0),
            r'\node [start] (test1-0) {Start};'
        )
        # Tool
        self.assertEqual(
            self.sf._makeTikzNode('>>  Something', 1),
            r'\node [block, below=of test1-0] (test1-1) {Something};'
        )
        # Cut
        self.assertEqual(
            self.sf._makeTikzNode('>>  ( X > 500 * MeV )', 2),
            r'\node [block, cut, below=of test1-1] (test1-2) '
            '{( X > 500 * MeV )};'
        )
        # Sink
        self.assertEqual(
            self.sf._makeTikzNode(">>  SINK( 'Hlt1%(name)sDecision' )", 3),
            r"\node [block, sink, below=of test1-2] (test1-3) "
            r"{SINK( 'Hlt1\%(name)sDecision' )};"
        )
        # Logging (not included in flowchart)
        self.assertEqual(
            self.sf._makeTikzNode(">>  tee  ( monitor( TC_SIZE > 0, '# pass "
                                  "match', LoKi.Monitoring.ContextSvc ) )", 4),
            ''
        )

    def testMakeLine(self):
        """
            Test the basic functionality of StreamerFlowchart._makeLine.
        """
        self.assertEqual(
            self.sf._makeLine(0, 1),
            r'\path [line] (test1-0) -- (test1-1);'
        )

    def testTikz(self):
        """
            Test whether generating the TikZ code for a very simple example
            works.
            A more detailed example can be found in
            test_StreamerFlowchartOnFile.py
        """
        self.assertEqual(self.sf.tikz, r'\node [start] (test1-0) {SomeCode};')
