import unittest

from validemail import utils


class TestParse(unittest.TestCase):
    def test_bad_email(self):
        validator = utils.EmailChecker('bryan@bryanhelmig.com')
        validator.validate()


if __name__ == '__main__':
    unittest.main()
