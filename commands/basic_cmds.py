from commands.command import Command
from evennia import CmdSet

import inflect


class CmdPut(Command):
    """
    Put something in a container.

    Usage:
        PUT <object> IN <container>
    """

    key = "put"
    aliases = "place"
    help_category = "Interaction"

    def parse(self):
        self.args = self.args.strip()
        put_obj, *container = self.args.split(" in ", 1)
        if not container:
            put_obj, *container = put_obj.split(" ", 1)
        self.put_obj = put_obj.strip()
        if container:
            container = container[0].strip()
            self.container = container
        else:
            self.container = None

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("What do you want to fill?")
            return

        put_obj = caller.search(self.put_obj)
        if not put_obj:
            return

        container = caller.search(self.container, quiet=True)
        if not container:
            caller.msg(f"Where did you want to put the {put_obj}?")
            return
        container = container[0]

        put_obj.location = container

        # strings are for intended pathways-- self.caller.msg is for error breakouts, I have decided
        string = f"$You() $conj(put) the {put_obj} into the {container}."
        caller.location.msg_contents(string, from_obj=caller)


class CmdGet(Command):
    """
    Pick something up.

    Usage:
      GET <object> (FROM <container>)

    Picks up an object from your location and puts it in
    your inventory.
    """

    key = "get"
    aliases = "grab"
    help_category = "Interaction"
    locks = "cmd:all();view:perm(Developer);read:perm(Developer)"
    arg_regex = r"\s|$"

    def parse(self):
        self.args = self.args.strip()
        obj, *container = self.args.split(" from ", 1)
        if not container:
            obj, *container = obj.split(" ", 1)
        self.obj = obj.strip()
        if container:
            container = container[0].strip()
            self.container = container
        else:
            self.container = None

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("Get what?")
            return
        # search the caller's location first
        obj = caller.search(self.obj, location=caller.location, quiet=True)
        # set the caller as the next location to search
        if not obj:
            loc = caller.search(self.container, location=caller.location, quiet=True)
            obj = caller.search(self.obj, location=loc, quiet=True)

        if not obj:
            loc = caller.search(self.container, location=caller, quiet=True)
            obj = caller.search(self.obj, location=loc, quiet=True)
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return

        if len(obj) == 1:
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
                if self.container:
                    string = f"$You() $conj(retrieve) the {obj.name} from the {self.container}."
                else:
                    string = f"$You() $conj(pick) up the {obj.name}."
                caller.location.msg_contents(string, from_obj=caller)
                # calling at_get hook method
                obj.at_get(caller)
        else:
            pass


class CmdDrink(Command):
    """
    Consume a liquid of your choice.

    Usage:
      DRINK <container>

    Consumes a sip of liquid from a container.
    """

    key = "drink"
    aliases = "sip"
    help_category = "Interaction"

    def func(self):
        if not self.args:
            self.caller.msg("Drink what?")
            return

        container = self.caller.search(self.args)
        string = f"$You() $conj(take) a sip from a $obj(vessel)."
        container.fill_level -= 1
        if container.fill_level == 0:
            string += f"You have emptied {container}"
        self.caller.location.msg_contents(string, from_obj=self.caller, mapping={"vessel": container})


class CmdEat(Command):
    """
    Consume a food of your choice.

    Usage:
      EAT <object>

    Consumes an edible object from your inventory.
    """

    key = "eat"
    aliases = "munch"
    help_category = "Interaction"

    def func(self):
        if not self.args:
            self.caller.msg("Eat what?")
            return

        obj = self.caller.search(self.args, quiet=True)
        if not obj:
            return
        if len(obj) > 1:
            for objec in obj:
                if objec.location == self.caller:
                    obj = objec
                    break
        self.caller.msg(f"You eat a {obj}.")
        obj.delete()


class BasicCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPut)
        self.add(CmdGet)
        self.add(CmdDrink)
        self.add(CmdEat)
