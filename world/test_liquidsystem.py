import unittest

from evennia import prototypes


class TestLiquidSystem(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.well = prototypes.spawner.spawn("well")[0]
        self.kettle = prototypes.spawner.spawn("kettle")[0]
        self.liquid = "water"

    def test_liquid_container(self):
        self.assertEqual(self.well.db.capacity, 1000)
        self.assertEqual(self.well.db.fill_level, 1000)
        self.assertEqual(self.well.db.liquid, self.liquid)

    def test_transfer_in_bounds(self):
        self.well.transfer(-10, self.liquid)
        self.kettle.transfer(10, self.liquid)

        self.assertEqual(self.well.db.fill_level, 990)
        self.assertEqual(self.kettle.db.fill_level, 10)

    def test_transfer_out_of_bounds(self):
        self.well.transfer(-10000, self.liquid)
        self.kettle.transfer(1000, self.liquid)

        self.assertEqual(self.well.db.fill_level, 0)
        self.assertEqual(self.kettle.db.fill_level, 20)