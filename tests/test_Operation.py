import unittest

from StreamerFlowchart import Operation

class TestOperation(unittest.TestCase):
    def testIsCut(self):
        self.assertTrue(Operation.is_cut(
            '( ( TrPT > %(PT)s * MeV ) & ( TrP  > %(P)s  * MeV ) )'))
        self.assertFalse(Operation.is_cut('Not a cut'))

    def testIsSink(self):
        self.assertTrue(Operation.is_sink("SINK( 'Hlt1%(name)sDecision' )"))
        self.assertFalse(Operation.is_sink('Not a sink'))
