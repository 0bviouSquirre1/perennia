from evennia.commands.default.comms import CmdChannel, CmdPage
from evennia.commands.default import general, help, account
from evennia import CmdSet


class HelpCmdChannel(CmdChannel):
    help_category = "Communication"


class HelpCmdPage(CmdPage):
    locks = "cmd:perm(Admin)"
    help_category = "Communication"


class HelpCmdSay(general.CmdSay):
    help_category = "Communication"


class HelpCmdWhisper(general.CmdWhisper):
    help_category = "Communication"


class HelpCmdAccess(general.CmdAccess):
    help_category = "Helpers"


class HelpCmdHelp(help.CmdHelp):
    help_category = "Helpers"


class HelpCmdNick(general.CmdNick):
    help_category = "Helpers"


class HelpCmdDrop(general.CmdDrop):
    help_category = "Interaction"


class HelpCmdGive(general.CmdGive):
    help_category = "Interaction"


class HelpCmdInventory(general.CmdInventory):
    help_category = "Personal Info"


class HelpCmdLook(general.CmdLook):
    help_category = "Interaction"


class HelpCmdPose(general.CmdPose):
    help_category = "Personal Info"


class HelpCmdSetDesc(general.CmdSetDesc):
    help_category = "Personal Info"

class HelpCmdQuell(account.CmdQuell):
    locks = "cmd:pperm(Builder)"
    help_category = "Admin"


class HelpCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(HelpCmdChannel)
        self.add(HelpCmdPage)
        self.add(HelpCmdSay)
        self.add(HelpCmdWhisper)
        self.add(HelpCmdAccess)
        self.add(HelpCmdHelp)
        self.add(HelpCmdNick)
        self.add(HelpCmdDrop)
        self.add(HelpCmdGive)
        self.add(HelpCmdInventory)
        self.add(HelpCmdLook)
        self.add(HelpCmdPose)
        self.add(HelpCmdSetDesc)
        self.add(HelpCmdQuell)
