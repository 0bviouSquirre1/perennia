from evennia.commands.default.muxcommand import MuxCommand
from commands.command import Command
from evennia import CmdSet, utils
from typeclasses.liquidobjects import LiquidContainer, BoilContainer

import inflect

p = inflect.engine()
liquid_string = "typeclasses.liquidobjects.LiquidContainer"


class CmdFill(MuxCommand):
    """
    Fill a container from another container.

    Usage:
        FILL <container> FROM <another container>
    """

    key = "fill"
    rhs_split = [" from "]
    help_category = "Interaction"

    def func(self):
        caller = self.caller
        self.to_container = self.lhs
        self.from_container = self.rhs

        if not self.args:
            caller.msg("What do you want to fill?")
            return

        to_container = caller.search(self.to_container)
        if not to_container:
            return
        if not isinstance(to_container, LiquidContainer):
            self.caller.msg("You can't fill that!")
            return

        from_container = caller.search(self.from_container, quiet=True)
        if not from_container:
            caller.msg(f"What do you want to fill the {to_container} with?")
            return
        from_container = from_container[0]
        if not isinstance(from_container, LiquidContainer):
            caller.msg(f"The {from_container} does not hold liquids.")
            return
        if from_container.db.fill_level <= 0:
            caller.msg(f"The {from_container} is empty!")
            return

        transfer_amount = to_container.db.capacity - to_container.db.fill_level
        if transfer_amount == 0:
            caller.msg(f"The {to_container} is already full!")
            return
        elif transfer_amount > from_container.db.fill_level:
            transfer_amount = from_container.db.fill_level
        liquid = from_container.db.liquid

        from_container.transfer(-transfer_amount, liquid)
        to_container.transfer(transfer_amount, liquid)

        string = ""
        if from_container.db.fill_level < transfer_amount:
            string += f"$You() $conj(get) what $pron(you) can from the now-empty $obj(vessel)."
        else:
            string += f"$You() $conj(fill) the $obj(receptacle) from the $obj(vessel)."
        self.caller.location.msg_contents(string, from_obj=self.caller, mapping={
            "receptacle": to_container,
            "vessel": from_container}
        )


class CmdEmpty(MuxCommand):
    """
    Empty a container, possibly into another container.
    If no other container is specified, the fill_level will
    be dumped on the ground.

    Usage:
        EMPTY <container> (INTO <another container>)
    """

    key = "empty"
    aliases = "pour"
    help_category = "Interaction"
    rhs_split = [" into "]

    def func(self):
        caller = self.caller
        self.to_container = self.rhs
        self.from_container = self.lhs

        string = ""
        if not self.args:
            caller.msg("What do you want to empty?")
            return

        from_container = caller.search(self.from_container, location=caller, quiet=True)
        if not from_container:
            from_container = caller.search(self.from_container, location=caller.location)
            from_container.move_to(caller, quiet=True, move_type="get")
            return
        if not isinstance(from_container, LiquidContainer):
            caller.msg("You can't empty that!")
            return

        transfer_amount = from_container.db.fill_level
        if transfer_amount == 0:
            caller.msg(f"The {from_container} is already empty!")
            return

        liquid = from_container.db.liquid
        from_container.transfer(-transfer_amount, liquid)

        to_container = caller.search(self.to_container, quiet=True)

        string = ""
        if len(to_container) == 1:
            to_container = to_container[0]
            if not isinstance(to_container, LiquidContainer):
                caller.msg(f"You cannot pour {liquid} into the {to_container}.")
                return
            
            empty = to_container.db.capacity - to_container.db.fill_level
            to_container.transfer(transfer_amount, liquid)

            if transfer_amount > empty:
                string += f"$You() $conj(empty) the $obj(vessel) into the $obj(receptacle)."
                string += f"\nThe rest of the {liquid} splashes all over the ground."
            else:
                string += f"$You() $conj(empty) the $obj(vessel) into the $obj(receptacle)."
        else:
            string += f"$You() $conj(empty) the $obj(vessel) out on the ground."

        caller.location.msg_contents(
            string,
            from_obj=caller,
            mapping={"receptacle": to_container,"vessel": from_container})


class CmdBoil(MuxCommand):
    """
    Put the kettle on to boil.

    Usage:
        BOIL <container>
    """

    key = "boil"
    help_category = "Interaction"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("What do you want to boil?")
            return

        container = self.caller.search(self.args)
        if not container:
            return
        if not isinstance(container, BoilContainer):
            caller.msg("You can't boil that!")
            return

        caller.location.msg_contents(
            container.boil(container),
            from_obj=caller,
            mapping={"boiler": container})


class LiquidCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdFill)
        self.add(CmdEmpty)
        self.add(CmdBoil)
