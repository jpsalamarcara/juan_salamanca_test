import unittest

from juan.point_b import check_version


class AllTests(unittest.TestCase):

    def test_case1(self):
        v1 = '10.1.3a'
        v2 = '10.1.3b'
        self.assertEqual(check_version(v1, v2), tuple((-1, 1)))
        self.assertEqual(check_version(v2, v1), tuple((1, -1)))

    def test_case2(self):
        v1 = '10.1.3.0.0.0'
        v2 = '10.1.3'
        self.assertEqual(check_version(v1, v2), tuple((0, 0)))
        self.assertEqual(check_version(v2, v1), tuple((0, 0)))

    def test_case3(self):
        v1 = '10.1.3.0.0.0b'
        v2 = '10.1.3'
        self.assertEqual(check_version(v1, v2), tuple((-1, 1)))
        self.assertEqual(check_version(v2, v1), tuple((1, -1)))

    def test_case4(self):
        v1 = '5'
        v2 = '5.0'
        self.assertEqual(check_version(v1, v2), tuple((0, 0)))
        self.assertEqual(check_version(v2, v1), tuple((0, 0)))

    def test_case5(self):
        v1 = '1'
        v2 = 'ab.'
        self.assertRaises(AssertionError, check_version, v1, v2)

    def test_case6(self):
        v1 = '2.5a'
        v2 = '2.5b'
        self.assertEqual(check_version(v1, v2), tuple((-1, 1)))
        self.assertEqual(check_version(v2, v1), tuple((1, -1)))

    def test_case7(self):
        v1 = '0a'
        v2 = '0b'
        self.assertEqual(check_version(v1, v2), tuple((-1, 1)))
        self.assertEqual(check_version(v2, v1), tuple((1, -1)))
