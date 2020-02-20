import unittest
from juan.point_a import check_overlap


def swap(vector: tuple):
    return tuple((vector[1], vector[0]))


class AllTests(unittest.TestCase):

    def test_case1(self):
        a = (3, 8)
        b = (6, 11)
        self.assertTrue(check_overlap(a, b))
        self.assertTrue(check_overlap(b, a))
        self.assertTrue(check_overlap(swap(a), b))
        self.assertTrue(check_overlap(swap(b), a))
        self.assertTrue(check_overlap(swap(b), swap(a)))

    def test_case2(self):
        a = (-25, 25)
        b = (5, 10)
        self.assertTrue(check_overlap(a, b))
        self.assertTrue(check_overlap(b, a))
        self.assertTrue(check_overlap(swap(a), b))
        self.assertTrue(check_overlap(swap(b), a))
        self.assertTrue(check_overlap(swap(b), swap(a)))

    def test_case3(self):
        a = (0, 6)
        b = (7, 11)
        self.assertFalse(check_overlap(a, b))
        self.assertFalse(check_overlap(b, a))
        self.assertFalse(check_overlap(swap(a), b))
        self.assertFalse(check_overlap(swap(b), a))
        self.assertFalse(check_overlap(swap(b), swap(a)))

    def test_case4(self):
        a = (0, 0)
        b = (0, 0)
        self.assertTrue(check_overlap(a, b))

