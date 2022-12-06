from typeclasses.objects import Object
from evennia import AttributeProperty, prototypes, DefaultScript
import inflect
        

class Plant(Object):
    produce_counter = AttributeProperty(0)
    produce = AttributeProperty(None)

    def return_appearance(self, looker, **kwargs):
        """
        Returns the amount and type gatherable items on a plant.

        """
        p = inflect.engine()
        string = super().return_appearance(looker, **kwargs)
        if self.produce_counter == 0:
            status = f"\n\nThe {self} is bare."
        elif self.produce_counter == 1:
            status = f"\n\nThe {self} has only one {self.produce.replace('_', ' ')} remaining."
        else:
            num_left = p.number_to_words(self.produce_counter)
            plural = p.plural_noun(self.produce).replace("_", " ")
            status = f"\n\nThe {self} has {num_left} {plural} remaining."
        return string + status

    def at_object_creation(self):
        self.scripts.add(GrowthScript)

    def be_harvested(self, caller):
        harvest = prototypes.spawner.spawn(self.produce)[0]
        harvest.location = caller
        self.produce_counter -= 1


class HarvestableObject(Object):
    def at_object_creation(self):
        self.tags.add("boilable")


class GrowthScript(DefaultScript):
    def at_script_creation(self):
        self.key = "growth_script"
        self.desc = "Growing plant"
        self.interval = 60 * 60
        self.plant = self.obj

    def at_repeat(self, **kwargs):
        if self.plant.produce_counter < 10:
            self.plant.produce_counter += 1