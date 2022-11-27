from commands.command import Command
from evennia import CmdSet

class CmdPut(Command):
    """
    Put something in a container.

    Usage:
        PUT <object> IN <container>
    """
    key = "put"

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
        if not self.args:
            self.caller.msg("What do you want to fill?")
            return

        put_obj = self.caller.search(self.put_obj)
        if not put_obj:
            return

        container = self.caller.search(self.container, quiet=True)
        if not container:
            self.caller.msg(f"Where did you want to put the {put_obj}?")
            return
        container = container[0]

        put_obj.location = container

        # strings are for intended pathways-- self.caller.msg is for error breakouts, I have decided
        string = f"You put the {put_obj} into the {container}."
        self.caller.msg(string)

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
        obj = caller.search(self.obj, location=caller.location, quiet=True)
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
                caller.msg(f"You pick up {obj.name}.")
                caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)
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

    def func(self):
        if not self.args:
            self.caller.msg("Drink what?")
            return

        container = self.caller.search(self.args)
        self.caller.msg(f"You take a sip from {container}.")
        container.fill_level -= 1
        if container.fill_level == 0:
            self.caller.msg(f"You have emptied {container}")

class CmdEat(Command):
    """
    Consume a food of your choice.

    Usage:
      EAT <object>

    Consumes an edible object from your inventory.
    """

    key = "eat"

    def func(self):
        if not self.args:
            self.caller.msg("Eat what?")
            return

        obj = self.caller.search(self.args)
        self.caller.msg(f"You eat {obj}.")
        obj.delete()

class BasicCmdSet(CmdSet):
    
    def at_cmdset_creation(self):
        self.add(CmdPut)
        self.add(CmdGet)
        self.add(CmdDrink)
        self.add(CmdEat)