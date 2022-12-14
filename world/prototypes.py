"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their parents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (equivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""
plant_string = "typeclasses.plantobjects.Plant"
harvest_string = "typeclasses.plantobjects.HarvestableObject"
liquid_string = "typeclasses.liquidobjects.LiquidContainer"
boil_string = "typeclasses.liquidobjects.BoilContainer"

# region Plants
MINT = {
    "prototype_key": "mint_plant",
    "key": "mint plant",
    "typeclass": plant_string,
    "desc": "a square-stemmed mint plant",
    "produce": "mint_leaf",
    "aliases": ("mint", "plant"),
    "locks": "get:not perm(Player)"
}
TOMATO_PLANT = {
    "prototype_key": "tomato_plant",
    "key": "tomato plant",
    "typeclass": plant_string,
    "desc": "a low, bushy tomato plant",
    "produce": "tomato",
    "aliases": ("tomato", "bush", "plant"),
    "locks": "get:not perm(Player)"
}
SUNFLOWER = {
    "prototype_key": "sunflower_plant",
    "key": "sunflower plant",
    "typeclass": plant_string,
    "desc": "a sturdy sunflower plant",
    "long_name": "Following the passage of the sun intently, a sunflower plant grows here.",
    "produce": "sunflower_seed",
    "aliases": ("flower", "sunflower", "plant"),
    "locks": "get:not perm(Player)"
}
THYME = {
    "prototype_key": "thyme_plant",
    "key": "thyme plant",
    "typeclass": plant_string,
    "desc": "a fragrant thyme plant",
    "produce": "thyme_leaf",
    "aliases": ("thyme", "plant"),
    "locks": "get:not perm(Player)"
}
NIGHTSHADE = {
    "prototype_key": "nightshade_plant",
    "key": "nightshade plant",
    "typeclass": plant_string,
    "desc": "a menacing-looking nightshade plant",
    "produce": "nightshade_berry",
    "aliases": ("nightshade", "plant"),
    "locks": "get:not perm(Player)"
}
# endregion

# region Harvest Products
MINT_LEAF = {
    "prototype_key": "mint_leaf",
    "key": "mint leaf",
    "typeclass": harvest_string,
    "desc": "a fragrant leaf from a mint plant",
}
TOMATO = {
    "prototype_key": "tomato",
    "key": "tomato",
    "typeclass": harvest_string,
    "desc": "a bulging, ripe tomato",
}
SUNFLOWER_SEED = {
    "prototype_key": "sunflower_seed",
    "key": "sunflower seed",
    "typeclass": harvest_string,
    "desc": "a crunchy sunflower seed",
}
THYME_LEAF = {
    "prototype_key": "thyme_leaf",
    "key": "thyme leaf",
    "typeclass": harvest_string,
    "desc": "a fragrant leaf from a thyme plant",
}
NIGHTSHADE_BERRY = {
    "prototype_key": "nightshade_berry",
    "key": "nightshade berry",
    "typeclass": harvest_string,
    "desc": "a dark berry from a nightshade plant",
}
# endregion

# region Liquid Containers
WELL = {
    "prototype_key": "well",
    "key": "stone well",
    "typeclass": liquid_string,
    "desc": "an old stone well",
    "capacity": 1000,
    "fill_level": 1000,
    "liquid": "water",
    "locks": "get:not perm(Player)"
}
BUCKET = {
    "prototype_key": "bucket",
    "key": "wooden bucket",
    "typeclass": liquid_string,
    "desc": "a sturdy wooden bucket",
    "capacity": 100,
    "fill_level": 0,
    "liquid": None,
}
KETTLE = {
    "prototype_key": "kettle",
    "key": "iron kettle",
    "typeclass": boil_string,
    "desc": "a rusty iron kettle",
    "capacity": 20,
    "fill_level": 0,
    "liquid": None,
    "locks": "get:not perm(Player)"
}
CUP = {
    "prototype_key": "cup",
    "key": "teacup",
    "typeclass": liquid_string,
    "desc": "a porcelain teacup",
    "capacity": 5,
    "fill_level": 0,
    "liquid": None,
    "aliases": "cup",
}
SPOON = {
    "prototype_key": "spoon",
    "key": "silver spoon",
    "typeclass": liquid_string,
    "desc": "a tarnished silver spoon",
    "capacity": 1,
    "fill_level": 0,
    "liquid": None,
}
# endregion

## example of module-based prototypes using
## the variable name as `prototype_key` and
## simple Attributes

# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"],
# "tags": = [("greenskin", "monster"), ("humanoid", "monster")]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }
