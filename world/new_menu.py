from evennia.utils import dedent
from typeclasses.characters import Character

#########################################################
#                   Welcome Page
#########################################################

def menunode_welcome(caller):
    """Starting page"""
    
    text = dedent(
    """
        |wWelcome to Perennia!|n

        Perennia aims to be a lush and vibrant world, immersive and engaging with low- and high-stakes adventures available to all characters. As we are in development at the moment, please feel free to experiment and make suggestions where you feel like you ought to be able to interact with something or have two things interact with each other.

        This process will change dramatically over time, so don't get too attached to anything.
    """
    )
    help = "Names that won't break immersion are generally one word (Jod, Jenkins), not a phrase (TheBatMan). Names should also not be completely unpronounceable, we want this game to be accessible to players using screen readers as well."

    options = {
        "desc": "Let's begin!",
        "goto": "menunode_choose_pronouns"
    }

    return (text, help), options

#########################################################
#                Choosing Pronouns
#########################################################

_GENDER_OPTIONS = ["male", "female", "neutral", "plural"]

def menunode_choose_pronouns(caller, **kwargs):
    """Pronoun selection"""

    char = caller.new_char

    char.db.chargen_step = "menunode_choose_pronouns"

    text = dedent(
    """
        |wChoosing Pronouns|n

        Pronouns in Perennia are entirely cosmetic and only affect how you are referred to in text to other players. At the moment the system supports four options, but plans are in the works for players to be able to provide custom pronouns of their own, so bear with us!
    """
    )
    help = (
        "Choose one of the four options. Yes, you can be plural if you want."
    )

    options = []

    for gender in _GENDER_OPTIONS:
        options.append(
            {
                "desc": f"Choose {gender}",
                "goto" (_set_object_choice, )
            }
        )

    options.append(
        {
            "key": ("(Back)", "back", "b"),
            "desc": "Go back to the previous step",
            "goto": "menunode_welcome",
        }
    )

    return (text, help), options

#########################################################
#                Choosing a Name
#########################################################


def menunode_choose_name(caller, raw_string, **kwargs):
    """Name selection"""
    char = caller.new_char

    # another decision, so save the resume point
    char.db.chargen_step = "menunode_choose_name"

    # check if an error message was passed to the node. if so, you'll want to include it
    # into your "name prompt" at the end of the node text.
    if error := kwargs.get("error"):
        prompt_text = f"{error}. Enter a different name."
    else:
        # there was no error, so just ask them to enter a name.
        prompt_text = "Enter a name here to check if it's available."

    # this will print every time the player is prompted to choose a name,
    # including the prompt text defined above
    text = dedent(
        f"""\
        |wChoosing a Name|n

        Especially for roleplaying-centric games, being able to choose your
        character's name after deciding everything else, instead of before,
        is really useful.

        {prompt_text}
        """
    )

    help = "You'll have a chance to change your mind before confirming, even if the name is free."
    # since this is a free-text field, we just have the one
    options = {"key": "_default", "goto": _check_charname}
    return (text, help), options


def _check_charname(caller, raw_string, **kwargs):
    """Check and confirm name choice"""

    # strip any extraneous whitespace from the raw text
    # if you want to do any other validation on the name, e.g. no punctuation allowed, this is the place!
    charname = raw_string.strip()

    # aside from validation, the built-in normalization function from the caller's Account does some useful cleanup on the input, just in case they try something sneaky
    charname = caller.account.normalize_username(charname)

    # check to make sure that the name doesn't already exist
    candidates = Character.objects.filter_family(db_key__iexact=charname)
    if len(candidates):
        # the name is already taken - report back with the error
        return (
            "menunode_choose_name",
            {"error": f"|w{charname}|n is unavailable.\n\nEnter a different name."},
        )
    else:
        # it's free! set the character's key to the name to reserve it
        caller.new_char.key = charname
        # continue on to the confirmation node
        return "menunode_confirm_name"


def menunode_confirm_name(caller, raw_string, **kwargs):
    """Confirm the name choice"""
    char = caller.new_char

    # since we reserved the name by assigning it, you can reference the character key
    # if you have any extra validation or normalization that changed the player's input
    # this also serves to show the player exactly what name they'll get
    text = f"|w{char.key}|n is available! Confirm?"
    # let players change their mind and go back to the name choice, if they want
    options = [
        {"key": ("Yes", "y"), "goto": "menunode_end"},
        {"key": ("No", "n"), "goto": "menunode_choose_name"},
    ]
    return text, options

#########################################################
#                     The End
#########################################################


def menunode_end(caller, raw_string):
    """End-of-chargen cleanup."""
    char = caller.new_char

    # clear in-progress status
    char.attributes.remove("chargen_step")
    text = dedent(
        """
        Congratulations!

        You have completed character creation. Enjoy the game!
    """
    )
    return text, None