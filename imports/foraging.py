""" 
Foraging module. 
  
This module contains data and functions related to foraging.

Created by Poe 
"""

from distutils.sysconfig import customize_compiler 
from evennia.utils import evmenu 
from evennia.utils.gametime import get_season 
import time 
import random 
from evennia import Command 
from evennia import CmdSet 
 
_FORAGE_CLASSES = {} 
FORAGEPIECE_CLASSES = {} 
  
########### 
# Allow searching for a specific herb. 
# basically, 'search dandelion' would refresh one of the  
# herbs, and have a chance to generate the dandelion! 
# Limit number of refreshes. 
# e.g. refreshing an item has a 50% chance to turn up nothing, 
# and instead generates one less option to forage from. 
 
  
# Create a global list of terrain items at some point. 
# FIXME 
ALL_TERRAIN = ["forest", "lakes and ponds", "streams", "tall grass", "swamps", "mud", 
            "brambles and thorns", "leaf cover", "rocky terrain", 
            "the coast", "open ground"] 
 
FORAGE_TYPES = ["berry", "root", "leaf", "stem", "flower"] 
 
FORAGE_DELAY = 5 * 60 # 5 minutes. 
 
class ForageException(Exception):
   def __init__(self, msg): 
        self.msg = msg 
  
class ForagePieceClass: 
    name = "a plant berry" # name 
    type = "berry" # berry, root, leaf, stem, flower 
#   known = "known berry" # name when known 
    unknown = "unknown berry" # name when unknown 
    difficulty = 100 # % chance to spawn. 
    rarity = 0 # 1..100.  0 = always. 
    quantity = 1 # number of harvestables per plant 
#   color = "red" # color of the piece 
    toxic = False 
    tools = [] 
    color_list = ["red"] 
  
class ForageClass: 
    name = "plant name" 
    difficulty = 1 # 1..100 
    durability = 1 # 1..100 
    unknown = "an unidentified plant" # EvMenu when the plant is unrecognized 
#   known = "a familiar plant" # when the plant is recognized 
    desc = "This is the longform plant description." 
    rarity = 100 # % chance to spawn. 
    region = ["forest"] 
    season = ["spring", "summer", "autumn", "winter"] # The seasons when the plant is available. 
    time = [] # A list of time when the plant is available. 
    pieces = [] # A list of ForagePieceClass that can be pulled from the plant. 
             # FIXME - should this automatically happen, or pick plant THEN disassemble? 
    current_pieces = [] # Store the randomly rolled pieces. 
    tools = [] # Required tools. 
  
### 
# Dandelion. 
### 
class DandelionStem(ForagePieceClass): 
    name = "a dandelion stem" 
    type = "stem" 
    difficulty = 1 
    quantity = 1 
#   known = "dandelion stem" 
    unknown = "plant stem" 
#   color = "green" 
    color_list = ["green"] 
  
class DandelionFlower(ForagePieceClass): 
    name = "a dandelion flower" 
    type = "flower" 
    difficulty = 5 
    quantity = 1 
 #    known = "dandelion flower" 
    unknown = "yellow flower" 
 #    color = "yellow" 
    color_list = ["yellow"] 
  
class DandelionRoot(ForagePieceClass): 
    name = "a dandelion root" 
    type = "root" 
    difficulty = 10 
    quantity = 1 
 #    known = "dandelion root" 
    unknown = "brown root" 
 #    color = "brown" 
    color_list = ["brown"] 
  
class DandelionPlant(ForageClass): 
    name = "dandelion" 
    unknown = "an unfamiliar weed" 
    rarity = 100 
    desc = "A leafy weed with a long stem and yellow flower." 
    region = ["forest", "lakes and ponds", "streams", "tall grass", "leaf cover", "brambles and thorns", "open ground"] 
    season = ["spring", "summer", "winter"] # FIXME - Remove winter. 
    pieces = [DandelionStem, DandelionFlower, DandelionRoot] 
_FORAGE_CLASSES["dandelion"] = DandelionPlant 
  
### 
# Miner's lettuce. 
### 
class MinersLettuceLeaf(ForagePieceClass): 
    name = "miner's lettuce leaf" 
    type = "leaf" 
    difficulty = 1 
    quantity = 10 
    rarity = 100 
 #    known = "miner's lettuce leaf" 
    unknown = "green leaf" 
 #    color = "green" 
    color_list = ["green"] 
  
class MinersLettucePlant(ForageClass): 
    name = "miner's lettuce" 
    unknown = "an unfamiliar weed" 
    rarity = 100 
    desc = "A wide-spread weed with numerous, cupped leafs." 
    region = ["forest", "lakes and ponds", "streams", "tall grass", "leaf cover", "brambles and thorns", "open ground"] 
    season = ["spring", "summer", "winter"] # FIXME - Remove winter. 
    pieces = [MinersLettuceLeaf] 
_FORAGE_CLASSES["miner's lettuce"] = MinersLettucePlant 
  
### 
# Foxglove. 
### 
class FoxgloveFlower(ForagePieceClass): 
    name = "foxglove flower" 
    type = "flower" 
    difficulty = 1 
    quantity = 8 
    rarity = 5 
 #    known = "foxglove flower" 
    unknown = "colorful flower" 
 #    color = "purple" # put this in at_obj_creation //  
    color_list = ["purple", "pink", "white", "yellow"] 
    toxic = True 
  
class FoxgloveRoot(ForagePieceClass): 
    name = "a foxglove root" 
    type = "root" 
    difficulty = 10 
    quantity = 1 
 #    known = "foxglove root" 
    unknown = "brown root" 
 #    color = "brown" 
    color_list = ["brown"] 
    toxic = True 
  
class FoxglovePlant(ForageClass): 
    name = "foxglove" 
    unknown = "an unfamiliar flower" 
    rarity = 100 
    desc = "A tall plant with numerous tubular flowers." 
    region = ["forest", "lakes and ponds", "streams", "tall grass", "leaf cover", "brambles and thorns", "open ground"] 
    season = ["spring", "summer", "winter"] # FIXME - Remove winter. 
    pieces = [FoxgloveFlower, FoxgloveRoot] 
_FORAGE_CLASSES["foxglove"] = FoxglovePlant 
  
### 
# Wild Chamomile / pineapple weed 
### 
class WildChamomileFlower(ForagePieceClass): 
    name = "wild chamomile flower" 
    type = "flower" 
    difficulty = 1 
    quantity = 8 
    rarity = 5 
 #    known = "wild chamomile flower" 
    unknown = "round yellow flower" 
    color = "yellow" # put this in at_obj_creation //  
    color_list = ["yellow"] 
  
class WildChamomilePlant(ForageClass): 
    name = "wild chamomile" 
    unknown = "an unfamiliar flower" 
    rarity = 100 
    desc = "A tall plant with numerous round yellow flowers." 
    region = ["forest", "lakes and ponds", "streams", "tall grass", "leaf cover", "brambles and thorns", "open ground"] 
    season = ["spring", "summer", "winter"] # FIXME - Remove winter. 
    pieces = [WildChamomileFlower] 
_FORAGE_CLASSES["wild chamomile"] = WildChamomilePlant 
  
### 
# Blackberry 
### 
class BlackberryBerry(ForagePieceClass): 
    name = "blackberry berry" 
    type = "berry" 
    difficulty = 1 
    quantity = 12 
    rarity = 5 
 #    known = "wild chamomile flower" 
    unknown = "round purple berry" 
 #    color = "black" # put this in at_obj_creation //  
    color_list = ["purple"] 
  
class BlackberryShoot(ForagePieceClass): 
    name = "blackberry shoot" 
    type = "stem" 
    difficulty = 50 
    quantity = 3 
    rarity = 2 
    unknown = "a thorned stem" 
    color_list = ["green"] 
  
class BlackberryPlant(ForageClass): 
    name = "blackberry" 
    unknown = "a thorny bush" 
    rarity = 100 
    desc = "A sprawling bush with sharp thorns." 
    region = ["forest", "lakes and ponds", "streams", "tall grass", "leaf cover", "brambles and thorns", "open ground"] 
    season = ["spring", "summer", "winter"] # FIXME - Remove winter. 
    pieces = [BlackberryShoot, BlackberryBerry] 
_FORAGE_CLASSES["blackberry"] = BlackberryPlant 
  
  
#### 
# Add mushrooms FIXME 
  
  
  
  
  
def get_plants_list(terr, all = False): 
    """Returns a list of valid plants based on the current requirements.""" 
    if terr not in ALL_TERRAIN: 
        return None 
    plist = [] 
    season = get_season() 
    for p in _FORAGE_CLASSES: 
        if all: 
            plist.append(_FORAGE_CLASSES[p]) 
        elif terr in p.region and season in p.season: 
            plist.append(_FORAGE_CLASSES[p]) 
    return plist 
  
def get_room_plants(r): 
    """Returns a list of valid ForageClass items.""" 
    # FIXME - for actual room tags. 
    # terrain = room.tags.get(category="terrain") 
    # plant_list = get_plants_list(terrain) 
    return get_plants_list("forest", True) # FIXME - temp for testing. 
  
def see_plant_as(caller, plant): 
    """Returns the name of the plant as the character sees it.""" 
    if not caller.db.known_plants or plant.name not in caller.db.known_plants: 
        return plant.unknown 
    return plant.name 
  
def known_plant(caller, plant): 
    """Returns whether character knows the specific plant.""" 
    if not caller.db.known_plants or plant.name not in caller.db.known_plants: 
        return False 
    return True 
  
def get_plant_by_name(name): 
    """Returns ForageClass from a (str).""" 
    for plant in _FORAGE_CLASSES: 
        if name in _FORAGE_CLASSES[plant].name: 
            return _FORAGE_CLASSES[plant] 
        if name in _FORAGE_CLASSES[plant].unknown: 
            return _FORAGE_CLASSES[plant] 
    return None 
  
def deforage_room(room): 
    """Set a cooldown timer on the room for foraging.""" 
    room.db.forage_timer = time.time() + FORAGE_DELAY 
  
def seed_forage_room(room, plants): 
    """Add forage items to a room.""" 
    seed_list = [] 
    for plant in plants: 
        if random.randint(1, 100) >= plant.rarity: 
            for piece in plant.pieces: 
                if random.randint(1,100) <= piece.rarity: 
                    piece.db.color = random.choice(piece.color_list) # FIXME -- just added this... hope for the best. 
                    plant.current_pieces.append(piece) 
            seed_list.append(plant) 
    room.ndb.plant_list = seed_list 
  
def has_forage_tool(caller, piece): 
    tools = [] 
    if not piece.tools: 
        return True 
    required = piece.tools.copy() 
    for item in caller.contents: 
        if not required: 
            break 
        for r in required: 
            if item.tags.has(category=r): 
                required.remove(required) 
                tools.append(item) 
    return tools 
  
def foraging_mainmenu(caller): 
    """This is the foraging menu.""" 
  
    caller.ndb.known_plant = False 
    caller.ndb.plant_name = None 
    options = [] 
  
    # free up the plant. 
    if caller.ndb.plant: 
        caller.ndb.busy_plant.ndb.busy = False 
        caller.ndb.busy_plant = None 
  
    for p in caller.location.ndb.plant_list: 
        desc = see_plant_as(caller, p) 

        if desc: 
            options.append({"desc": desc, 
                            "goto": "foraging_select_menu"}) 

    if options: 
        text = "You find the plants below to forage.  Use EXIT to stop foraging." 
    else: 
        text = "There is nothing to forage here." 

    return text, options 

def foraging_end(caller, raw_input, **kwargs): 
    text = "You stop foraging." 
    return text, None 

def foraging_select_menu(caller, raw_string): 
    "Sets up the foraging screen." 
    plist = caller.location.ndb.plant_list 
    iterr = int(raw_string) - 1 
    plant = plist[iterr] 
    caller.ndb.known_plant = plant.name in caller.db.known_plants 
    caller.ndb.plant_name = see_plant_as(caller, plant) 

    # Only one person can interact with a plant at a time. 
    if plant.ndb.busy: 
        options = ({"desc": "Look for something else to forage.", 
                    "goto": "foraging_mainmenu"}) 

        return text, options 

    caller.ndb.busy_plant = plant 
    plant.ndb.busy = True 

    text = f"You examine {caller.ndb.plant_name}.\n" 
    text += plant.desc 

    pieces = [] 
    cannot_forage = [] 
    if plant.current_pieces: 
        for piece in plant.current_pieces: 
            if has_forage_tool(caller, piece): 
                pieces.append(f"{piece.db.color} {piece.type}") 
            else: 
                cannot_forage.append(f"{piece.db.color} {piece.type} {', '.join(piece.tools)}") 

        if pieces: 
            text += f"\nYou may be able to harvest: {', '.join(pieces)}.\n" 
        
        if cannot_forage: 
            text += f"\nYou are not equipped to forage: {', '.join(pieces)}.\n" 

    def select_forage_plant(caller): 
        "This will be executed first when foraging a plant." 
        rtext = f"You forage {caller.ndb.plant_name}.\n" 
        forage_results = [] 
        forage_failure = [] 
        for i in plant.current_pieces: 
            fail = False 
            if not has_forage_tool(caller, i): 
                fail = True 

            if random.randint(1, 100) <= 50: # random chance -- FIXME 
                fail = True 

            if caller.ndb.known_plant: 
                s = f"{i.db.color} {plant.name} {i.type}" 
            else: 
                s = f"unknown {i.db.color} {i.type}" 
            if fail: 
                forage_failure.append(s) 
            else: 
                forage_results.append(s) 

        if forage_results: 
            rtext += f"You manage to gather: {', '.join(forage_results)}.\n" 
        if forage_failure: 
            rtext += f"You failed to gather: {', '.join(forage_failure)}\n" 

        if not caller.ndb.known_plant: 
            # random knowledge roll here.  FIXME 
            rtext += f"\nYou discovered that {caller.ndb.plant_type} is {plant.name}." 
            caller.db.known_plants.append(plant.name) 

        if random.randint(1, 100) <= 50: # -- FIXME 
            rtext += "\nYou destroyed the plant in the process." 
            caller.location.ndb.plant_list.remove(plant) 
        elif not plant.current_pieces: 
            rtext += "\nYou picked the plant clean in the process." 
            caller.location.ndb.plant_list.remove(plant) 
        else: 
            rtext += "\nYou managed to not destroy the plant in the process." 
        caller.msg(rtext) 

        if not caller.location.ndb.plant_list: 
            rtext = "There are no more plants currently available here." 
        deforage_room(caller.location) 

    options = ({"desc": "Forage %s." % caller.ndb.plant_name, # -- FIXME 
                "goto": "foraging_mainmenu", 
                "exec": select_forage_plant}, 
            {"desc": "Look for something else to forage.", 
                "goto": "foraging_mainmenu"}) 

    return text, options 

class CmdForage(Command): 
    """ 
    Start foraging. 
    """ 

    key = "forage" 

    def func(self): 
        "starts foraging." 

        if not self.caller.db.known_plants: 
            self.caller.db.known_plants = [] 

        room_plants = get_room_plants(self.caller.location) 
        if not room_plants: 
            self.msg("You cannot forage here.") 
            return 

        if self.caller.location.db.forage_timer and self.caller.location.db.forage_timer > time.time(): 
            self.msg("There is nothing left to forage.  You will need to search later.") 
            return 

        if not self.caller.location.ndb.plant_list: 
            self.caller.location.ndb.plant_list = room_plants 

        if self.caller.location.db.forage_timer: 
            self.caller.location.db.forage_timer = None 

        evmenu.EvMenu(self.caller, 
                    "world.foraging", 
                    startnode="foraging_mainmenu") 

class ForageCmdSet(CmdSet): 
    def at_cmdset_creation(self): 
            self.add(CmdForage())