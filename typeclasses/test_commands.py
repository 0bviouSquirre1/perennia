from evennia.utils.test_resources import EvenniaCommandTest
from evennia import prototypes
from commands import basic_cmds


class TestCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.item = prototypes.spawner.spawn("tomato")[0]
        self.bucket = prototypes.spawner.spawn("bucket")[0]
        self.bucket.fill_level = 10
        self.bucket.liquid = "water"

    def test_put(self):
        self.item.move_to(self.char1)
        self.bucket.move_to(self.room1)

        self.call(basic_cmds.CmdPut(), f"{self.item} in {self.bucket}", "Success")

        self.assertEqual(self.item.location, self.bucket)

        # TODO: Something like location.msg_contents = MagicMock() and then location.msg_contents.assert_called_with("Foo is putting the tomato in the bucket.") in order to actually check feedback from commands

    def test_get_from_room(self):
        self.item.move_to(self.room1)

        self.call(basic_cmds.CmdGet(), f"{self.item}", "Success")

        self.assertEqual(self.item.location, self.char1)

    def test_get_from_container(self):
        self.item.move_to(self.bucket)
        self.bucket.move_to(self.room1)

        self.call(basic_cmds.CmdGet(), f"{self.item} from {self.bucket}", "Success")

        self.assertEqual(self.item.location, self.char1)

    def test_drink(self):
        self.bucket.move_to(self.room1)

        self.call(basic_cmds.CmdDrink(), f"{self.bucket}", "Success")

        self.assertEqual(self.bucket.fill_level, 9)

    def test_eat(self):
        self.item.move_to(self.char1)

        self.call(basic_cmds.CmdEat(), f"{self.item}", "Success")

        self.assertNotEqual(self.item.location, self.char1)
