from gevent import monkey
monkey.patch_all()

import unittest

from emailpie import utils
from emailpie.spelling import correct
from emailpie.throttle import should_be_throttled, reset_throttle

class TestParse(unittest.TestCase):
    def test_good_email(self):
        validator = utils.EmailChecker('bryan@bryanhelmig.com')
        errors = validator.validate()

        self.assertFalse(errors)

    def test_good_plus_email(self):
        validator = utils.EmailChecker('bryan+merica@bryanhelmig.com')
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

    def test_mispelled_domain(self):
        validator = utils.EmailChecker('bryan@gnail.con')
        self.assertEquals('bryan@gmail.com', validator.didyoumean())


class SpellingTest(unittest.TestCase):
    def test_simple_mispell(self):
        self.assertEquals('gmail', correct('gnail'))
        self.assertEquals('yahoo', correct('uahoo'))
        self.assertEquals('sakjfh', correct('sakjfh'))
        self.assertEquals('guess', correct('guess'))


class ThrottleTest(unittest.TestCase):
    def test_throttle(self):
        for x in range(100):
            self.assertFalse(should_be_throttled('mykey'))

        self.assertTrue(should_be_throttled('mykey', LIMIT=50))

        reset_throttle('mykey')


if __name__ == '__main__':
    unittest.main()
