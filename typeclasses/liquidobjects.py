from typeclasses.objects import Object

class LiquidContainer(Object):

    def at_object_creation(self):
        self.db.desc = ""
        self.db.capacity = 100
        self.db.fill_level = 50
        self.db.liquid = None

    def return_appearance(self, looker, **kwargs):
        """
        Returns the amount and type of liquid in the well.
        
        """
        string = super().return_appearance(looker, **kwargs)
        if self.db.fill_level == 0:
            status = f"\n\nThe {self} is empty."
        else:
            status = f"\n\nThe {self} has {str(self.db.fill_level)} sips of {self.db.liquid} remaining."
        return string + status

    def transfer(self, amount, liquid):
        """
        Updates the amount of liquid in the container.
        
        """
        self.db.fill_level += amount
        if self.db.fill_level > self.db.capacity:
            self.db.fill_level = self.db.capacity
        if self.db.fill_level <= 0:
            self.db.fill_level = 0
            self.db.liquid = None
        else:
            self.db.liquid = liquid