import unittest

from StreamerFlowchart import StreamerFlowchart


class TestStreamerFlowchartDefaults(unittest.TestCase):
    def setUp(self):
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

    def testTikz(self):
        """
        """
        self.assertEqual(self.sf.tikz, r'\node [start] (test1-0) {SomeCode};')
