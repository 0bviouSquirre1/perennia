from typeclasses.objects import Object

class LiquidContainer(Object):

    def return_appearance(self, looker, **kwargs):
        """
        Returns the amount and type of liquid in the well.
        
        """
        string = super().return_appearance(looker, **kwargs)
        if self.db.fill_level != 0:
            status = f"\n\nThe {self} has {str(self.db.fill_level)} sips of {self.db.liquid} remaining."
        else:
            status = f"\n\nThe {self} is empty."
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

class Well(LiquidContainer):
    """
    A stone well.
    
    """

    def at_object_creation(self):
        self.db.desc = "an old stone well"
        self.db.liquid = "water"
        self.db.capacity = 1000
        self.db.fill_level = 1000
        
class Bucket(LiquidContainer):
    """
    A wooden bucket.
    
    """

    def at_object_creation(self):
        self.db.desc = "a sturdy wooden bucket"
        self.db.capacity = 100
        self.db.fill_level = 0
        self.db.liquid = None

class Kettle(LiquidContainer):
    """
    An iron kettle
    
    """

    def at_object_creation(self):
        self.db.desc = "an old iron kettle"
        self.db.capacity = 20
        self.db.fill_level = 0
        self.db.liquid = None

class Cup(LiquidContainer):
    """
    A porcelain teacup.
    
    """

    def at_object_creation(self):
        self.db.desc = "a pretty porcelain teacup"
        self.db.capacity = 5
        self.db.fill_level = 0
        self.db.liquid = None

class Spoon(LiquidContainer):
    """
    A silver spoon.
    
    """

    def at_object_creation(self):
        self.db.desc = "a tarnished silver spoon"
        self.db.capacity = 1
        self.db.fill_level = 0
        self.db.liquid = None