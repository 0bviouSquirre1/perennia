from evennia import prototypes
from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from commands import liquid_cmds


class TestLiquidSystem(EvenniaTest):
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
    
    def test_boil(self):
        pass

class TestLiquidCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.well = prototypes.spawner.spawn("well")[0]
        self.kettle = prototypes.spawner.spawn("kettle")[0]
        self.liquid = "water"
        self.kettle.move_to(self.room1)
        self.well.move_to(self.room1)

    def test_fill(self):
        self.call(liquid_cmds.CmdFill(), f"{self.kettle} from {self.well}", "Success")

        self.assertEqual(self.kettle.fill_level, 20)
        self.assertEqual(self.well.fill_level, 980)

    def test_fill_from_low(self):
        self.well.fill_level = 15

        self.call(liquid_cmds.CmdFill(), f"{self.kettle} from {self.well}", "Success")

        self.assertEqual(self.kettle.fill_level, 15)
        self.assertEqual(self.well.fill_level, 0)

    def test_empty(self):
        self.kettle.fill_level = 20
        self.well.fill_level = 500

        self.call(liquid_cmds.CmdEmpty(), f"{self.kettle} into {self.well}", "Success")

        self.assertEqual(self.kettle.fill_level, 0)
        self.assertEqual(self.well.fill_level, 520)
    
    def test_empty_ground(self):
        self.kettle.fill_level = 20

        self.call(liquid_cmds.CmdEmpty(), f"{self.kettle}", "Success Ground")

        self.assertEqual(self.kettle.fill_level, 0)
        

    def test_boil(self):
        pass