#
#   Perennia Starter World
# 

#HEADER

from evennia import create_object

#CODE

kitchen = create_object("rooms.Room",key="kitchen")

# 
tel kitchen
# 
set kitchen/long_name = A tidy little kitchen
# 
set kitchen/desc = Bottles and jars line the shelves of this homey cookspace. A small hearth in one corner warms the cottage.
# 
spawn kettle
# 
spawn cup
# 
spawn spoon
# 
dig front room = the front room;room;r, the kitchen;kitchen;k
#
room
# 
set front room/long_name = A cozy sitting area
# 
set front room/desc = An overstuffed couch strewn with knitted and woven blankets sits beneath a window in the western wall, and on the north a bookcase stands packed with a jumble of mismatched tomes.
# 
dig front step = the front step;step;s, the front room;room;r
#
step
# 
set front step/long_name = A set of stone steps
# 
set front step/desc = Stone steps lead up to a sturdy wooden door held together with iron bands at the top and bottom. Flowers crowd the threshold and bees can be heard buzzing among them. A flagstone path leads south through a wooden gate and into the shadows of the trees.
# 
spawn sunflower
# 
dig west yard = the western yard;west;w, the front step;step;s
#
west
#
set west yard/long_name = A sunny garden
#
set west yard/desc = Herbs and vegetables are planted here in untidy patches. The garden is well cared-for, but whoever planted it was not interested in straight lines.
# 
spawn mint
# 
spawn thyme
# 
spawn tomato
# 
dig back yard = behind the house;behind;b, the western yard;west;w
#
tel back yard
#
set back yard/long_name = A shady spot
#
set back yard/desc = On the north side of the cottage, it is noticeably cooler as the sunlight rarely reaches this spot. Weeds and wildflowers are starting to overtake this area.
# 
spawn nightshade
# 
dig east yard = the eastern yard;east;e, behind the house;behind;b
#
tel east yard
#
set east yard/long_name = A sunny clearing
#
open the front step;step;s = front step
#
set east yard/desc = The space between the cottage and the fence on this side has been cut clear to allow easy access to the well. The grassy stubble underfoot has started to soften, creating a pleasant walking surface.
# 
spawn well
# 
spawn bucket
#
tel front step
# 
open the eastern yard;east;e = east yard
# 
tel kitchen-1