import unittest

from s2f.Sanitize import (
    sanitize_prefix,
    sanitize_for_latex
)

class TestSanitize(unittest.TestCase):
    """ Test case for the Sanitize module """
    def testSanitizePrefix(self):
        """ The function sanitize_prefix should only allow for lower case ASCII
        letters, digits and the hyphen. Upper case letters are supposed to be
        converted to lower case, everything else is supposed to be omitted.
        """
        self.assertEqual(sanitize_prefix('_. Testü@# - .5$ç§÷≠0π00'),
                         'test-5000')

    def testSanitizeForLatex(self):
        """ LaTeX special characters are supposed to be escaped. """
        self.assertEqual(sanitize_for_latex('I am 100% certain!'),
                         r'I am 100\% certain!')
        self.assertEqual(sanitize_for_latex('Toto & Harry'),
                         r'Toto \& Harry')
        self.assertEqual(sanitize_for_latex('~50%'), r'\~50\%')
        self.assertEqual(sanitize_for_latex('%_&~'), r'\%\_\&\~')
