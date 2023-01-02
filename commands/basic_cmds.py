from commands.command import Command
from evennia.commands.default.muxcommand import MuxCommand
from evennia import CmdSet, utils

import inflect


class CmdPut(MuxCommand):
    """
    Put something in a container.

    Usage:
        PUT <object> IN <container>
    
    Move an object from your inventory (or your location) to a container.
    """

    key = "put"
    aliases = ["place"]
    help_category = "Interaction"

    rhs_split = [" in "]

    def func(self):
        caller = self.caller
        self.put_obj = self.lhs
        self.container = self.rhs

        if not self.args:
            caller.msg("What do you want to put down?")
            return

        container = caller.search(self.container, location=caller, quiet=True)
        if not container:
            container = caller.search(self.container, location=caller.location, quiet=True)

        if not container:
            caller.msg(f"Where did you want to put the {self.put_obj}?")
            return

        put_obj = caller.search(self.put_obj, location=caller, quiet=True)
        if not put_obj:
            put_obj = caller.search(self.put_obj, location=caller.location, quiet=True)

        if not put_obj:
            caller.msg(f"Could not find '{self.put_obj}'.")
            return

        container = container[0]
        put_obj = put_obj[0]

        success = put_obj.move_to(container, quiet=True)
        if not success:
            caller.msg("You can't do that.")
        else:
            string = f"$You() $conj(put) the {put_obj} into the {container}."
            caller.location.msg_contents(string, from_obj=caller)


class CmdGet(MuxCommand):
    """
    Pick something up.

    Usage:
      GET <object> (FROM <container>)

    Picks up an object from your location and puts it in
    your inventory.
    """

    key = "get"
    aliases = ["grab", "pick up", "take"]
    help_category = "Interaction"
    arg_regex = r"\s|$"

    rhs_split = [" from "]

    def func(self):
        caller = self.caller
        self.obj = self.lhs
        self.container = self.rhs

        if not self.args:
            caller.msg("What did you want to get?")
            return

        container = caller.search(self.container, location=caller.location, quiet=True)

        if not container:
            container = caller.search(self.container, location=caller, quiet=True)

        if not container:
            location = caller.location
            string = f"$You() $conj(pick) up a {self.obj}."
        else:
            location = container
            string = f"$You() $conj(get) a {self.obj} from the {container[0]}."

        obj = caller.search(self.obj, location=location, quiet=True)

        if not obj:
            caller.msg(f"Could not find '{self.obj}'.")
            return

        if caller == obj:
            caller.msg("You can't get yourself.")
            return

        obj = obj[0]

        if not obj.access(caller, "get"):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_pre_get hook method
        if not obj.at_pre_get(caller):
            return

        success = obj.move_to(caller, quiet=True, move_type="get")
        if not success:
            caller.msg("This can't be picked up.")
        else:
            caller.location.msg_contents(string, from_obj=caller)
            # calling at_get hook method
            obj.at_get(caller)


class CmdDrink(MuxCommand):
    """
    Consume a liquid of your choice.

    Usage:
      DRINK <container>

    Consumes a sip of liquid from a container.
    """

    key = "drink"
    aliases = ["sip", "quaff", "drink from"]
    help_category = "Interaction"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("Drink what?")
            return

        container = caller.search(self.args)

        if not container:
            caller.msg("Drink what?")

        if not utils.inherits_from(
            container, "typeclasses.liquidobjects.LiquidContainer"
        ):
            caller.msg("You can't drink that!")
            return

        if container.fill_level == 0:
            caller.msg(f"You can't drink from an empty {container}.")
        else:
            container.transfer(-1, container.liquid)

            string = f"$You() $conj(take) a sip from a $obj(vessel)."

            if container.fill_level == 0:
                string += f" This empties a $obj(vessel)."

            caller.location.msg_contents(
                string, from_obj=caller, mapping={"vessel": container}
            )


class CmdEat(Command):
    """
    Consume a food of your choice.

    Usage:
      EAT <object>

    Consumes an edible object from your inventory.
    """

    key = "eat"
    aliases = ["munch"]
    help_category = "Interaction"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("Eat what?")
            return

        obj = self.caller.search(self.args, location=caller, quiet=True)

        if not obj:
            return

        obj = obj[0]
        string = f"$You() $conj(eat) a $obj(food) with obvious enthusiasm."
        self.caller.location.msg_contents(
            string, from_obj=self.caller, mapping={"food": obj}
        )
        obj.delete()


class BasicCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPut)
        self.add(CmdGet)
        self.add(CmdDrink)
        self.add(CmdEat)
