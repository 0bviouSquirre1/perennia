import unittest

from evennia import create_object
from typeclasses.liquidobjects import LiquidContainer

class TestLiquidSystem(unittest.TestCase):
   
    def setUp(self):
        """Called before every test method"""
        super().setUp()
    
    def test_liquid_container(self):
        container = create_object("typeclasses.liquidobjects.LiquidContainer", key="well")
        assert container.db.capacity == 100, f"capacity is {container.db.capacity}"
        assert container.db.fill_level == 0, f"fill_level are {container.db.fill_level}"
        assert container.db.liquid == None, f"liquid is {container.db.liquid}"

    def test_transfer_in_bounds(self):
        self.well = create_object("typeclasses.liquidobjects.LiquidContainer", key="well")
        self.kettle = create_object("typeclasses.liquidobjects.LiquidContainer", key="kettle")
        liquid = "water"
        self.well.fill_level = 20

        self.well.transfer(-10, liquid)
        self.kettle.transfer(10, liquid)

        assert self.well.db.fill_level == 10, f"actually {self.well.db.fill_level}"
        assert self.kettle.db.fill_level == 10, f"actually {self.kettle.db.fill_level}"
    
    def test_transfer_out_of_bounds(self):
        self.well = create_object("typeclasses.liquidobjects.LiquidContainer", key="well")
        self.kettle = create_object("typeclasses.liquidobjects.LiquidContainer", key="kettle")
        liquid = "water"

        self.well.transfer(-10000, liquid)
        self.kettle.transfer(1000, liquid)

        assert self.well.db.fill_level == 0, f"actually {self.well.db.fill_level}"
        assert self.kettle.db.fill_level == 100, f"actually {self.kettle.db.fill_level}"