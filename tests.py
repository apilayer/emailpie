from gevent import monkey
monkey.patch_all()

import unittest

from emailpie import utils


class TestParse(unittest.TestCase):
    def test_good_email(self):
        validator = utils.EmailChecker('bryan@bryanhelmig.com')
        errors = validator.validate()

        self.assertFalse(errors)

    def test_invalid_email(self):
        validator = utils.EmailChecker('sdahjsdfh.asdofh')
        errors = validator.validate()

        self.assertTrue(errors)

    def test_double_invalid_email(self):
        validator = utils.EmailChecker('sdahjsdfh@@sssss')
        errors = validator.validate()

        self.assertTrue(errors)

    def test_invalid_mx_email(self):
        validator = utils.EmailChecker('bryan@example.com')
        errors = validator.validate()

        self.assertTrue(errors)

    def test_invalid_domain(self):
        validator = utils.EmailChecker('bryan@asdahsdfgasdfgyadfiuyadsfguy.com')
        errors = validator.validate()

        self.assertTrue(errors)


if __name__ == '__main__':
    unittest.main()
