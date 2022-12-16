from evennia import prototypes
from evennia.utils.test_resources import EvenniaTest


class TestPlantSystem(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.plant = prototypes.spawner.spawn("tomato_plant")[0]
        self.scripty = self.plant.scripts.get("growth_script")[0]

    def test_be_harvested_zero(self):
        self.plant.produce_counter = 0

        self.plant.be_harvested(self.char2)

        assert self.plant.produce_counter == 0

    def test_be_harvested_more_than_zero(self):
        self.plant.produce_counter = 2

        self.plant.be_harvested(self.char2)

        assert self.plant.produce_counter == 1

    def test_at_repeat_zero(self):
        self.plant.produce_counter = 0

        self.scripty.at_repeat()

        assert self.plant.produce_counter == 1

    def test_at_repeat_more_than_ten(self):
        self.plant.produce_counter = 11

        self.scripty.at_repeat()

        assert self.plant.produce_counter == 11

    def test_at_repeat_less_than_zero(self):
        self.plant.produce_counter = -5

        self.scripty.at_repeat()

        assert self.plant.produce_counter == 0
