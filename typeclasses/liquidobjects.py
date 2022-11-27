from typeclasses.objects import Object
from evennia import AttributeProperty
from evennia import search_tag

class LiquidContainer(Object):
    capacity = AttributeProperty(100)
    fill_level = AttributeProperty(0)
    liquid = AttributeProperty(None)

    def at_object_creation(self):
        self.db.desc = ""

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

class BoilContainer(LiquidContainer):

    def boil(self, container, caller):
        string = ""
        # check for water in kettle
        if container.fill_level != 0:
            leaf = search_tag("boilable", location=container)
            leaf = leaf[0]
            if leaf:
                string += f"You've boilt {leaf.name} tea."
            else:
                string += "Water boils."
        else:
            string += "You can't boil anything without water!"

        return string