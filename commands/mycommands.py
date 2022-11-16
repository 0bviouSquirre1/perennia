from commands.command import Command
from evennia import CmdSet
from evennia import default_cmds

class CmdEcho(Command):
    """
    Docstring here
    """
    key = "echo"

    def func(self):
        self.caller.msg(f"Echo: '{self.args.strip()}'")

class MyCmdGet(default_cmds.CmdGet):

    def func(self):
        super().func()
        self.caller.msg(str(self.caller.location.contents))

class CmdHit(Command):
    """
    Hit a target.

    Usage:
      hit <target> [[with] weapon]

    """
    key = "hit"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            weapon = weapon[0].strip()
            self.weapon = weapon
        else:
            self.weapon = ""

    def func(self):
        if not self.args:
            self.caller.msg("Who do you want to hit?")
            return
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return
        # get and handle the weapon
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "bare fists"

        self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        target.msg(f"You got hit by {self.caller.key} with {weaponstr}!")

class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEcho)
        self.add(CmdHit)