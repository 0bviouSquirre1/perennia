from typeclasses.objects import Object
from evennia import AttributeProperty

class LiquidContainer(Object):
    capacity = AttributeProperty(100)
    fill_level = AttributeProperty(0)
    liquid = AttributeProperty(None)

    def at_object_creation(self):
        self.db.desc = ""
        # self.db.capacity = 100
        # self.db.fill_level = 50
        # self.db.liquid = None

    def return_appearance(self, looker, **kwargs):
        """
        Returns the amount and type of liquid in the well.
        
        """
        string = super().return_appearance(looker, **kwargs)
        if self.fill_level == 0:
            status = f"\n\nThe {self} is empty."
        else:
            status = f"\n\nThe {self} has {str(self.fill_level)} sips of {self.liquid} remaining."
        return string + status

    def transfer(self, amount, liquid):
        """
        Updates the amount of liquid in the container.
        
        """
        self.fill_level += amount
        if self.fill_level > self.capacity:
            self.fill_level = self.capacity
        if self.fill_level <= 0:
            self.fill_level = 0
            self.liquid = None
        else:
            self.liquid = liquid