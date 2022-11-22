from commands.command import Command
from evennia import CmdSet
from evennia import utils
from evennia import prototypes

class CmdGather(Command):
    """
    Gather from a nearby plant.

    Usage:
        GATHER <plant>
    """
    key = "gather"

    def parse(self):
        self.plant = self.args.strip()

    def func(self):
        if not self.plant:
            self.caller.msg("What do you want to gather?")
            return

        plant = self.caller.search(self.plant)
        if not plant:
            return
        if not utils.inherits_from(plant, "typeclasses.plantobjects.Plant"):
            self.caller.msg("You can't gather that!")
            return

        # strings are for intended pathways-- self.caller.msg is for error breakouts, I have decided
        string = ""
        if plant.produce_counter <= 0:
            string += f"There is nothing to gather from a {plant}."
        elif plant.produce_counter == 1:
            string += f"You gather the last {plant.produce.replace('_', ' ')}."
            plant.be_harvested(self.caller)
        else:
            string += f"You gather one unit of {plant.produce} from the {plant}"
            plant.be_harvested(self.caller)
        self.caller.msg(string)

class PlantCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdGather)