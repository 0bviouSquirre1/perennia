from typeclasses.objects import Object
from evennia import AttributeProperty, prototypes
from evennia.utils import lazy_property
from imports.growables import GrowthHandler
import inflect

class Plant(Object):
    produce_counter = AttributeProperty(0)
    produce = AttributeProperty(None)
    time_to_grow = 6000 # in milliseconds

    @lazy_property
    def growth(self):
        return GrowthHandler(self)

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
            plural = p.plural_noun(self.produce).replace('_', ' ')
            status = f"\n\nThe {self} has {num_left} {plural} remaining."
        return string + status
    
    def at_object_creation(self):
        self.growth.add("sprout", 60, key="seedling", desc="A tiny seedling, just barely sprouted.")
        self.growth.add("young", 1200, key="small plant", desc="This plant is small but still growing.", leaves=True)
        self.grow()
        return super().at_object_creation()

    def grow(self):
        self.produce_counter += 1

    def be_harvested(self, caller):
        harvest = prototypes.spawner.spawn(self.produce)[0]
        harvest.location = caller
        self.produce_counter -= 1
    


class HarvestableObject(Object):

    def at_object_creation(self):
        self.tags.add("boilable")
        return super().at_object_creation()