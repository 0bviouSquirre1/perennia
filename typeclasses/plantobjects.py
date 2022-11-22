from typeclasses.objects import Object
from evennia import AttributeProperty

class Plant(Object):
    produce_counter = AttributeProperty(0)
    
    def at_object_creation(self):
        self.grow()
        return super().at_object_creation()

    def grow(self):
        produce_counter += 1
        pass

    def be_harvested(self):
        # spawn produce in player inventory
        produce_counter -= 1


class HarvestableObject(Object):

    def at_object_creation(self):
        return super().at_object_creation()