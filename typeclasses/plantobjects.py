from typeclasses.objects import Object
from evennia import AttributeProperty

class Plant(Object):
    produce_counter = AttributeProperty(0)
    produce = AttributeProperty(None)
    time_to_grow = 6000 # in milliseconds

    def return_appearance(self, looker, **kwargs):
        """
        Returns the amount and type of liquid in the well.
        
        """
        string = super().return_appearance(looker, **kwargs)
        if self.produce_counter == 0:
            status = f"\n\nThe {self} is bare."
        else:
            status = f"\n\nThe {self} has {str(self.produce_counter)} units of {self.produce} remaining."
        return string + status
    
    def at_object_creation(self):
        self.grow()
        return super().at_object_creation()

    def grow(self):
        self.produce_counter += 1

    def be_harvested(self):
        # spawn produce in player inventory
        self.produce_counter -= 1


class HarvestableObject(Object):

    def at_object_creation(self):
        return super().at_object_creation()