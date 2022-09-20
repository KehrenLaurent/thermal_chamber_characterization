from math import sqrt
import unittest

import calc


class TestCalc(unittest.TestCase):
    def test_moyenne(self):
        self.assertEqual(5.5, calc.moyenne([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

    def test_get_incertitude_type_uniforme(self):
        self.assertEqual(1/sqrt(3), calc.get_incertitude_type_uniforme(1))

    def test_get_somme_quadratique(self):
        self.assertEqual(0.37417, round(
            calc.get_somme_quadratique([0.1, 0.2, 0.3]), 5))
