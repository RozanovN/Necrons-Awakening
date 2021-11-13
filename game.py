"""
Your name:
Your student number:

All of your code must go in this file.
"""
import random
import time


def game():
    """

    """
    rows = 25
    columns = 25
    board = make_board(rows, columns)
    print("\tYou stand on the front line of a great and secret war. As an Acolyte of the powerful"
          "Inquisition, you will root out threats to the Imperium of Man. You will engage\nin deadly combat"
          "against heretics, aliens and witches.")
    print("\tBut perhaps the biggest threat you face is your fellow man, for the human soul is such "
          "fertile ground for corruption. It is your duty to shepherd mankind from the\nmanifold paths" 
          " of damnation\n")
    print("Prior to starting your service to the Emperor, you must first create a character.\n")
    character = character_creation()
    command = str(input())
    while command != 'q':  # q = quit
        if command in get_command_list():
            if has_argument(command):
                command = get_command(command)
                command(character)
            else:
                command = get_command(command)
                command()
        else:
            print(command, " is not a command")
        command = str(input())
    print("You may quit now, but your duty to the Emperor will last forever")


def make_board(rows: int, columns: int):
    """
    Create rows by columns board.

    :param rows: a positive integer
    :param columns: a positive integer
    :precondition: rows must be >= 2
    :precondition: columns must be >= 2
    :postcondition: returns rows by columns board with a random description per each cell
    :return: the board as a dictionary
    """
    board = {(row, column): generate_random_room_description() for row in range(rows) for column
             in range(columns)}
    return board


def generate_random_room_description():
    """
    Generate a random room description.

    This is a helper function for make_board().

    :postcondition: returns a random description for a room from the list of description.
    :return: the description as a string
    """
    rooms_description = ["This room is empty", "This room is yet another empty room.",
                         "This room torchers you with its boredom and emptiness.",
                         "This room has an ancient altar.",
                         "This room has a raven sitting on the bust of Pallas.",
                         "This room is full of treasures.",
                         "This room is filled with cosmic terror.",
                         "This room has not seen visitors before."]
    return random.choice(rooms_description)


def character_creation():

    character = {"Name": set_name(), "Adeptus": set_adeptus(), "Max wounds": 0, "Current wounds": 0, "Characteristics":
                 {}, "Level": (1, None), "Skills": {}, "X-coordinate": 0, "Y-coordinate": 0, "Current experience": 0,
                 "Experience for the next level": 1000}
    character["Max wounds"] = set_wounds(character["Adeptus"])
    time.sleep(3)
    character["Current wounds"] = character["Max wounds"]
    character["Characteristics"] = get_characteristics(character["Adeptus"])
    time.sleep(3)
    get_skills(character)
    character["Level"]: get_level_name(character["Adeptus"], character[""])
    return character


def set_name():
    print("Enter your name:")
    name = str(input()).capitalize()
    return name


def set_adeptus():
    print(
          "\n\tAdepts, Adepta or Adeptus is the formal title given to the individual Imperial servants "
          "of the various departments of the Adeptus Terra that serve the will of the \nbeneficent "
          "Emperor. These titles are used by everyone in the service of the Emperor as part of the "
          "Imperial service, from high ranking officials to lowly scribes.\nThe Adepta is the career your character "
          "had before starting his life as an acolyte of an Inquisitor.\n"
          "\n\tThere are 4 adepts in the game. Adepts (Classes) determine your maximum wounds(HP), your skills and your"
          " stats\' propensities.\n\n"
          "\tAdeptus Astra Telepathica is an adeptus of fearsome psykers. They operate with psychic powers, sometimes "
          "referred as \"sorceries\", that can take a myriad of forms from\nreading one's mind to unleashing dreadful "
          "lightnings. Psykers' might comes from warp and the Gods of Chaos. Psykers are physically weak and barely "
          "agile, instead\nthey focus on their mind's strength. However, the true Achilles heel of psykers is their own"
          " outrageous power. Every time psyker fails to cast their psychic power,\nthey must succeed in a will power "
          "or else they will suffer a severe punishment form warp instability. Indeed, to toy with warp is to"
          "perform before the Gods of Chaos; they\nlove the show until they see a single failure.\n"
          "\tAdeptus Astra Militarum is an adeptus of powerful warriors. They specialize in brute force and close "
          "combat. They are the brave souls that lead the Emperor's\nconquest. Those soldiers are strong and though,"
          " yet lack in agility. As for intellect, one only needs to follow orders.\n"
          "\tAdeptus Mechanicus is an adeptus of clever engineers. They specialize in machinery and fight with help of "
          " servo-skulls and dreadful servitors. Mechanics believe in\nthe supremacy of their Machine God —— Omnissiah "
          " —— and eagerly reject their own weak flesh to get divine bionic one. As a result, they end up looking more"
          "robotic than\ntheir own machines. The dire engineers despise involving themselves into battles, despite "
          "having foremost strength and dexterity due to their mechanical prostheses.\nInstead they play their battles "
          "as though they play some chess, so only thing they need is power of their brain.\n"
          "\tAdeptus Officio Assassinorum is an \"elite\" adepta of rogues and hitmen. Inquisitors recruit the most "
          "menacing and terrifying ones to make them acolytes. Those\nassassins are extremely agile, even if they lack "
          "in strength. Preferring the range combat, the best of them are elusive ghosts to their enemies."
          "\n\nPlease, choose your adeptus carefully.")

    adepts_list = ["Adeptus Astra Telepathica", "Adeptus Astra Militarum", "Adeptus Mechanicus", "Adeptus Officio"
                   " Assassinorum"]
    print("To choose an adeptus, enter its index from the numbered list.")
    print_numbered_list_of_possibilities(adepts_list)
    choice = input()
    while choice not in ["1", "2", "3", "4"]:
        print("{0} is not a correct input, try again:".format(choice))
        print("To choose a adeptus enter its index from the numbered list")
        print_numbered_list_of_possibilities(adepts_list)
        choice = input()
    return adepts_list[int(choice) - 1]


def set_wounds(adeptus: str):
    print("\n\tWounds(HP) are a vital part of any character and represent how much punishment they can take before " 
          "meeting the Emperor.")
    print("Your character's wounds are determined by the chosen adeptus and 1k5 dice roll.")
    adeptus_wounds = {"Adeptus Astra Telepathica": 17, "Adeptus Astra Militarum": 23,
                      "Adeptus Mechanicus": 20, "Adeptus Officio Assassinorum": 19}
    max_wounds = adeptus_wounds[adeptus] + roll(1, 5)
    print("You have {0} wounds.".format(max_wounds))
    return max_wounds


def get_characteristics(adeptus: str):
    print("\n\tCharacteristics are crucial part of the game. They determine the results of evasion, fleeing, avoiding "
          "traps. Meanwhile, bonus of your characteristic\n(characteristic divided by 10) affects your damage. "
          "The Characteristics your character has propensities for are equal to 30 + 3k10 dice rolls,\nwhile others "
          " are equal to 30 + 2k10 dice rolls.\n\nCalculating stats...")
    stats = {}
    if adeptus == "Adeptus Astra Telepathica":
        stats = {"Intellect": 30 + roll(3, 10), "Strength": 30 + roll(2, 10), "Toughness": 30 + roll(2, 10), "Agility":
                 30 + roll(2, 10), "Willpower": 30 + roll(2, 10)}  # Willpower is unique for psykers
    elif adeptus == "Adeptus Astra Militarum":
        stats = {"Intellect": 30 + roll(2, 10), "Strength": 30 + roll(3, 10), "Toughness": 30 + roll(3, 10), "Agility":
                 30 + roll(2, 10)}
    elif adeptus == "Adeptus Mechanicus":
        stats = {"Intellect": 30 + roll(3, 10), "Strength": 30 + roll(3, 10), "Toughness": 30 + roll(3, 10), "Agility":
                 30 + roll(3, 10)}
    else:
        stats = {"Intellect": 30 + roll(2, 10), "Strength": 30 + roll(2, 10), "Toughness": 30 + roll(2, 10), "Agility":
                 30 + roll(3, 10)}
    print_dictionary_items(stats)
    return stats


def get_skills(character: dict):
    """

    :param character:
    :return:

    >>> d = {"Skills": {}, "Adeptus": "Adeptus Astra Telepathica"}
    >>> get_skills(d)
    >>> print(d)
    """
    adeptus = character.get("Adeptus")
    dictionary_of_skills = {"Adeptus Astra Telepathica": ("Lightning", "A bolt of blinding lightning strikes from your "
                            "hand dealing 2k10 damage."), "Adeptus Astra Militarum": ("Colossus Smash", "A devastating "
                            "blow of your weapon that deals (1k10 + Strength Bonus) damage."), "Adeptus Mechanicus": (
                            "Laser shot", "Your servo-skull shots a laser beam from its eyes dealing Intellect Bonus "
                            "damage."), "Adeptus Officio Assassinorum": ("Deadly Burst", "you give your foe a burst of"
                            " fire from two plasma-pistols dealing (5 + 1k10 + Agility Bonus) damage.")}
    character["Skills"].setdefault(dictionary_of_skills[character["Adeptus"]][0],
                                    dictionary_of_skills[character["Adeptus"]][1])


def get_level_name(adeptus: str, level: int):
    level_dictionary = {"Adeptus Astra Telepathica": "Magister Telepathicae", "Adeptus Astra Militarum":
                        "Legionary Astartes", "Adeptus Mechanicus": "Techno-Priest", "Adeptus Officio Assassinorum":
                        "Night Haunter", 1: "Acolyte", 2: "Inquisitor"}
    if level != 3:
        return level, level_dictionary[level]
    else:
        return level, level_dictionary[adeptus]


def lightning():
    damage = roll(2, 10)
    print("A bolt of blinding lightning strikes from your hand dealing {0} damage.".format(damage))
    return damage


def colossus_smash(character):
    damage = character["Characteristics"]["Strength"] + roll(1, 10)
    print("A devastating blow of your weapon that deals {0} damage".format(damage))
    return damage


def laser_shot(character):
    damage = character["Characteristics"]["Intellect"]
    print("A devastating blow of your weapon that deals {0} damage to".format(damage))
    return damage


def deadly_burst(character):
    damage = character["Characteristics"]["Agility"] + 5 + roll(1, 10)
    print("A devastating blow of your weapon that deals {0} damage".format(damage))
    return damage


def print_numbered_list_of_possibilities(list_of_options: list):
    """
    Prints a numbered list of options

    :param list_of_options: a non-empty list

    >>> print_numbered_list_of_possibilities(["south", "east"])
    1 south
    2 east
    """
    for index, option_name in enumerate(list_of_options, 1):
        print(green_text() + str(index) + normal_text(), option_name)


def print_dictionary_items(dictionary: dict):
    """

    :param dictionary:

    >>> print_dictionary_items({"a": 1})

    """
    for key in dictionary.keys():
        print(green_text() + key, normal_text() + "is equal to", dictionary[key])


def roll(number_of_dice, number_of_sides):
    list_of_rolls = []
    for number in range(number_of_dice):
        single_roll = (random.choice([number for number in range(1, number_of_sides + 1)]))
        print("Your roll is", single_roll)
        list_of_rolls.append(single_roll)
    print("The sum of your rolls is", sum(list_of_rolls))
    return sum(list_of_rolls)


def help_commands():
    """

    :return:

    >>> help_commands()

    """
    print("{0}h{1} —— show list of commands with a short description\n{0}s{1} —— start the game\n{0}q{1} —— quit the "
          "game\n{0}b{1} —— bandage your wounds and heal your HP".format(green_text(), normal_text()))


def get_command_list():
    commands_dictionary = ["h", "b"]
    return commands_dictionary


def get_command(command_name: str):
    """

    :param command_name:
    :return:
    """
    commands_dictionary = {"h": help_commands, "b": bandage, "Lightning": lightning, "Colossus Smash": colossus_smash,
                           "Laser shot": laser_shot, "Burst of two-gun fire": deadly_burst}
    return commands_dictionary[command_name]


def has_argument(command: str):
    commands_dictionary = {"h": False, "b": True, "Lightning": False, "Colossus Smash": True, "Laser shot": True,
                           "Burst of two-gun fire": True}
    return commands_dictionary[command]


def reached_new_level(character: dict):
    return character["Current experience"] == character["Experience for the next level"]


def level_up(character: dict):
    if character["Level"] == 3:
        return None
    character["Level"] += 1
    character["Experience for the next level"] *= 2
    dictionary_of_skills = {}


def green_text():
    return "\x1b[1;32m"


def normal_text():
    return "\x1b[0;20m"


def bandage(character: dict):
    character['Wounds'] = character['Max wounds']


def describe_current_location(board, character):
    """
    Print the description of character's location.

    :param board: a dictionary
    :param character: a dictionary
    :precondition: board must be a dictionary
    :precondition: board must be a dictionary
    :precondition: character keys must have "X-coordinate" and "Y-coordinate"
    :precondition: character values must be integers that are >= 0
    :precondition: board keys must have coordinates represented as tuple of two integers that are
                    >= 0
    :precondition: board values must have room's description as a string
    :postcondition: prints the description of character's location
    >>> describe_current_location({(0, 0): "This room is empty"}, {"X-coordinate": 0, "Y-coordinate": 0})
    <BLANKLINE>
    This room is empty
    """
    print("\n" + board[(character["X-coordinate"], character["Y-coordinate"])])


def get_available_directions(character, columns, rows):
    """
    Get the list of available directions.

    :param character: a dictionary
    :param columns: an integer
    :param rows: an integer
    :precondition: character must be a dictionary
    :precondition: columns >= 0
    :precondition: rows >= 0
    :precondition: character keys must have "X-coordinate" and "Y-coordinate"
    :precondition: character values must be integers that are >= 0
    :postcondtition: returns a list of available directions based on current character's coordinates
    :postcondtion:
    :return: available directions as a list

    >>> get_available_directions(make_character(), 4, 4)
    ['south', 'east']
    >>> get_available_directions({"Y-coordinate": 1, "X-coordinate": 1}, 4, 4)
    ['north', 'south', 'west', 'east']
    >>> get_available_directions({"Y-coordinate": 1, "X-coordinate": 3}, 4, 4)
    ['north', 'south', 'west']
    """
    available_directions = []
    if character["Y-coordinate"] > 0:
        available_directions.append("north")
    if character["Y-coordinate"] < rows - 1:
        available_directions.append("south")
    if character["X-coordinate"] > 0:
        available_directions.append("west")
    if character["X-coordinate"] < columns - 1:
        available_directions.append("east")
    return available_directions





def main():
    """
    Drive the program
    """
    print("{:^160}".format("It is the 41st Millennium… "), (
        "\n \tFor more than a hundred centuries the Emperor has sat immobile on the Golden Throne "
        "of Earth. He is the master of mankind by the will of the gods, and master of a "
        "\nmillion worlds by the might of his inexhaustible armies. He is a rotting carcass "
        "writhing invisibly with power from the Dark Age of Technology. He is the "
        "Carrion Lord of\nthe Imperium for whom a thousand souls are sacrificed every day, "
        "so that he may never truly die."), (
        "\n\tYet in his deathless state, the Emperor continues his eternal vigilance. Mighty "
        "battle fleets cross the Daemon-infested miasma of the warp, the only route between \n"
        "distant stars, their way lit by the Astronomican, the psychic manifestation of "
        "the Emperor’s will. Vast armies give battle in his name on uncounted worlds. "
        "Greatest\namongst his soldiers are the Adeptus Astartes, the Space Marines, "
        "bio-engineered super-warriors. Their comrades in arms are legion: the "
        "Imperial Guard and countless\nplanetary defence forces, the ever-vigilant "
        "Inquisition and the Tech-Priests of the Adeptus Mechanicus, to name but a few. But "
        "for all their multitudes, they are \nbarely enough to hold off the ever-present "
        "threat from aliens, heretics, mutants—and worse."), (
        "\n\tTo be a man in such times is to be one amongst untold billions. It "
        "is to live in the cruellest and most bloody regime imaginable. Forget the power of " 
        "technology and \nscience, for so much has been forgotten, never to be re-learned. " 
        "Forget the promise of progress and understanding, for in the grim darkness of " 
        "the far future, there is \nonly war. There is no peace amongst the stars, " 
        "only an eternity of carnage and slaughter, and the laughter of thirsting gods."),
        "\nAll rights belong to Games Workshop.")
    time.sleep(3)
    print("\n\n\n{:^160}".format("Welcome to the nightmarish world of Warhammer 40k Dark Heresy"))
    print("\nPlease type {0}s{1} to start the game:".format(green_text(), normal_text()))
    print("You may desert anytime by typing {0}q{1}.".format(green_text(), normal_text()))
    if str(input()) == 's' or "start":
        game()


if __name__ == '__main__':
    main()
