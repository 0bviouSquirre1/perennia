from typeclasses.objects import Object

class Plant(Object):

    def return_appearance(self, looker, **kwargs):
        """
        Returns something about the produce on the plant
        
        """
        string = super().return_appearance(looker, **kwargs)
        status = ""
        return string + status

    def grow(self, produce):
        """
        Grows a new harvestable object on the plant
        
        """
        pass

class Mint(Plant):
    """
    A stone well.
    
    """

    def at_object_creation(self):
        self.db.desc = "an old stone well"
        self.db.liquid = "water"
        self.db.capacity = 1000
        self.db.contents = 1000
        
class Nightshade(Plant):
    """
    A wooden bucket.
    
    """

    def at_object_creation(self):
        self.db.desc = "a sturdy wooden bucket"
        self.db.capacity = 100
        self.db.contents = 0
        self.db.liquid = None

class Tomato(Plant):
    """
    An iron kettle
    
    """

    def at_object_creation(self):
        self.db.desc = "an old iron kettle"
        self.db.capacity = 20
        self.db.contents = 0
        self.db.liquid = None

class Sunflower(Plant):
    """
    A porcelain teacup.
    
    """

    def at_object_creation(self):
        self.db.desc = "a pretty porcelain teacup"
        self.db.capacity = 5
        self.db.contents = 0
        self.db.liquid = None

class Thyme(Plant):
    """
    A silver spoon.
    
    """

    def at_object_creation(self):
        self.db.desc = "a tarnished silver spoon"
        self.db.capacity = 1
        self.db.contents = 0
        self.db.liquid = None