from evennia import prototypes
from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from commands import plant_cmds

class TestPlantCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.plant = prototypes.spawner.spawn("tomato_plant")[0]
        self.plant.move_to(self.room1)

    def test_gather(self):
        self.plant.produce_counter = 5
        self.call(plant_cmds.CmdGather(), f"{self.plant}", f"You gather a {self.plant.produce} from a {self.plant}")

    def test_gather_not_plant(self):
        self.well = prototypes.spawner.spawn("well")[0]
        self.well.move_to(self.char1.location)
        self.call(plant_cmds.CmdGather(), f"{self.well}", "You can't gather that!")

    def test_gather_nothing(self):
        self.call(plant_cmds.CmdGather(), "", "What do you want to gather?")

    def test_gather_empty(self):
        self.plant.produce_counter = 0
        self.call(plant_cmds.CmdGather(), f"{self.plant}", f"There is nothing to gather from a {self.plant}")

    def test_gather_last(self):
        self.plant.produce_counter = 1
        self.call(plant_cmds.CmdGather(), f"{self.plant}", f"You gather the last {self.plant.produce} from a {self.plant}({self.plant.dbref}).")

class TestPlantSystem(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.plant = prototypes.spawner.spawn("tomato_plant")[0]

    def test_be_harvested_zero(self):
        self.plant.produce_counter = 0

        self.plant.be_harvested(self.char2)

        self.assertEqual(self.plant.produce_counter, 0)

    def test_be_harvested_more_than_zero(self):
        self.plant.produce_counter = 2

        self.plant.be_harvested(self.char2)

        self.assertEqual(self.plant.produce_counter, 1)

class TestPlantScript(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.plant = prototypes.spawner.spawn("tomato_plant")[0]
        self.scripty = self.plant.scripts.get("growth_script")[0]

    def test_at_repeat_zero(self):
        self.plant.produce_counter = 0

        self.scripty.at_repeat()

        self.assertEqual(self.plant.produce_counter, 1)

    def test_at_repeat_more_than_ten(self):
        self.plant.produce_counter = 11

        self.scripty.at_repeat()

        self.assertEqual(self.plant.produce_counter, 11)

    def test_at_repeat_less_than_zero(self):
        self.plant.produce_counter = -5

        self.scripty.at_repeat()

        self.assertEqual(self.plant.produce_counter, 0)
