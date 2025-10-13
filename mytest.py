import unittest
from bbq import SaiclAareal
class TestCalculatot (unittest.TestCase):
    def setup(self):
        self.calculator = SaiclAareal()
    def test_add(self):
        self.assertEqual(self.calculator.add(4), 11)