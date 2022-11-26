from commands.command import Command
from evennia import CmdSet
from evennia import utils

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

class BasicCmdSet(CmdSet):
    
    def at_cmdset_creation(self):
        self.add(CmdPut)