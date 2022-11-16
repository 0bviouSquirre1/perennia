from typeclasses.objects import Object
from evennia.contrib.base_systems.components import ComponentHolderMixin

class LiquidContainer(ComponentHolderMixin, Object):
    pass

from evennia.contrib.base_systems.components import Component

class Liquid(Component):
    pass