from evennia.utils.test_resources import BaseEvenniaTest
from evennia import create_object
from typeclasses import liquidobjects

class TestLiquidSystem(BaseEvenniaTest):
   
    def setUp(self):
        """Called before every test method"""
        super().setUp()
    
    def test_well(self):
        self.well = create_object("typeclasses.liquidobjects.Well", key="well")
        assert self.well.db.capacity == 1000, f"capacity is {self.well.db.capacity}"
        assert self.well.db.fill_level == 1000, f"fill_level are {self.well.db.fill_level}"
        assert self.well.db.liquid == "water", f"liquid is {self.well.db.liquid}"
    
    def test_bucket(self):
        self.bucket = create_object("typeclasses.liquidobjects.Bucket", key="bucket")
        assert self.bucket.db.capacity == 100, f"capacity is {self.bucket.db.capacity}"
        assert self.bucket.db.fill_level == 0, f"fill_level are {self.bucket.db.fill_level}"
        assert self.bucket.db.liquid == None, f"liquid is {self.bucket.db.liquid}"
    
    def test_kettle(self):
        self.kettle = create_object("typeclasses.liquidobjects.Kettle", key="kettle")
        assert self.kettle.db.capacity == 20, f"capacity is {self.kettle.db.capacity}"
        assert self.kettle.db.fill_level == 0, f"fill_level are {self.kettle.db.fill_level}"
        assert self.kettle.db.liquid == None, f"liquid is {self.kettle.db.liquid}"

    def test_cup(self):
        self.cup = create_object("typeclasses.liquidobjects.Cup", key="cup")
        assert self.cup.db.capacity == 5, f"capacity is {self.cup.db.capacity}"
        assert self.cup.db.fill_level == 0, f"fill_level are {self.cup.db.fill_level}"
        assert self.cup.db.liquid == None, f"liquid is {self.cup.db.liquid}"

    def test_spoon(self):
        self.spoon = create_object("typeclasses.liquidobjects.Spoon", key="spoon")
        assert self.spoon.db.capacity == 1, f"capacity is {self.spoon.db.capacity}"
        assert self.spoon.db.fill_level == 0, f"fill_level are {self.spoon.db.fill_level}"
        assert self.spoon.db.liquid == None, f"liquid is {self.spoon.db.liquid}"

    def test_transfer_in_bounds(self):
        self.well = create_object("typeclasses.liquidobjects.Well", key="well")
        self.kettle = create_object("typeclasses.liquidobjects.Kettle", key="kettle")
        liquid = "water"

        self.well.transfer(-10, liquid)
        self.kettle.transfer(10, liquid)

        assert self.well.db.fill_level == 990, f"actually {self.well.db.fill_level}"
        assert self.kettle.db.fill_level == 10, f"actually {self.kettle.db.fill_level}"
    
    def test_transfer_out_of_bounds(self):
        self.well = create_object("typeclasses.liquidobjects.Well", key="well")
        self.kettle = create_object("typeclasses.liquidobjects.Kettle", key="kettle")
        liquid = "water"

        self.well.transfer(-10000, liquid)
        self.kettle.transfer(1000, liquid)

        assert self.well.db.fill_level == 0, f"actually {self.well.db.fill_level}"
        assert self.kettle.db.fill_level == 20, f"actually {self.kettle.db.fill_level}"