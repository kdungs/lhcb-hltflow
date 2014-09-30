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
            self.expected = f.read()[:-1]  # don't want the empty line

    def testMakeTikzOnFile(self):
        """
            Test whether StreamerFlowchart.tikz works on a real example.
        """
        self.assertMultiLineEqual(self.expected, self.sf.tikz)
