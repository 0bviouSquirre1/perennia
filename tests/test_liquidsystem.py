from evennia import prototypes
from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from commands import liquid_cmds


class TestFillCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.well = prototypes.spawner.spawn("well")[0]
        self.kettle = prototypes.spawner.spawn("kettle")[0]
        self.kettle.liquid = "water"
        self.kettle.move_to(self.room1)
        self.well.move_to(self.room1)
        self.fill_string = f"{self.kettle} from {self.well}"

    def test_fill_parser(self):
        command = liquid_cmds.CmdFill()
        command.args = self.fill_string

        command.parse()

        self.assertEqual(command.lhs, "iron kettle")
        self.assertEqual(command.rhs, "stone well")

    def test_fill_parser_no_from_container(self):
        command = liquid_cmds.CmdFill()
        command.args = f"{self.kettle}"

        command.parse()

        self.assertEqual(command.lhs, "iron kettle")
        self.assertEqual(command.rhs, None)

    def test_fill_nothing(self):
        self.call(liquid_cmds.CmdFill(), "", "What do you want to fill?")

    def test_fill_from_nothing(self):
        self.call(
            liquid_cmds.CmdFill(),
            f"{self.kettle}",
            f"What do you want to fill the {self.kettle} with?",
        )

    def test_fill_unfillable(self):
        self.tomato = prototypes.spawner.spawn("tomato")[0]
        self.tomato.move_to(self.char1)

        self.call(liquid_cmds.CmdFill(), f"{self.tomato}", "You can't fill that!")

    def test_fill_from_unfillable(self):
        self.tomato = prototypes.spawner.spawn("tomato")[0]
        self.tomato.move_to(self.char1)

        self.call(
            liquid_cmds.CmdFill(),
            f"{self.kettle} from {self.tomato}",
            f"The {self.tomato} does not hold liquids.",
        )

    def test_fill_empty_from(self):
        self.well.fill_level = 0

        self.call(liquid_cmds.CmdFill(), self.fill_string, f"The {self.well} is empty!")

    def test_fill_full(self):
        self.kettle.fill_level = 20

        self.call(
            liquid_cmds.CmdFill(),
            self.fill_string,
            f"The {self.kettle} is already full!",
        )

    def test_fill(self):
        self.call(
            liquid_cmds.CmdFill(),
            self.fill_string,
            f"You fill the {self.kettle}({self.kettle.dbref}) from the {self.well}({self.well.dbref}).",
        )

        self.assertEqual(self.kettle.fill_level, 20)
        self.assertEqual(self.well.fill_level, 980)

    def test_fill_from_low(self):
        self.well.fill_level = 15

        self.call(
            liquid_cmds.CmdFill(),
            f"{self.kettle} from {self.well}",
            f"You get what you can from the now-empty {self.well}({self.well.dbref}).",
        )

        self.assertEqual(self.kettle.fill_level, 15)
        self.assertEqual(self.well.fill_level, 0)

class TestEmptyCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.well = prototypes.spawner.spawn("well")[0]
        self.kettle = prototypes.spawner.spawn("kettle")[0]
        self.kettle.liquid = "water"
        self.kettle.move_to(self.room1)
        self.well.move_to(self.room1)
        self.fill_string = f"{self.kettle} from {self.well}"

    def test_empty_parser(self):
        command = liquid_cmds.CmdEmpty()
        command.args = f"{self.kettle} into {self.well}"

        command.parse()

        self.assertEqual(command.lhs, "iron kettle")
        self.assertEqual(command.rhs, "stone well")

    def test_empty_parser_ground(self):
        command = liquid_cmds.CmdEmpty()
        command.args = f"{self.kettle}"

        command.parse()

        self.assertEqual(command.lhs, "iron kettle")
        self.assertEqual(command.rhs, None)

    def test_empty_nothing(self):
        self.call(liquid_cmds.CmdEmpty(), "", "What do you want to empty?")

    def test_empty_unemptyable(self):
        self.tomato = prototypes.spawner.spawn("tomato")[0]
        self.tomato.move_to(self.char1)

        self.call(liquid_cmds.CmdEmpty(), f"{self.tomato}", "You can't empty that!")

    def test_empty_empty(self):
        self.call(
            liquid_cmds.CmdEmpty(),
            f"{self.kettle}",
            f"The {self.kettle} is already empty!",
        )

    def test_empty_into_unfillable(self):
        self.tomato = prototypes.spawner.spawn("tomato")[0]
        self.tomato.move_to(self.char1)

        self.kettle.fill_level = 5

        self.call(
            liquid_cmds.CmdEmpty(),
            f"{self.kettle} into {self.tomato}",
            f"You cannot pour {self.kettle.liquid} into the {self.tomato}.",
        )

    def test_empty_overflow(self):
        self.call(
            liquid_cmds.CmdEmpty(),
            f"{self.well} into {self.kettle}",
            f"You empty the {self.well}({self.well.dbref}) into the {self.kettle}({self.kettle.dbref}).\nThe rest of the {self.kettle.liquid} splashes all over the ground.",
        )

    def test_empty(self):
        self.kettle.fill_level = 20
        self.well.fill_level = 500

        self.call(
            liquid_cmds.CmdEmpty(),
            f"{self.kettle} into {self.well}",
            f"You empty the {self.kettle}({self.kettle.dbref}) into the {self.well}({self.well.dbref}).",
        )

        self.assertEqual(self.kettle.fill_level, 0)
        self.assertEqual(self.well.fill_level, 520)

    def test_empty_ground(self):
        self.kettle.fill_level = 20

        self.call(
            liquid_cmds.CmdEmpty(),
            f"{self.kettle}",
            f"You empty the {self.kettle}({self.kettle.dbref}) out on the ground.",
        )

        self.assertEqual(self.kettle.fill_level, 0)

class TestBoilCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.well = prototypes.spawner.spawn("well")[0]
        self.kettle = prototypes.spawner.spawn("kettle")[0]
        self.kettle.liquid = "water"
        self.kettle.move_to(self.room1)
        self.well.move_to(self.room1)
        self.fill_string = f"{self.kettle} from {self.well}"

    def test_boil_nothing(self):
        self.call(liquid_cmds.CmdBoil(), "", "What do you want to boil?")

    def test_boil_unboilable(self):
        self.tomato = prototypes.spawner.spawn("tomato")[0]
        self.tomato.move_to(self.char1)

        self.call(liquid_cmds.CmdBoil(), f"{self.tomato}", "You can't boil that!")

    def test_boil_empty(self):
        self.call(
            liquid_cmds.CmdBoil(),
            f"{self.kettle}",
            "You can't boil anything without water!",
        )

    def test_boil_water(self):
        self.kettle.fill_level = 10

        self.call(
            liquid_cmds.CmdBoil(),
            f"{self.kettle}",
            f"Water boils in the {self.kettle}({self.kettle.dbref})",
        )


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
