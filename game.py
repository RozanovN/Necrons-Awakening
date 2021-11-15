"""
Your name:
Your student number:

All of your code must go in this file.
"""
import random
import time
import itertools


def game():
    """
    Drive the game.
    """
    rows = 25
    columns = 25
    board = {
        (0, 0):
            tutorial,
        (25, 0):
            boss
    }
    print("\tYou stand on the front line of a great and secret war. As an Acolyte of the powerful"
          " Inquisition, you will root out threats to the Imperium of Man. You will engage\nin deadly combat"
          "against heretics, aliens and witches.")
    print("\tBut perhaps the biggest threat you face is your fellow man, for the human soul is such "
          "fertile ground for corruption. It is your duty to shepherd mankind from the\nmanifold paths"
          " of damnation\n")
    print("Prior to starting your service to the Emperor, you must first create a character.\n")
    character = character_creation()
    user_input = None
    in_combat = False
    enemy = {}

    while user_input != "q" and is_alive(character) and is_goal_attained(character):  # q = quit
        if user_input in get_command_list():
            if has_argument(user_input):
                user_input = get_command(user_input)
                user_input(character)
            else:
                user_input = get_command(user_input)
        if not in_combat:
            available_directions = get_available_directions(character, rows, columns)
            print_numbered_list_of_possibilities(available_directions)
            user_input = str(input())
            if user_input in get_command_list():
                continue
            elif not validate_option(user_input, available_directions):
                print("{0} is not a valid input. Please, try again.".format(user_input))
                continue
            user_input = int(user_input) - 1
            coordinates = move_character(character, user_input, available_directions)
            add_room_to_the_board(coordinates, board)
            show_filtered_map("", get_map(board, character, columns, rows))
            show_wounds(character["Current wounds"], character["Max wounds"])
            describe_current_location(board, coordinates)
            time.sleep(1)
            if check_for_foes():
                in_combat = True   # Combat begins
                enemy = generate_enemy(character["Level"][0])
        elif in_combat:
            if not (is_alive(character) and is_alive(enemy) and character["Will to fight"] and enemy["Will to fight"]):
                in_combat = False  # Combat ends
            print_numbered_list_of_possibilities(list(character["Skills"].keys()))
            user_input = str(input())
            if user_input in get_command_list():
                continue
            elif validate_option(user_input, list(character["Skills"].keys())):
                print("{0} is not a valid input. Please, try again.".format(user_input))
                continue
            damage = use_skill(character, list(character["Skills"].keys())[int(user_input) - 1], enemy)  # player's turn
            enemy["Current wounds"] -= 0 if has_evaded(enemy) else damage / 2 if has_sustained(character) else damage
            damage = use_skill(enemy, random.choice(list(enemy["Skills"].keys())), character)  # enemy's turn
            character["Current wounds"] -= 0 if has_evaded(character) else damage / 2
            if random.randrange(1, 6) == 1:
                use_skill(enemy, list(enemy["Skills"].keys())[0], character)  # Enemy fleeing, boss' additional attack
        if reached_new_level(character):
            time.sleep(1)
            print("\nYou reached new level.")
            level_up(character)
    if user_input == "q":  # Make Game Over function later
        print("\nYou may deserve now, but your duty to the Emperor will last forever")
    elif is_alive(character):
        print("\nYou died. Game over!")
    else:
        print("Congratulations! You slain yet another blasphemous denizen of the Realm of Chaos and retrieved"
              "an accursed Necronian artifact.\nThe end.")


def add_room_to_the_board(coordinates: tuple, board: dict):
    """
    Add a room to the board if the board doesn't have a room at the given coordinates

    :param board: a dictionary
    :param coordinates: tuple of positive integers
    :precondition: board must be a dictionary
    :precondition: coordinates items must be positive integers
    :postcondition: Adds a room with random description to the board if the board doesn't have a room at the given
                    coordinates
    """
    if coordinates not in board.keys():
        board.setdefault(coordinates, generate_random_room_description())


def generate_random_room_description():
    """
    Generate a random room description.

    This is a helper function for make_board().

    :postcondition: returns a random description for a room from the list of description.
    :return: the description as a string
    """
    list_of_rooms = [
        #"This room is empty", "This room is yet another empty room.",
        #"This room torchers you with its boredom and emptiness.",
        empty_room
        ancient_altar_room,
        crate,
        eldritch_altar,
        stack of books,
        discarded_pack,
        necronian_chest,
        necronian_alchemy_table,
        decorative_urn
        iron_maiden,
        locked_sarcophagus,
        suit_of_armor,
        makeshift_dining_table,
        pile_of_bones,
        eerie_spiderweb,
        mummified_remains,
        transcendent_terror,
        iron_crown,
        ceiling_drops
        shifting_mist
        ]
    return random.choices(list_of_rooms, weights=[5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], k=1)[0]


def character_creation():
    character = {
        "Name": set_name(),
        "Adeptus": set_adeptus(),
        "Max wounds": 0,
        "Current wounds": 0,
        "Characteristics": {},
        "Level": (1, None),
        "Skills": {
            "Flee Away": "You retreat to the previous room"},
        "X-coordinate": 0,
        "Y-coordinate": 0,
        "Current experience": 0,
        "Experience for the next level": 1000,
        "Will to fight": True,
        "Inventory": {
            "Bandage" : 10
        }
    }
    character["Max wounds"] = set_wounds(character)
    character["Current wounds"] = character["Max wounds"]
    time.sleep(3)
    character["Characteristics"] = get_characteristics(character)
    time.sleep(3)
    get_skills(character)
    print("To check the list of skills type {0}s{1}.\nRight now you have the following skills:".format(green_text(),
          normal_text()))
    character["Level"] = get_level_name(character["Adeptus"], character["Level"][0])
    print("To see your inventory type {0}i{1}".format(green_text(), normal_text()))
    return character


def set_name():
    print("Enter your name:")
    name = str(input()).capitalize()
    while name == "":
        print("You must enter something. Even this grim dark world wants to know your name. Please, try again:")
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
        " outrageous power. Indeed, to toy with warp is to perform before the Gods of\nChaos; they love the show until "
        "they see a single failure.\n"
        
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
    while not validate_option(choice, adepts_list) and choice != "q":
        print("{0} is not a correct input, try again:".format(choice))
        print("To choose an adeptus enter its index from the numbered list")
        print_numbered_list_of_possibilities(adepts_list)
        choice = input()
    return adepts_list[int(choice) - 1]


def set_wounds(character: dict):
    print("\n\tWounds(HP) are a vital part of any character and represent how much punishment they can take before "
          "meeting the Emperor.")
    print("Your character's wounds are determined by the chosen adeptus and 1k5 dice roll.")
    adeptus_wounds = {
        "Adeptus Astra Telepathica": 17,
        "Adeptus Astra Militarum": 23,
        "Adeptus Mechanicus": 20,
        "Adeptus Officio Assassinorum": 19}
    print("Your adeptus has {0} wounds".format(adeptus_wounds[character["Adeptus"]]))
    max_wounds = adeptus_wounds[character["Adeptus"]] + roll(1, 5, character["Name"])
    print("You have {0} wounds.".format(max_wounds))
    return max_wounds


def get_characteristics(character: dict):
    print("\n\tCharacteristics are crucial part of the game. They determine the results of evasion, fleeing, avoiding "
          "traps. Meanwhile, bonus of your characteristic\n(characteristic divided by 10) affects your damage. "
          "The Characteristics your character has propensities for are equal to 30 + 3k10 dice rolls,\nwhile others "
          " are equal to 30 + 2k10 dice rolls.\n\nCalculating stats...")
    characteristics = {}
    if character["Adeptus"] == "Adeptus Astra Telepathica":
        characteristics = {
            "Intellect": 30 + roll(3, 10, character["Name"]),
            "Strength": 30 + roll(2, 10, character["Name"]),
            "Toughness": 30 + roll(2, 10, character["Name"]),
            "Agility": 30 + roll(2, 10, character["Name"])
        }
    elif character["Adeptus"] == "Adeptus Astra Militarum":
        characteristics = {
            "Intellect": 30 + roll(2, 10, character["Name"]),
            "Strength": 30 + roll(3, 10, character["Name"]),
            "Toughness": 30 + roll(3, 10, character["Name"]),
            "Agility": 30 + roll(2, 10, character["Name"])
        }
    elif character["Adeptus"] == "Adeptus Mechanicus":
        characteristics = {
            "Intellect": 30 + roll(3, 10, character["Name"]),
            "Strength": 30 + roll(3, 10, character["Name"]),
            "Toughness": 30 + roll(3, 10, character["Name"]),
            "Agility": 30 + roll(3, 10, character["Name"])
        }
    else:
        characteristics = {
            "Intellect": 30 + roll(2, 10, character["Name"]),
            "Strength": 30 + roll(2, 10, character["Name"]),
            "Toughness": 30 + roll(2, 10, character["Name"]),
            "Agility": 30 + roll(3, 10, character["Name"])
        }
    print_dictionary_items(characteristics)
    return characteristics


def get_skills(character: dict):
    """

    :param character:
    :return:

    >>> d = {"Skills": {}, "Adeptus": "Adeptus Astra Telepathica"}
    >>> get_skills(d)
    >>> print(d)
    """
    dictionary_of_skills = {
        "Adeptus Astra Telepathica": (
            "Lightning", "A bolt of blinding lightning strikes from your hand dealing 2k10 damage."),
        "Adeptus Astra Militarum": (
            "Colossus Smash", "A devastating blow of your weapon that deals (1k10 + Strength Bonus) damage."),
        "Adeptus Mechanicus": (
            "Laser Shot", "Your servo-skull shots a laser beam from its eyes dealing Intellect Bonus damage."),
        "Adeptus Officio Assassinorum": (
            "Deadly Burst", "You give your foe a burst of fire from two plasma-pistols dealing"
            " (5 + 1k10 + Agility Bonus) damage.")
    }
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


def has_evaded(enemy: dict):
    if roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Agility"]:
        print("{0} evaded the attack".format(enemy["Name"]))
        return True
    return False


def has_sustained(enemy: dict):
    if roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Toughness"]:
        print("{0} sustained the attack".format(enemy["Name"]))
        return True
    return False


def manage_wounds(damage: int, character: dict):
    if has_evaded(character):
        print("However, {0} evaded the attack.".format(character["Name"]))
    else:
        if has_sustained(character):
            character["Current wounds"] -= damage / 2
            print("However, {0} sustained the attack and receives only {1}".format(character["Name"], damage / 2))
        else:
            character["Current wounds"] -= damage


def lightning(character: dict, enemy: dict):
    damage = roll(2, 10, character["Name"])
    print("A bolt of blinding lightning strikes from {0}'s hand dealing {1} damage to the {2}.".format(
        character["Name"], damage, enemy["Name"]))
    return damage


def colossus_smash(character: dict, enemy: dict):
    damage = character["Characteristics"]["Strength"] + roll(1, 10, character["Name"])
    print("A devastating blow of {0} weapon rips the {1} that dealing {2} damage".format(
        character["Name"], enemy["Name"], damage))
    return damage


def laser_shot(character: dict, enemy: dict):
    damage = character["Characteristics"]["Intellect"]
    print("Your servo-skull shots a laser beam from its eyes dealing {0} damage to the {1}.".format(damage,
          enemy["Name"]))
    return damage


def deus_ex_machina(character: dict, enemy: dict):
    """
    Use random amount of random skills

    :param character:
    :param enemy:
    :return:
    """
    skills_list = [skill for skill in character["Skills"].keys()]
    skills_list = random.choices(skills_list, k=roll(1, 10, character["Name"]))
    for skill in skills_list:
        use_skill(character, skill, enemy)


def deadly_burst(character: dict, enemy: dict):
    damage = character["Characteristics"]["Agility"] + 5 + roll(1, 10, character["Name"])
    print("You give {0} a burst of fire from two plasma-pistols dealing {1} damage.".format(enemy["Name"], damage,))
    return damage


def flee_away(character: dict, enemy: dict):
    if roll(1, 100, character["Name"]) > character["Characteristics"]["Agility"]:
        use_skill(enemy, random.choice(list(enemy["Skills"].keys())[0::1]), character)
    character["Will to fight"] = False
    return 0


def enemy_attack(character: dict, enemy: dict):
    pass


def daemon_trickery(character, enemy):
    print("{0} dirtily makes another attack".format(character["Name"]))
    damage = sum(list(map(lambda number: number if number % 2 == 0 else 0, [roll(1, 10, character) for _ in range(5)])))
    print("{0} deals {1} damage to {2}".format(character["Name"], damage, enemy["Name"]))
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
        print(green_text() + key + normal_text() + ":", dictionary[key])


def roll(number_of_dice: int, number_of_sides: int, name: str):
    """

    :param number_of_dice:
    :param number_of_sides:
    :param name:
    :return:


    """
    list_of_rolls = [random.randrange(1, number_of_sides + 1) for _ in range(number_of_dice)]
    print("{0} rolled: {1}".format(name, list(itertools.chain(list_of_rolls))))
    print("The sum of {0} rolls is {1}".format(name, sum(list_of_rolls)))
    return sum(list_of_rolls)


def help_commands():
    """

    :return:

    >>> help_commands()

    """
    print("{0}h{1} —— show list of commands with a short description\n{0}q{1} —— quit the game\n{0}b{1} —— bandage your"
          "injuries and restore 3 wounds\n{0}s{1} —— show list of skills\nn{0}i{1} —— show inventory"
          .format(green_text(), normal_text()))


def get_command_list():
    commands_dictionary = ["h", "b", "s", "i"]
    return commands_dictionary


def has_argument(command: str):
    commands_dictionary = {"h": False, "b": True, "s": True}
    return commands_dictionary[command]


def get_command(command_name: str):
    """

    :param command_name:
    :return:
    """
    commands_dictionary = {"h": help_commands, "b": bandage, "s": show_list_of_skills,}
    return commands_dictionary[command_name]


def show_list_of_skills(character: dict):
    """

    :param character:
    """
    print("Right now you have the following skills:")
    print_dictionary_items(character["Skills"])


def use_skill(character: dict, skill_name: str, enemy: dict):
    skills_dictionary = {"Lightning": lightning, "Colossus Smash": colossus_smash, "Laser Shot": laser_shot,
                         "Deadly Burst": deadly_burst, "Flee Away": flee_away, "Enemy Attack": enemy_attack,
                         "Daemon's Trickery": daemon_trickery}
    return skills_dictionary[skill_name](character, enemy)


def reached_new_level(character: dict):
    if character["Level"] == 3:
        return False
    return character["Current experience"] >= character["Experience for the next level"]


def level_up(character: dict):
    dictionary_of_skills = {
        2: {
            "Adeptus Astra Telepathica":
                ("Spontaneous Combustion", "Your enemy ... dealing (Bonus Intellect)k10 damage.."),
            "Adeptus Astra Militarum":
                ("Charge", "... dealing (3 * Bonus Strength."),
            "Adeptus Mechanicus":
                ("Robotic Wrath", "Another runtime error infuriates your servitor and makes it destroy everything in "
                                  "its way dealing 3k(Bonus Intellect) damage"),
            "Adeptus Officio Assassinorum":
                ("Killer Instinct ", "You spray a fan of venomous knives dealing (Bonus Agility)k5 damage")
        },
        3: {
            "Adeptus Astra Telepathica":
                ("Chaos of Warp", "One is always equal in death. You make your enemy wounds equal to yours."),
            "Adeptus Astra Militarum":
                ("Rampage", "Those who live by the sword shall die by my blade. You make a series of bloodthirsty"
                            " slashes dealing (1k(Bonus Strength))k10 damage"),
            "Adeptus Mechanicus":
                ("Deus ex machina", "You pray Omnissiah to slay fools who cannot see the stupor mundi of machines."
                                    " You use 1k10 of your skills in one round. Skills are chosen randomly."),
            "Adeptus Officio Assassinorum":
                ("Vendetta", "You make a single fatal shot dealing 1k100 damage")
        }
    }
    dictionary_of_wounds = {
        2: {
            "Adeptus Astra Telepathica": 3,
            "Adeptus Astra Militarum": 10,
            "Adeptus Mechanicus": 7,
            "Adeptus Officio Assassinorum": 4
        },
        3: {
            "Adeptus Astra Telepathica": 3,
            "Adeptus Astra Militarum": 10,
            "Adeptus Mechanicus": 8,
            "Adeptus Officio Assassinorum": 5
        }
    }
    character["Level"] += 1
    if character["Level"] == 3:
        character["Experience for the next level"] = "Reached the maximum level."
    character["Experience for the next level"] *= 2
    character["Skills"].setdefault(dictionary_of_skills[character["Level"]][character["Adeptus"]][0],
                                   dictionary_of_skills[character["Level"]][character["Adeptus"]][1])
    character["Maximum wounds"] += dictionary_of_wounds[character["Level"]][character["Adeptus"]]
    character["Current wounds"] = character["Maximum wounds"]


def green_text():
    return "\x1b[1;32m"


def normal_text():
    return "\x1b[0;20m"


def bandage(character: dict):
    if character["Inventory"]["Bandage"] > 0:
        character["Current wounds"] += 4
        character["Inventory"]["Bandage"] -= 1
        show_wounds(character["Current wounds"], character["Maximum wounds"])
        print("{0} bandage{1} {2} left".format(
            character["Inventory"]["Bandage"],
            "s" if character["Inventory"]["Bandage"] > 1 else "",
            "are" if character["Inventory"]["Bandage"] > 1 else "is"
            )
        )
    else:
        print("You have no bandages")


def show_wounds(wounds, maximum_wounds):
    """

    :param wounds:
    :param maximum_wounds:

    >>> show_wounds(3, 25)
    Wounds: 3/25
    """
    print("Wounds: {0}/{1}".format(wounds, maximum_wounds))


def show_level(character: dict):
    print(
        "Level: {0}, {1}\n"
        "Experience: {2}/{3}".format(
            character["Level"][0],
            character["Level"][1],
            character["Current experience"],
            character["Experience for the next level"]
        )
    )


def describe_current_location(board: dict, coordinates: tuple):
    """
    Print the description of character's location.

    :param board: a dictionary
    :param coordinates: a tuple of positive integers
    :precondition: board must be a dictionary
    :precondition: coordinates must be positive integers
    :precondition: character values must be integers that are >= 0
    :precondition: board keys must have coordinates represented as tuple of two integers that are
                    >= 0
    :precondition: board values must have room's description as a string
    :postcondition: prints the description of character's location
    >>> describe_current_location({(0, 0): "This room is empty"}, (0, 0)
    <BLANKLINE>
    This room is empty
    """
    print("Current location is {0}.\n{1}".format(coordinates, board[coordinates]))


def get_available_directions(character: dict, columns: int, rows: int):
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

    >>> get_available_directions({"Y-coordinate": 0, "X-coordinate": 0}, 4, 4)
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


def validate_option(choice: str, list_of_options: list):
    """
    Validate option availability.

    :param choice: a string
    :param list_of_options: a list of strings
    :precondition: choice must be a string
    :precondition: available_directions must be a list
    :postcondition: returns False if choice is not a number
    :postcondition: returns False if choice - 1 is not in rage of available_direction length
    :postcondition: returns true otherwise
    :return: True if choice is valid, else False

    >>> validate_option("1", ["south", "east"])
    True
    >>> validate_option("0", ["south", "east"])
    False
    >>> validate_option("wait what", ["south", "east"])
    False
    """
    return choice.isnumeric() and (int(choice) - 1) in range(len(list_of_options))


def move_character(character: dict, direction_index: int, available_directions: list):
    """
    Change character's coordinates.

    :param character: a dictionary
    :param direction_index: a non-negative integer
    :param available_directions: a list of strings
    :precondition: character keys must contain "X-coordinate" and "Y-coordinate"
    :precondition: character values must be integers
    :precondition: direction_index must be a non-negative integer validated by validate_move function
    :precondition: availabe_directions each item must be either "north", "south", "east" or "west"
    :postcondition: updates character X or Y coordinate based on direction choice
    :return: new character's coordinates as a tuple

    >>> protagonist = {"X-coordinate": 0, "Y-coordinate": 0}
    >>> move_character(protagonist, 0, ["south", "west"])
    >>> print(protagonist)
    {'X-coordinate': 0, 'Y-coordinate': 1}
    """
    directions_dictionary = {"north": -1, "south": 1, "west": -1, "east": 1}
    direction = available_directions[direction_index]
    if direction in "north south":
        character["Y-coordinate"] += directions_dictionary[direction]
    else:
        character["X-coordinate"] += directions_dictionary[direction]
    return character["Y-coordinate"], character["X-coordinate"]


def is_goal_attained(character: dict):
    """
    Check if goal is attained.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :postcondition: returns True if character a Necronian artifact, else returns False
    :return: True if goal is attained, otherwise False

    >>> is_goal_attained({"Artifact": "Necronian Servo-Skull"})
    True
    >>> is_goal_attained({"Max wounds": 1000000000})
    False
    """
    return "Artifact" in character.keys()


def check_for_foes():
    """
    Check if foe is encountered.

    :postcondition: returns True with 25% probability, else returns False
    :return: True if foe is encountered, otherwise False
    """
    return random.randrange(0, 6) == 0


def generate_enemy(level):
    enemies_dictionary = {
        1:  # Level 1
        [
            {  # Template
                "Name": "",
                "Max wounds": 5,
                "Current wounds": 5,
                "Stats": {
                    "Intellect": 10,
                    "Strength": 15,
                    "Toughness": 15,
                    "Agility": 55
                },
                "Skills": {

                },
                "Will to fight": True
            },
            {  # Rat
                "Name": "Rat",
                "Max wounds": 5,
                "Current wounds": 5,
                "Stats": {
                    "Intellect": 10,
                    "Strength": 15,
                    "Toughness": 15,
                    "Agility": 25
                },
                "Skills": {
                    "Enemy Attack": "Rat greedily bites you with its front teeth"
                },
                "Will to fight": True
            },
        ]
    }
    return random.choices(enemies_dictionary[level], [0, 30], k=1)[0]


def is_alive(character: dict):
    """
    Determine if character is alive.
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character keys must contain "Current HP"
    :precondition: character values must be integers
    :postcondition: returns True if character's HP > 0, else return False
    :return: True if character is alive, otherwise False
    >>> is_alive({"Current wounds": 5})
    True
    >>> is_alive({"Current wounds": 0})
    False
    >>> is_alive({"Current wounds": -1})
    False
    """
    return character["Current wounds"] > 0


def get_map(board: dict, character: dict, columns: int, rows: int):
    """

    :param board:
    :param character:
    :param columns:
    :param rows:
    >>> print(get_map({(0, 0): "This room is empty", (0, 1): "This room is empty", (0, 2): "This room is empty", \
                (1, 0): "This room is empty", (1, 1): "This room is empty", (1, 2): ancient_altar_room}, \
                {"Y-coordinate": 0, "X-coordinate": 0}, 5, 5))

    """
    result = ""
    for row in range(rows):
        for column in range(columns):
            if (row, column) in board.keys() and (row, column) == \
                    (character["Y-coordinate"], character["X-coordinate"]):
                result += green_text() + "U" + normal_text() + " "
            elif (row, column) in board.keys() and board[(row, column)] == ancient_altar_room:
                result += green_text() + "+" + normal_text() + " "
            elif (row, column) not in board.keys():
                result += "*" + " "
            elif (row, column) in board.keys() and "empty" in board[(row, column)]:
                result += "e" + " "
        result += "\n"
    return result


def show_map(location_map):
    r"""

    :param location_map:

    >>> show_map("\x1b[1;32mU\x1b[0;20mee**\nee\x1b[1;32m+\x1b[0;20m**\n*****\n*****\n*****\n")

    """
    #  result = "".join(map(lambda ascii_character: " " if ascii_character == filter_element
    #                     else ascii_character, location_map))
    #  result = "".join([" " if letter == filter_element else letter for letter in location_map])
    print(location_map)
    print("* —— not discovered yet, + —— room with an altar, U —— your character, e —— an empty room"
          "█ ——")
    

def ancient_altar_room(character: dict):
    print("This room has an ancient altar. You feel strangely relaxed among this heresy. All your wounds are healed.")
    character["Current wounds"] = character["Maximum wounds"]


def tutorial():
    pass


def boss(character):
    if character["Level"][0] != 3:
        print("Fear takes control over you as soon as you get close to this room.\n"
              "You feel like you have to get more experience before facing it.\n You decide to retreat.")
        character["X-coordinate"] = 1
        character["Y-coordinate"] = 25
    else:
        print("You enter the dreadful room. The Necronian decor exactly matches the description the Inquisitor gave you"
              ". However, your joy deserves rapidly as you notice a gigantic daemon holding the precious artefact"
              "you are tasked to retrieve. The daemon notices you and smirks. His grotesque claws reveals his name"
              "Goreclaw the Render, a Daemon Prince of Khorne, infamous among the inquisitors of this galaxy."
              "\n\"Bring. It. On.\", his monstrous majesty mandates")
        enemy = {
            "Name": "Goreclaw the Render, a Daemon Prince of Khorne",
            "Max wounds": 100,
            "Current wounds": 100,
            "Stats": {
                "Intellect": 45,
                "Strength": 100,
                "Toughness": 70,
                "Agility": 5},
            "Skills": {
                "Daemon's Trickery": "20% to deal 5k10 damage, roll is counted to damage only if it's even",
                "Flame of Chaos": 0
            }
        }
        combat(character, enemy)

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
        "\n\nAll rights belong to Games Workshop.")
    time.sleep(2)
    print("\n\n\n{:^160}".format("Welcome to the nightmarish world of Warhammer 40k Dark Heresy"))
    print("\nPlease type {0}s{1} to start the game:".format(green_text(), normal_text()))
    print("You may desert anytime by typing {0}q{1}.".format(green_text(), normal_text()))
    if str(input()) == 's':
        game()


if __name__ == '__main__':
    main()
