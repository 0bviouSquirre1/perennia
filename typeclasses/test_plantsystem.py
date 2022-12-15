from evennia import prototypes
from typeclasses.plantobjects import Plant
from evennia.utils.test_resources import EvenniaTest, E


class TestPlantSystem(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.plant = prototypes.spawner.spawn("tomato_plant")[0]

    def test_be_harvested(self):
        result = self.plant.be_harvested(self.char2)

        assert self.plant.produce_counter == 0