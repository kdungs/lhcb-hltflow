import unittest

from hltflow.core import StreamerFlowchart


class TestStreamerFlowchartOnFile(unittest.TestCase):
    def setUp(self):
        """
            Instantiate a test fixture.
            Loads code and supposed result from files and builds a
            StreamerFlowchart object with the code.
        """
        with open('tests/data/code.txt') as f:
            self.sf = StreamerFlowchart('Test', f.read())
        with open('tests/data/code_result.txt') as f:
            self.expected = f.read()

    def testMakeTikzLong(self):
        """
            Test whether StreamerFlowchart.tikz works on a real example.
            TestCase.assertMultilineEqual does not seem to work properly or
            there are empty lines that we can't measure.
        """
        for t, e in zip(self.sf.tikz.split('\n'), self.expected.split('\n')):
            self.assertEqual(t, e)
