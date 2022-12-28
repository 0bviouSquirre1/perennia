from evennia.utils.test_resources import EvenniaCommandTest
from evennia import prototypes
from commands import basic_cmds


class TestCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()

        self.item = prototypes.spawner.spawn("tomato")[0]
        self.bucket = prototypes.spawner.spawn("bucket")[0]

        self.put_string = f"{self.item} in {self.bucket}"

        self.item.move_to(self.char1)
        self.bucket.move_to(self.room1)

        self.bucket.fill_level = 10
        self.bucket.liquid = "water"

    def test_put_parser(self):
        command = basic_cmds.CmdPut()
        command.args = self.put_string

        command.parse()

        self.assertEqual(command.put_obj, "tomato")
        self.assertEqual(command.container, "wooden bucket")

    def test_put_nothing(self):
        self.call(basic_cmds.CmdPut(), "", "What do you want to put down?")

    def test_put_nowhere(self):
        self.call(
            basic_cmds.CmdPut(),
            f"{self.item}",
            f"Where did you want to put the {self.item}?",
        )

    def test_put_from_inventory(self):
        self.item.move_to(self.char1)
        self.bucket.move_to(self.room1)

        self.call(
            basic_cmds.CmdPut(),
            f"{self.item} in {self.bucket}",
            f"You put the {self.item} into the {self.bucket}.",
        )

        self.assertEqual(self.item.location, self.bucket)

    def test_put_from_room(self):
        self.item.move_to(self.room1)
        self.bucket.move_to(self.room1)

        self.call(
            basic_cmds.CmdPut(),
            f"{self.item} in {self.bucket}",
            f"You put the {self.item} into the {self.bucket}.",
        )

        self.assertEqual(self.item.location, self.bucket)

    def test_get_parser(self):
        self.item.move_to(self.bucket)

        command = basic_cmds.CmdGet()
        command.args = f"{self.item} from {self.bucket}"

        command.parse()

        self.assertEqual(command.obj, "tomato")
        self.assertEqual(command.container, "wooden bucket")

    def test_get_nothing(self):
        self.call(basic_cmds.CmdGet(), "", "Get what?")

    def test_get_inaccessible(self):
        self.item.locks.add("get:none()")

        self.call(basic_cmds.CmdGet(), f"{self.item}", "You can't get that.")

    def test_get_from_room(self):
        self.item.move_to(self.room1)

        self.call(
            basic_cmds.CmdGet(),
            f"{self.item}",
            f"You pick up the {self.item}.",
        )

        self.assertEqual(self.item.location, self.char1)

    def test_get_from_container(self):
        self.item.move_to(self.bucket)
        self.bucket.move_to(self.room1)

        self.call(
            basic_cmds.CmdGet(),
            f"{self.item} from {self.bucket}",
            f"You retrieve the {self.item} from the {self.bucket}.",
        )

        self.assertEqual(self.item.location, self.char1)

    def test_drink_nothing(self):
        self.call(basic_cmds.CmdDrink(), "", "Drink what?")

    def test_drink_undrinkable(self):
        self.call(basic_cmds.CmdDrink(), f"{self.item}", "You can't drink that!")

    def test_drink(self):
        self.call(
            basic_cmds.CmdDrink(),
            f"{self.bucket}",
            f"You take a sip from a {self.bucket}({self.bucket.dbref}).",
        )

        self.assertEqual(self.bucket.fill_level, 9)

    def test_drink_empty(self):
        self.bucket.fill_level = 1

        self.call(
            basic_cmds.CmdDrink(),
            f"{self.bucket}",
            f"You take a sip from a {self.bucket}({self.bucket.dbref}). You have emptied a {self.bucket}({self.bucket.dbref}).",
        )

        self.assertEqual(self.bucket.fill_level, 0)

    def test_eat_nothing(self):
        self.call(basic_cmds.CmdEat(), "", "Eat what?")

    def test_eat(self):
        self.item.move_to(self.char1)

        self.call(
            basic_cmds.CmdEat(),
            f"{self.item}",
            f"You eat a {self.item}({self.item.dbref}) with obvious enthusiasm.",
        )

        self.assertNotEqual(self.item.location, self.char1)