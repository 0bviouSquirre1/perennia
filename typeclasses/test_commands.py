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

    def test_get(self):
        pass

    def test_drink(self):
        pass

    def test_eat(self):
        pass
