import unittest

from s2f.StreamerFlowchart import StreamerFlowchart


class TestStreamerFlowchartDefaults(unittest.TestCase):
    def setUp(self):
        self.sf = StreamerFlowchart('Test % 1', 'SomeCode')

    def testProperties(self):
        """ If no properties parameter is supplied to the constructor the
        attribute should default to empty dict.
        """
        self.assertDictEqual(self.sf.properties, {})

    def testPrefix(self):
        """ If no prefix is specified, it defaults to a lowercase stripped
        version of the name.
        """
        self.assertEqual(self.sf.prefix, 'test1')

    def testMakeTikzNode(self):
        """ Test all (intended) cases of StreamerFlowchart._makeTikzNode. """
        self.assertEqual(
            self.sf._makeTikzNode('Start', 0),
            r'\node [start] (test1-0) {Start};'
        )
        self.assertEqual(
            self.sf._makeTikzNode('>>  Something', 1),
            r'\node [block, below=of test1-0] (test1-1) {Something};'
        )
        self.assertEqual(
            self.sf._makeTikzNode('>>  ( X > 500 * MeV )', 2),
            r'\node [block, cut, below=of test1-1] (test1-2) '
            '{( X > 500 * MeV )};'
        )
        self.assertEqual(
            self.sf._makeTikzNode(">>  SINK( 'Hlt1%(name)sDecision' )", 3),
            r"\node [block, sink, below=of test1-2] (test1-3) "
            r"{SINK( 'Hlt1\%(name)sDecision' )};"
        )
        self.assertEqual(
            self.sf._makeTikzNode(">>  tee  ( monitor( TC_SIZE > 0, '# pass "
                                  "match', LoKi.Monitoring.ContextSvc ) )", 4),
            ''
        )

    def testMakeLine(self):
        self.assertEqual(
            self.sf._makeLine(0, 1),
            r'\path [line] (test1-0) -- (test1-1);'
        )

    def testTikz(self):
        """
        """
        self.assertEqual(self.sf.tikz, r'\node [start] (test1-0) {SomeCode};')
