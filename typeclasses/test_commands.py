from evennia.utils.test_resources import EvenniaCommandTest
from evennia import prototypes
from commands import basic_cmds


class TestCommands(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.item = prototypes.spawner.spawn("tomato")[0]
        self.bucket = prototypes.spawner.spawn("bucket")[0]

    def test_put(self):
        self.item.move_to(self.char1)

        self.call(basic_cmds.CmdPut(), "put tomato in bucket")

        self.assertEqual(self.item.location, self.bucket)

        # TODO: Something like location.msg_contents = MagicMock() and then location.msg_contents.assert_called_with("Foo is putting the tomato in the bucket.") in order to actually check feedback from commands

    def test_get(self):
        pass

    def test_drink(self):
        pass

    def test_eat(self):
        pass
