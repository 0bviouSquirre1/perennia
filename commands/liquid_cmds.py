from commands.command import Command
from evennia import CmdSet, utils
import inflect

p = inflect.engine()
liquid_string = "typeclasses.liquidobjects.LiquidContainer"


class CmdFill(Command):
    """
    Fill a container from another container.

    Usage:
        FILL <container> FROM <another container>
    """

    key = "fill"
    help_category = "Interaction"

    def parse(self):
        self.args = self.args.strip()
        to_container, *from_container = self.args.split(" from ", 1)
        self.to_container = to_container.strip()
        if from_container:
            from_container = from_container[0].strip()
            self.from_container = from_container
        else:
            self.from_container = None

    def func(self):
        if not self.args:
            self.caller.msg("What do you want to fill?")
            return

        to_container = self.caller.search(self.to_container)
        if not to_container:
            return
        if not utils.inherits_from(
            to_container, "typeclasses.liquidobjects.LiquidContainer"
        ):
            self.caller.msg("You can't fill that!")
            return

        from_container = self.caller.search(self.from_container, quiet=True)
        if not from_container:
            self.caller.msg(f"What do you want to fill the {to_container} with?")
            return
        from_container = from_container[0]
        if not utils.inherits_from(
            from_container, "typeclasses.liquidobjects.LiquidContainer"
        ):
            self.caller.msg(f"The {from_container} does not hold liquids.")
            return
        if from_container.db.fill_level <= 0:
            self.caller.msg(f"The {from_container} is empty!")
            return

        transfer_amount = to_container.db.capacity - to_container.db.fill_level
        if transfer_amount == 0:
            self.caller.msg(f"The {to_container} is already full!")
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


class CmdEmpty(Command):
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

    def parse(self):
        self.args = self.args.strip()
        from_container, *to_container = self.args.split(" into ", 1)
        self.from_container = from_container.strip()
        if to_container:
            to_container = to_container[0].strip()
            self.to_container = to_container
        else:
            self.to_container = None

    def func(self):
        string = ""
        if not self.args:
            self.caller.msg("What do you want to empty?")
            return

        from_container = self.caller.search(self.from_container)
        if not from_container:
            return
        if not utils.inherits_from(
            from_container, liquid_string
        ):
            self.caller.msg("You can't empty that!")
            return

        transfer_amount = from_container.db.fill_level
        if transfer_amount == 0:
            self.caller.msg(f"The {from_container} is already empty!")
            return

        liquid = from_container.db.liquid
        from_container.transfer(-transfer_amount, liquid)

        to_container = self.caller.search(self.to_container, quiet=True)

        string = ""
        if len(to_container) == 1:
            to_container = to_container[0]
            if not utils.inherits_from(to_container, liquid_string):
                self.caller.msg(f"You cannot pour {liquid} into the {to_container}.")
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

        self.caller.location.msg_contents(string, from_obj=self.caller, mapping={"receptacle": to_container,"vessel": from_container})


class CmdBoil(Command):
    """
    Put the kettle on to boil.

    Usage:
        BOIL <container>
    """

    key = "boil"
    help_category = "Interaction"

    def func(self):
        if not self.args:
            self.caller.msg("What do you want to boil?")
            return

        container = self.caller.search(self.args)
        if not container:
            return
        if not utils.inherits_from(
            container, "typeclasses.liquidobjects.BoilContainer"
        ):
            self.caller.msg("You can't boil that!")
            return

        self.caller.location.msg_contents(container.boil(container), from_obj=self.caller, mapping={"boiler": container})


class LiquidCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdFill)
        self.add(CmdEmpty)
        self.add(CmdBoil)
