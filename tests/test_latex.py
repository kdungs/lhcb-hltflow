import unittest

from hltflow.core import StreamerFlowchart
from hltflow import latex


class TestLatex(unittest.TestCase):
    def setUp(self):
        """
            Create test fixture. Load code and expected results from files.
        """
        with open('tests/data/code.txt') as f:
            self.sf = StreamerFlowchart('Test', f.read())
        with open('tests/data/code_figure.tex') as f:
            self.expectedFigure = f.read()[:-1]  # don't want empty line
        with open('tests/data/code_document.tex') as f:
            self.expectedDocument = f.read()
        self.figure = latex.make_figure(self.sf)
        self.document = latex.make_document([self.figure])

    def testMakeFigure(self):
        """
            Test whether the latex module can properly produce a figure given a
            StreamerFlowchart.
        """
        self.assertMultiLineEqual(self.expectedFigure, self.figure)

    def testMakeDocument(self):
        """
        """
        self.assertMultiLineEqual(self.expectedDocument, self.document)
