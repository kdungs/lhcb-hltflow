import unittest

from hltflow.core import Operation


class TestOperation(unittest.TestCase):
    def testIsCut(self):
        """
            Iff a line begins with an opening parenthesis, it's assumed to be a
            cut.
        """
        self.assertTrue(Operation.is_cut(
            '( ( TrPT > %(PT)s * MeV ) & ( TrP  > %(P)s  * MeV ) )'))
        self.assertFalse(Operation.is_cut('Not a cut'))

    def testIsSink(self):
        """
            Iff a line begins with the word SINK, it's assumed to be a sink.
        """
        self.assertTrue(Operation.is_sink("SINK( 'Hlt1%(name)sDecision' )"))
        self.assertFalse(Operation.is_sink('Not a sink'))
