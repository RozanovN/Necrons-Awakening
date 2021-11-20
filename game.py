"""
Your name:
Your student number:

All of your code must go in this file.
rework characteristics
"""
import random
import time
import itertools
import math


def game() -> None:
    """
    Drive the game.

    """
    rows = 25
    columns = 25
    print("\tYou stand on the front line of a great and secret war. As an Acolyte of the powerful"
          " Inquisition, you will root out threats to the Imperium of Man. You will engage\nin deadly combat"
          " against heretics, aliens and witches."
          "\n\tBut perhaps the biggest threat you face is your fellow man, for the human soul is such "
          "fertile ground for corruption. It is your duty to shepherd mankind from the\nmanifold paths"
          " of damnation.\n"
          "\n\tPrior to starting your service to the Emperor, you must first create a character.\n")
    character = character_creation()
    board = {
        (0, 0):
            tutorial(character),
        (25, 0):
            boss
    }
    board[(0, 0)] = "Entrance"
    while is_alive(character) and not is_goal_attained(character):
        available_directions = get_available_directions(character, rows, columns)
        print("\nWhere would you like to go?")
        print_numbered_list_of_possibilities(available_directions)
        user_input = int(process_input(character, available_directions)) - 1
        add_room_to_the_board(move_character(character, user_input, available_directions), board)
        show_map(get_map(board, character, columns, rows))
        show_wounds(character["Current wounds"], character["Max wounds"])
        show_level(character)
        manage_events(board, character)
        time.sleep(1)
        if check_for_foes():
            enemy = generate_enemy(character["Level"][0])
            combat(character, enemy)  # Combat begins
        if reached_new_level(character):
            time.sleep(1)
            level_up(character)
    game_over(character)


def combat(character: dict, enemy: dict) -> None:
    """
    Drive the combat.

    :param character: a dictionary
    :param enemy: a dictionary
    :precondition: character must be a dictionary
    :precondition: character keys must contain the following strings: Current wounds, Will to Fight, Skills, Current
                   experience, Max wounds, Name, Characteristics, Inventory
    :precondition: character value with key Current wounds must be an integer
    :precondition: character value with key Will to fight must be a boolean
    :precondition: character value with key Skills must contain a dictionary with strings as keys and function
                   references as values
    :precondition: character value with key Current experience must contain an integer
    :precondition: character value with key Max wounds must be an integer
    :precondition: character value with key Name must be a string
    :precondition: character value with key Characteristics must be a dictionary with strings as keys and integers as
                   values
    :precondition: character value with key Inventory must be a dictionary  with strings as keys and integers as values
    :precondition: enemy must be a dictionary
    :precondition: enemy keys must contain the following strings: Current wounds, Will to Fight, Skills,
                   Experience, Name, Characteristics
    :precondition: enemy value with key Current wounds must be an integer
    :precondition: enemy value with key Will to fight must be a boolean
    :precondition: enemy value with key Skills must contain a dictionary with at least 2 pairs, strings as keys and
                   function references as values
    :precondition: enemy value with key Experience must contain an integer
    :precondition: enemy value with key Name must be a string
    :precondition: enemy value with key Characteristics must be a dictionary with strings as keys and integers as
                   values
    :postcondition: battle ends if character wounds is <= zero or if character decides to flee.
    :postcondition: battle ends if enemy wounds is <= zero or if enemy decides to flee.
    :postcondition: character receives full experience if enemy is killed, half experience if enemy flees, else none
    """
    print("\nCombat between {0} and {1} begins.".format(character["Name"], enemy["Name"]))
    while is_alive(character) and is_alive(enemy) and enemy["Will to fight"]:
        show_wounds(character["Current wounds"], character["Max wounds"])
        print_numbered_list_of_possibilities(list(character["Skills"].keys()))
        user_input = int(process_input(character, list(character["Skills"].keys()))) - 1
        damage = use_skill(character, list(character["Skills"].keys())[user_input], enemy)  # player's turn
        if not character["Will to fight"]:
            break
        manage_wounds(damage, enemy)
        damage = use_skill(enemy, random.choice(list(enemy["Skills"].keys())[1::]), character)  # enemy's turn
        manage_wounds(damage, character)
        if random.randrange(1, 6) == 1:
            use_skill(enemy, list(enemy["Skills"].keys())[0], character)  # Enemy fleeing, boss' additional attack
    if is_alive(character) and character["Will to fight"]:
        character["Current experience"] += enemy["Experience"] if enemy["Will to fight"] else math.floor(
                                           enemy["Experience"] / 2)
    if not character["Will to fight"]:
        move_character(character)
    time.sleep(2)
    print("\nThe battle is over.")
    show_level(character)
    character["Will to fight"] = True


def add_room_to_the_board(coordinates: tuple, board: dict) -> None:
    """
    Add a room to the board if the board doesn't have a room at the given coordinates.

    :param board: a dictionary
    :param coordinates: tuple of positive integers
    :precondition: board must be a dictionary
    :precondition: board keys must be tuples of integers
    :precondition: coordinates items must be positive integers
    :postcondition: Adds a room with a list with a random event and a boolean that is equal to False
                    to the board if the board doesn't have a room at the given coordinates
    :postcondition:
    """
    if coordinates not in board.keys():
        board.setdefault(coordinates, generate_random_room_event(),)


def generate_random_room_event() -> str:
    """
    Generate a random room event.

    This is a helper function for add_room_to_the_board function.

    :postcondition: returns a random event name for a room from the list of events.
    :return: the event's name as a string
    """
    list_of_events = [
        "Empty Room",
        "Ancient Altar Room",
        "Crate",
        "Eldritch Altar",
        "Stack of Books",
        "Discarded Pack",
        "Necronian Chest",
        "Necronian Alchemy Table",
        "Decorative Urn",
        "Iron Maiden",
        "Locked Sarcophagus",
        "Suit of Armor",
        "Makeshift Dining Table",
        "Pile of Bones",
        "Eerie Spiderweb",
        "Mummified Remains",
        "Transcendent Terror",
        "Iron Crown",
        "Ceiling Drops",
        "Shifting Mist"
        ]
    return random.choices(list_of_events, weights=[5, 1, 3, 1, 2, 3, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], k=1)[0]


def process_input(character=None, list_of_options=None, is_setting_name=False) -> str:
    """

    :param character:
    :param list_of_options:
    :param is_setting_name:
    :return:
    """
    user_input = str(input())
    input_is_processed = True
    while input_is_processed:
        if validate_option(user_input, list_of_options):
            return user_input
        elif user_input in get_command_list():
            process_command(user_input, character)
        elif is_setting_name and user_input != "":
            return user_input
        else:
            print("{0} is invalid input. Please, try again:".format(user_input))
        user_input = str(input())


def character_creation() -> dict:
    """
    Create character

    :postcondition: creates a character
    :return: character as a dictionary
    """
    character = {
        "Name": set_name(),
        "Adeptus": None,
        "Max wounds": 0,
        "Current wounds": 0,
        "Characteristics": {},
        "Level": (1, None),
        "Skills": {
            "Flee Away": "You retreat to the previous room"},
        "X-coordinate": 0,
        "Y-coordinate": 0,
        "Previous coordinates": (0, 0),
        "Current experience": 0,
        "Experience for the next level": 1000,
        "Will to fight": True,
        "Inventory": {
            "Bandage": 10,
            "Torch": 10
        }
    }
    character["Adeptus"] = set_adeptus(character)
    character["Max wounds"] = set_wounds(character)
    character["Current wounds"] = character["Max wounds"]
    time.sleep(3)
    character["Characteristics"] = get_characteristics(character)
    time.sleep(3)
    show_characteristics(character)
    time.sleep(3)
    get_skills(character)
    show_list_of_skills(character)
    time.sleep(3)
    character["Level"] = get_level_name(character["Adeptus"], character["Level"][0])
    show_level(character)
    return character


def set_name():
    """


    :return:
    """
    print("Enter your name:")
    name = process_input({}, [], True)
    return name


def set_adeptus(character) -> str:
    """

    :param character:
    :return:
    """
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
        "lightnings. Psykers' might comes from the warp and the Gods of Chaos. Psykers are physically weak and barely "
        "agile, instead\nthey focus on their mind's strength. However, the true Achilles heel of psykers is their own"
        " outrageous power. Indeed, to toy with warp is to perform before the Gods of\nChaos; they love the show until "
        "they see a single failure.\n"
        
        "\tAdeptus Astra Militarum is an adeptus of powerful warriors. They specialize in brute force and close "
        "combat. They are the brave souls that lead the Emperor's\nconquest. Those soldiers are strong and though,"
        " yet lack in agility. As for intellect, one only needs to follow orders.\n"
        
        "\tAdeptus Mechanicus is an adeptus of clever engineers. They specialize in machinery and fight with help of "
        "their servo-skulls and dreadful servitors. Mechanics believe in\nthe supremacy of their Machine God —— "
        "Omnissiah  —— and eagerly reject their own weak flesh to get the divine bionic one. As a result, they end "
        "up looking more robotic than\ntheir own machines. The dire engineers despise involving themselves into "
        "battles, despite "
        "having foremost strength and dexterity due to their mechanical prostheses.\nInstead, they play their battles "
        "as though they play a game of chess. Thus, the only thing they need is the power of their brain.\n"
        
        "\tAdeptus Officio Assassinorum is an \"elite\" adepta of rogues and hitmen. Inquisitors recruit the most "
        "menacing and terrifying ones to make them acolytes. Those\nassassins are extremely agile, even if they lack "
        "in strength. Preferring the range combat, the best of them are elusive ghosts to their enemies."
        "\n\nPlease, choose your adeptus carefully.")

    adepts_list = ["Adeptus Astra Telepathica", "Adeptus Astra Militarum", "Adeptus Mechanicus", "Adeptus Officio"
                   " Assassinorum"]
    print("To choose an adeptus, enter its index from the numbered list.")
    print_numbered_list_of_possibilities(adepts_list)
    choice = process_input(character, adepts_list)
    return adepts_list[int(choice) - 1]


def set_wounds(character: dict) -> int:
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
    time.sleep(4)
    return max_wounds


def get_characteristics(character: dict) -> dict:
    print("\n\tCharacteristics are crucial part of the game. They determine the results of evasion, fleeing, avoiding "
          "traps. Meanwhile, bonus of your characteristic\n(first digit of the characteristic) affects your damage. "
          "The Characteristics your character has propensities for are equal to 30 + 3k10 dice rolls,\nwhile others "
          " are equal to 30 + 2k10 dice rolls.\n\nCalculating stats...")
    time.sleep(4)
    characteristics_dictionary = {
        "Adeptus Astra Telepathica": [
            (30, 3),
            (30, 2),
            (30, 2),
            (30, 2),
        ],
        "Adeptus Astra Militarum": [
            (30, 2),
            (30, 3),
            (30, 3),
            (30, 2),
        ],
        "Adeptus Mechanicus": [
            (30, 3),
            (30, 3),
            (30, 3),
            (30, 3),
        ],
        "Adeptus Officio Assassinorum": [
            (30, 2),
            (30, 2),
            (30, 2),
            (30, 3),
        ]
    }
    characteristics = {
        "Intellect": characteristics_dictionary[character["Adeptus"]][0][0] +
                     roll(characteristics_dictionary[character["Adeptus"]][0][1], 10, character["Name"]),
        "Strength": characteristics_dictionary[character["Adeptus"]][1][0] +
                     roll(characteristics_dictionary[character["Adeptus"]][1][1], 10, character["Name"]),
        "Toughness": characteristics_dictionary[character["Adeptus"]][2][0] +
                     roll(characteristics_dictionary[character["Adeptus"]][2][1], 10, character["Name"]),
        "Agility": characteristics_dictionary[character["Adeptus"]][3][0] +
                     roll(characteristics_dictionary[character["Adeptus"]][3][1], 10, character["Name"])
    }
    return characteristics


def get_skills(character: dict) -> None:
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


def has_evaded(enemy: dict) -> bool:
    return roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Agility"]


def has_sustained(enemy: dict) -> bool:
    return roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Toughness"]


def manage_wounds(damage: int, enemy: dict) -> None:
    if has_evaded(enemy):
        print("However, {0} evades it.".format(enemy["Name"]))
    else:
        print("{0} was not able to evade.".format(enemy["Name"]))
        time.sleep(2)
        if has_sustained(enemy):
            damage = math.floor(damage / 2)
            enemy["Current wounds"] -= damage
            print("However, {0} sustains it and receives only {1}.".format(enemy["Name"], damage))
        else:
            time.sleep(2)
            print("{0} was not able to sustain.".format(enemy["Name"]))
            enemy["Current wounds"] -= damage


def lightning(character: dict, enemy: dict) -> int:
    damage = roll(2, 10, character["Name"])
    print("\nA bolt of blinding lightning strikes from {0}'s hand dealing {1} damage to {2}.".format(
        character["Name"], damage, enemy["Name"]))
    return damage


def spontaneous_combustion(character: dict, enemy: dict) -> int:
    damage = roll(math.floor(character["Characteristics"]["Intellect"]), 10, character["Name"])
    print("\nThe power of your mind ignites {0} dealing {1} damage.".format(enemy["Name"], damage))
    return damage


def chaos_of_warp(character: dict, enemy: dict) -> int:
    enemy["Max wounds"] = character["Max wounds"]
    enemy["Current wounds"] = enemy["Max wounds"]
    print("\nYou make {0}'s wounds equal to {1}.".format(enemy["Name"], enemy["Current wounds"]))
    return 0


def colossus_smash(character: dict, enemy: dict) -> int:
    damage = math.floor(character["Characteristics"]["Strength"] / 10) + roll(1, 10, character["Name"])
    print("\nA devastating blow of {0} weapon rips and tears {1} dealing {2} damage\n".format(
        character["Name"], enemy["Name"], damage))
    return damage


def charge(character: dict, enemy: dict) -> int:
    damage = math.floor(character["Characteristics"]["Strength"] / 10) * 3
    print("\n{0}'s enormous body charges into {1} dealing {2} damage\n".format(
        character["Name"], enemy["Name"], damage))
    return damage


def rampage(character: dict, enemy: dict) -> int:
    damage = roll(roll(1, math.floor(character["Characteristics"]["Strength"] / 10), character["Name"]), 10,
                  character["Name"])
    print("\n{0} makes a series of bloodthirsty slashes dealing {1} damage\n".format(
        character["Name"], damage))
    return damage


def laser_shot(character: dict, enemy: dict) -> int:
    damage = math.floor(character["Characteristics"]["Intellect"] / 10)
    print("\nYour servo-skull shots a laser beam from its eyes dealing {0} damage to {1}.".format(damage, enemy["Name"]))
    return damage


def robotic_wrath(character: dict, enemy: dict) -> int:
    damage = roll(3, math.floor(character["Characteristics"]["Intellect"] / 10), character["Name"])
    print("\n\"TRACEBACK (MOST RECENT CALL LAST):\n FILE C:/SERVITOR/BRAIN/COMBAT/ATTACK.py LINE 42, IN <module>\n"
          "ZERO DIVISION ERROR: DIVISION BY ZERO\n"
          "[FINISHED IN 0.314s WITH EXIT CODE ROBOTIC WRATH]\""
          " —— your Servitor roars robotically."
          "\nThe enraged servitor destroys everything in the way dealing {0} damage to {1}.".format(damage,
                                                                                                    enemy["Name"]))
    return damage


def deus_ex_machina(character: dict, enemy: dict) -> int:
    """
    Use random amount of random skills

    :param character:
    :param enemy:
    :return:
    """
    skills_list = [skill for skill in character["Skills"].keys()]
    skills_list = random.choices(skills_list, k=roll(1, 10, character["Name"]))
    damage = 0
    print("\nYou pray Omnissiah to slay fools who cannot see the stupor mundi of machines.")
    for skill in skills_list:
        damage += use_skill(character, skill, enemy)
    return damage


def deadly_burst(character: dict, enemy: dict) -> int:
    damage = math.floor(character["Characteristics"]["Agility"] / 10) + 5 + roll(1, 10, character["Name"])
    print("\nYou give {0} a burst of fire from two plasma-pistols dealing {1} damage.".format(enemy["Name"], damage))
    return damage


def killer_instinct(character: dict, enemy: dict) -> int:
    damage = roll(math.floor(character["Characteristics"]["Agility"] / 10), 5, character["Name"])
    print("\nYou spray a fan of venomous knives dealing dealing {0} damage to {1}.".format(damage, enemy["Name"]))
    return damage


def vendetta(character: dict, enemy: dict) -> int:
    damage = roll(1, 100, character["Name"])
    print("\nYour fatal shot deals {0} damage to {1}.".format(damage, enemy["Name"]))
    if damage < 20:
        print("V means very random.")
    return damage


def flee_away(character: dict, enemy: dict) -> 0:
    print("\n{0} decides to flee away".format(character["Name"]))
    if roll(1, 100, character["Name"]) > character["Characteristics"]["Agility"]:
        print("{0} is not quick enough to flee without damage.".format(character["Name"]))
        use_skill(enemy, random.choice(list(enemy["Skills"].keys())[0::1]), character)
    else:
        print("{0} flees without damage.".format(character["Name"]))
    character["Will to fight"] = False
    return 0


def enemy_attack(character: dict, enemy: dict) -> int:
    damage = roll(character["Skills"]["Enemy Attack"][1],
                  character["Skills"]["Enemy Attack"][2], character["Name"])
    print("\n" + character["Skills"]["Enemy Attack"][0] + " dealing {0}".format(damage))
    return damage


def daemon_trickery(character: dict, enemy: dict) -> int:
    """
    Use Daemon Trickery skill

    Roll is counted toward damage only if it's an even number.

    :param character:
    :param enemy:
    :return:
    """
    print("\n{0} dirtily makes another attack".format(character["Name"]))
    damage = sum(list(map(lambda number: number if number % 2 == 0 else 0, [roll(1, 10, character["Name"]) for _ in
                                                                            range(5)])))
    print("{0} deals {1} damage to {2}".format(character["Name"], damage, enemy["Name"]))
    return damage


def blade_of_chaos(character: dict, enemy: dict):
    print("\nYou notice how this fiend of Khorne prepares a slash attack. You have an opportunity to deflect it if you"
          "guess the 2 body parts he aims for H(head), B(body), A(arms), F(feet). He certainly will not be able to"
          "evade or sustain it."
          "\nEnter the first letters of 2 body parts (AB for arms and body):")
    correct_answer = random.choice(list(itertools.combinations("HBAF", 2)))
    correct_answer = [correct_answer, correct_answer[::-1]]
    if str(input()).replace(" ", "").upper() in correct_answer:
        print("Success! Who is smirking now?")
        character["Current wounds"] -= 8
        return 0
    print("Failure! The Daemon smirks and deals {0} to {1}".format(8, enemy["Name"]))
    return 8


def print_numbered_list_of_possibilities(list_of_options: list) -> None:
    """
    Prints a numbered list of options

    :param list_of_options: a non-empty list

    >>> print_numbered_list_of_possibilities(["south", "east"])
    1 south
    2 east
    """
    for index, option_name in enumerate(list_of_options, 1):
        print(green_text() + str(index) + normal_text(), option_name)


def print_dictionary_items(dictionary: dict) -> None:
    """

    :param dictionary:

    >>> print_dictionary_items({"a": 1})

    """
    for key in dictionary.keys():
        print(green_text() + key + normal_text() + ":", dictionary[key])


def roll(number_of_dice: int, number_of_sides: int, name: str) -> int:
    """

    :param number_of_dice:
    :param number_of_sides:
    :param name:
    :return:


    """
    list_of_rolls = [random.randrange(1, number_of_sides + 1) for _ in range(number_of_dice)]
    print("\n{0} rolled:".format(name))
    for single_roll in list_of_rolls:
        time.sleep(1)
        print("{0}{1}{2}".format(single_roll, green_text(), normal_text()))
    print("The sum of {0} rolls is {1}{2}{3}".format(name, green_text(), sum(list_of_rolls), normal_text()))
    return sum(list_of_rolls)


def help_commands():
    """

    :return:

    >>> help_commands()

    """
    print("\nThis is the list of the available commands:\n"
          "{0}h{1} —— show list of commands with a short description\n"
          "{0}q{1} —— quit the game\n"
          "{0}b{1} —— bandage your injuries and restore 4 wounds\n"
          "{0}s{1} —— show list of your skills\n"
          "{0}c{1} —— show your characteristics\n"
          "{0}i{1} —— show your inventory\n"
          .format(green_text(), normal_text()))


def get_command_list() -> list:
    commands_list = ["q", "h", "b", "s", "i", "c"]
    return commands_list


def has_argument(command: str) -> bool:
    commands_dictionary = {
        "q": False,
        "h": False,
        "b": True,
        "s": True,
        "i": True,
        "c": True
    }
    return commands_dictionary[command]


def get_command(command_name: str):
    """

    :param command_name:
    :return:
    """
    commands_dictionary = {
        "q": quit_game,
        "h": help_commands,
        "b": bandage,
        "s": show_list_of_skills,
        "i": show_inventory,
        "c": show_characteristics}
    return commands_dictionary[command_name]


def show_list_of_skills(character: dict) -> None:
    """

    :param character:
    """
    print("\nRight now you have the following skills:")
    print_dictionary_items(character["Skills"])


def use_skill(character: dict, skill_name: str, enemy: dict) -> int:
    skills_dictionary = {"Lightning": lightning, "Colossus Smash": colossus_smash, "Laser Shot": laser_shot,
                         "Deadly Burst": deadly_burst, "Flee Away": flee_away, "Enemy Attack": enemy_attack,
                         "Daemon's Trickery": daemon_trickery, "Spontaneous Combustion": spontaneous_combustion,
                         "Charge": charge, "Robotic Wrath": robotic_wrath, "Killer Instinct": killer_instinct,
                         "Chaos of Warp": chaos_of_warp, "Rampage": rampage, "Deus ex machina": deus_ex_machina,
                         "Vendetta": vendetta}
    return skills_dictionary[skill_name](character, enemy)


def reached_new_level(character: dict) -> bool:
    if character["Level"] == 3:
        return False
    return character["Current experience"] >= character["Experience for the next level"]


def level_up(character: dict) -> None:
    dictionary_of_skills = {
        2: {
            "Adeptus Astra Telepathica":
                ("Spontaneous Combustion", "The power of your mind ignites your enemy dealing (Bonus Intellect)k10"
                                           " damage."),
            "Adeptus Astra Militarum":
                ("Charge", "You charge into your enemy dealing (3 * Bonus Strength) damage. Prosaically, yet effective"
                           ""),
            "Adeptus Mechanicus":
                ("Robotic Wrath", "Another runtime error infuriates your servitor and makes it destroy everything in "
                                  "its way dealing 3k(Bonus Intellect) damage"),
            "Adeptus Officio Assassinorum":
                ("Killer Instinct", "You spray a fan of venomous knives dealing (Bonus Agility)k5 damage")
        },
        3: {
            "Adeptus Astra Telepathica":
                ("Chaos of Warp", "One is always equal in death. You make your enemy wounds equal to yours."),
            "Adeptus Astra Militarum":
                ("Rampage", "Those who live by the sword shall die by your blade.\nYou make a series of bloodthirsty"
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
    print("\nYou reached new level.")
    character["Level"] += 1
    if character["Level"] == 3:
        character["Experience for the next level"] = "Reached the maximum level."
    character["Experience for the next level"] *= 2
    character["Skills"].setdefault(dictionary_of_skills[character["Level"]][character["Adeptus"]][0],
                                   dictionary_of_skills[character["Level"]][character["Adeptus"]][1])
    character["Maximum wounds"] += dictionary_of_wounds[character["Level"]][character["Adeptus"]]
    character["Current wounds"] = character["Maximum wounds"]
    get_level_name(character["Adeptus"], character["Level"][0])


def green_text() -> str:
    return "\x1b[1;32m"


def normal_text() -> str:
    return "\x1b[0;20m"


def bandage(character: dict) -> None:
    if has_item("Bandage", character):
        character["Current wounds"] = character["Current wounds"] + 4 if character["Current wounds"] != \
            character["Max wounds"] else character["Max wounds"]
        character["Inventory"]["Bandage"] -= 1
        show_wounds(character["Current wounds"], character["Max wounds"])
        print("{0} bandage{1} {2} left".format(character["Inventory"]["Bandage"],
                                               "s" if character["Inventory"]["Bandage"] > 1 else "",
                                               "are" if character["Inventory"]["Bandage"] > 1 else "is"))
    else:
        print("You have no bandages")


def show_wounds(wounds, maximum_wounds) -> None:
    """

    :param wounds:
    :param maximum_wounds:

    >>> show_wounds(3, 25)
    <BLANKLINE>
    Wounds: 3/25
    """
    print("\nWounds: {0}/{1}".format(wounds, maximum_wounds))


def show_level(character: dict) -> None:
    print(
        "\nLevel: {0}, {1}\n"
        "Experience: {2}/{3}".format(
            character["Level"][0],
            character["Level"][1],
            character["Current experience"],
            character["Experience for the next level"]
        )
    )


def show_inventory(character: dict) -> None:
    print("You have the following items:")
    print("Item name: Amount of items")
    print_dictionary_items(character["Inventory"])


def show_characteristics(character):
    """

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character keys must contain Characteristics string
    :precondition: Characteristics value must be a dictionary
    :precondition: Characteristics value keys must be strings with integer values
    :postcondition: prints character's characteristics

    >>> show_characteristics({"Characteristics": {"Intellect: 30"}})

    """
    print("\nYour characteristics are:")
    print_dictionary_items(character["Characteristics"])


def quit_game() -> None:
    print("\nYou may deserve now, but your duty to the Emperor will last forever.")
    quit()


def manage_events(board: dict, character: dict) -> None:
    """
    Print the description of character's location.

    :param board: a dictionary
    :param character: a tuple of positive integers
    :precondition: board must be a dictionary
    :precondition: coordinates must be positive integers
    :precondition: character values must be integers that are >= 0
    :precondition: board keys must have coordinates represented as tuple of two integers that are
                    >= 0
    :precondition: board values must have room's description as a string
    :postcondition: prints the description of character's location
    >>>
    <BLANKLINE>
    This room is empty
    """
    events_dictionary = {
        "Entrance": {
            "Description": [
                "This is the entrance to the tomb."
            ]
        },
        "There is nothing here anymore": {
            "Description": [
                "There is nothing here anymore"
            ]
        },
        "Empty Room": {
            "Description": [
                "This room is empty", "The emptiness of this room reminds you nothing of necrons.",
                "This room torchers you with its boredom and emptiness."
            ]
        },
        "Ancient Altar Room": {
            "Description": [
                "This room has an ancient altar. You feel strangely relaxed among this heresy.",
                "All your wounds are healed.", "This room has an ancient altar. Despite its blasphemous appearance,"
                " it heals you innocently still."
            ],
            "Effect": "Heal"
        },
        "Crate": {
            "After-effect": False,
            "Description": [
                "This room has a large crate.",
                "This room has a strange crate."
            ],
            "Input": {
                "Description": "Would you like to open it?",
                "Yes": {
                    "Effect": [
                        ("Torch", "You find a torch."),
                        ("Bandage", "You find a bandage.")
                    ],
                },
                "No": {
                    "Item": [
                        ("Torch", "As you leave, you find a torch on the floor."),
                        ("Bandage", "As you leave, you find a bandage on the floor")
                    ]
                }
             }
        },
        "Eldritch Altar": {
            "Description": [
                "This room has an ominous altar.",
                "This room has an altar in form of a star that pierces a crescent moon, reminding you of Slaanesh",
            ],
            "Input": {
                "Description": "Would you like to to touch it?",
                "Yes": {
                    "Effect": [
                        ("Damage", "This altar tortures your mind and takes away 4 of your wounds."),
                        ("Random Stat Improvement", "This altar tortures your mind, yet makes you stronger.")
                    ],
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You have no time for such heresy."),
                    ]
                }
             }
        },
        "Stack of Books": {
             "After-effect": False,
             "Description": [
                 "This room has a stack of heretic books.",
                 "This room has a stack of Imperium's books, which seems strange to you.",
             ],
             "Input": {
                "Description": "Would you like to read one?",
                "Yes": {
                    "Effect": [
                        ("Damage", "This damned heresy poisons your mind and takes away 4 of your wounds."),
                        ("Experience gain", "You find some useful knowledge from Necrons. Current experience + 50.")
                    ],
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You have no time for this nonsense.")
                    ]
                }
             }
         },
        "Discarded Pack": {
             "After-effect": False,
             "Description": [
                 "This room has a discarded pack left by your predecessor.",
                 "This room has a big but miserable, discarded pack."
             ],
             "Input": {
                "Description": "Would you like to open it?",
                "Yes": {
                    "Item": [
                        ("Torch", "You find a torch."),
                        ("Bandage",  "You find a bandage."),
                        ("Shovel", "You find a shovel.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You are here for the artifact and not for looting, right?")
                    ]
                }
             }
         },
        "Necronian Chest": {
             "After-effect": False,
             "Description": [
                 "This room has a mechanical Necronian chest.",
                 "This room has a chest made of green steel."
             ],
             "Input": {
                "Description": "Would you like to open it?",
                "Yes": {
                    "Item": [
                        ("Armor", "You find a ring with C'tan insignia. Your wounds are increased by 2."),
                        ("Broken Armor",  "You find a ring, but its insignia was diligently erased. "
                                          "Your wounds are increased by 1."),
                        ("Shovel", "You find a simple shovel..")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You are here for the artifact and not for looting, right?")
                    ]
                }
             }
         },
        "Necronian Alchemy Table": {
            "After-effect": False,
            "Description": [
                "This room has a Necronian alchemy table with food on it.",
                "This room has a potion standing on some kind of alchemy pentagram.",
                "This room has a myriad of bulbs and flasks."
            ],
            "Input": {
                "Description": "Would you like to taste it?",
                "Yes": {
                    "Effect": [
                        ("Nothing", "It has no effect."),
                        ("Damage", "It wasn't delicious. Such bitterness takes away 4 of your wounds."),
                        ("Random Stat Improvement", "Mens sana in corpore sano.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You are not hungry anyway.")
                    ]
                }
            }
         },
        "Decorative Urn": {
            "After-effect": False,
            "Description": [
                "This room has a marble, giant urn.",
                "This room has multiple broken urns."
            ],
            "Input": {
                "Description": "Would you like to look for anything?",
                "Yes": {
                    "Item": [
                        ("Armor", "Inside you find a necklace enchanted with psykana that increases your wounds by 2."),
                        ("Broken Armor", "You find a broken piece of mechanical bracelet. Your wounds are increased "
                                         "by 1."),
                        ("Torch", "You find a torch."),
                        ("Bandage", "You find a bandage."),
                        ("Shovel", "You find a shovel.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You decide not to wear anything")
                    ]
                }
            }
         },
        "Iron Maiden": {
            "After-effect": False,
            "Description": [
                "This room has a dreadful iron maiden.",
                "This room has mechanical cage in form of star."
            ],
            "Input": {
                "Description": "Would you like to look inside?",
                "Yes": {
                    "Effect": [
                        ("Damage", "As you open the torture mechanism, it sends a fan of knives that takes away 4 of "
                                   "your wounds")
                    ],
                    "Item": [
                        ("Armor", "Inside you find a set of mechanical armor that increases your wounds by 2."),
                        ("Broken Armor", "You find a set of worn out armor. Your wounds are increased by 1.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You decide not to disturb the dead.")
                    ]
                }
            }
         },
        "Locked Sarcophagus": {
            "After-effect": False,
            "Description": [
                "This room has a mysterious sarcophagus.",
                "This room is a necronian cemetery."
            ],
            "Input": {
                "Description": "Would you like to look inside?",
                "Yes": {
                    "Effect": [
                        ("Damage", "As you open the sarcophagus, a hidden blade cuts you and takes away 4 of your "
                                   "wounds")
                    ],
                    "Item": [
                        ("Armor", "Inside you find a set of mechanical armor that increases your wounds by 2."),
                        ("Broken Armor", "You find a set of clearly worn out armor. Your wounds are increased by 1.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You decide not to wear anything")
                    ]
                }
            }
         },
        "Suit of Armor": {
            "After-effect": False,
            "Description": [
                "This room is an armory.",
                "This room has a set of mechanical, ancient armor."
            ],
            "Input": {
                "Description": "Would you like to take some new armor pieces?",
                "Yes": {
                    "Item": [
                        ("Armor", "This blasphemous, mechanical armor increases your wounds by 2."),
                        ("Broken Armor", "This armor is broken; however, cursed psykana protects you nonetheless. "
                                         "Your wounds are increased by 1.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You decide not to wear anything")
                    ]
                }
            }
         },
        "Makeshift Dining Table": {
            "After-effect": False,
            "Description": [
                "This room has a makeshift dining table with food on it.",
                "This room has a package of uneaten food.",
                "This room has some vases of water."
            ],
            "Input": {
                "Description": "Would you like to taste it?",
                "Yes": {
                    "Effect": [
                        ("Damage", "Necronian cuisine is not the best. It takes 4 of your wounds."),
                        ("Random Stat Deterioration", "This accursed cuisine has surely influenced your organism.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You are not hungry anyway.")
                    ]
                }
            }
         },
        "Pile of Bones": {
            "Description": [
                "This room has a pile of robotic, countless bones.",
                "This room is full of robotic skulls",
                "This room a robotic skeleton sitting on a throne."
            ],
            "Effect": [
                ("Nothing", "Dead men remain dead"),
                ("Battle", 2, "the Necronian skeleton", "Those sitting bones would like to see you dead as well.")
            ],
         },
        "Eerie Spiderweb": {
            "After-effect": False,
            "Description": [
                "This room is full of eerie spiderweb.",
                "You struggle to see anything because of the spiderweb."
            ],
            "Input": {
                "Description": "Would you like to burn some of it with a torch?",
                "Yes": {
                    "Check item": "Torch",
                    "Effect": [
                        ("Damage", "A small spider managed to bite you and take away 4 of your wounds "
                                   "before burning to ashes."),
                        ("Nothing", "You burn down the web without any problems.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Damage", "A small spider bites while try to break through the web."),
                        ("Battle", 2, "the giant Spider", "A giant spider is not fond of your intrusion ")
                    ]
                }
            }
         },
        "Mummified Remains": {
            "After-effect": False,
            "Description": [
                "This is room is devoured by darkness.",
                "This room has no lightning."
            ],
            "Input": {
                "Description": "Would you like to use a torch?",
                "Yes": {
                    "Check item": "Torch",
                    "Effect": [
                        ("Damage", "Fire activates the trap which takes 4 of your wounds."),
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "Nothing happens, but you feel like someone eyeing you."),
                        ("Battle", 2, "the mummified Necron", "A mummified Necron awakes. You are clearly not welcomed "
                                                          "here.")
                    ]
                }
            }
         },
        "Transcendent Terror": {
            "Description": [
                "You feel the instability of the Realm of Souls.",
                "You feel the cosmic terror of this world.",
                "You hear the whispers from beyond."
            ],
            "Effect": [
                ("Damage", "This mental torture takes away 4 of your wounds"),
                ("Battle", 3, "the entity of the warp", "You encounter a terrible indescribable thing."
                                                     "A shapeless congeries of protoplasmic bubbles and myriads of "
                                                     "temporary eyes."),
                ("Random Stat Deterioration", "You are forever changed by this.")
            ],
         },
        "Iron Crown": {
            "After-effect": False,
            "Description": [
                "In this restless room you see a crown.",
                "An iron crown stands still on the green, marble pedestal."
            ],
            "Input": {
                "Description": "Would you like to wear it?",
                "Yes": {
                    "Item": [
                        ("Armor", "This cursed mechanical crown increases your wounds by 2."),
                        ("Broken Armor", "This crown is broken, yet powerful machinery protects you still. "
                                         "Your wounds are increased by 1.")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You decide not to wear anything")
                    ]
                }
            }
         },
        "Ceiling Drops": {
            "After-effect": True,
            "Description": [
                "As you enter this room, the ceiling above you drops. You were able to evade it, but now you need to go"
                " through this mess.",
                "Before you enter the next room you hear how its ceiling drops. now you need to go through this mess. "
            ],
            "Input": {
                "Description": "Would like to use a shovel?",
                "Yes": {
                    "Check item": "Shovel",
                    "Effect": [
                        ("Nothing", "You clear path without any problem."),
                    ]
                },
                "No": {
                    "Effect": [
                        ("Damage", "Without a shovel it takes a tremendous amount of effort and 4 of your wounds")
                    ]
                }
            }
         },
        "Shifting Mist": {
            "After-effect": False,
            "Description": [
                "This room has a strange shifting mist.",
                "You are unable to see anything because of the mist."
            ],
            "Input": {
                "Description": "Would you like to light a torch?",
                "Yes": {
                    "Check item": "Torch",
                    "Effect": [
                        ("Nothing", "You see clearly now"),
                        ("Damage", "As soon as you lit your torch, the mist explodes. It takes 4 of your wounds")
                    ]
                },
                "No": {
                    "Effect": [
                        ("Nothing", "You eventually find your way")
                    ]
                }
            }
         }
    }
    event = board[(character["Y-coordinate"], character["X-coordinate"])][0]
    if event[0] == boss:
        event[0](character)
    else:
        print(events_dictionary[event]["Description"])
        if "Input" in events_dictionary[event].keys():
            event_with_input(character, events_dictionary[event])
        elif "Effect" in events_dictionary[event].keys():
            event_with_effect(event["Effect"], character)
        elif "After-effect" in events_dictionary[event].keys() and events_dictionary[event]["After-effect"]:
            board[(character["Y-coordinate"], character["X-coordinate"])] = "There is nothing here anymore"


def event_with_input(character: dict, event: dict):
    print(event["Input"]["Description"])
    user_input = process_input(character, ["Yes, No"])
    if user_input == "Yes":
        if "Check item" in event["Input"]["Yes"]:
            event_with_check_of_item(character, event)
        else:
            if "Effect" in event.keys():
                event_with_effect(event["Input"]["Yes"]["Effect"], character)
            elif "Item" in event.keys():
                event_with_item(event["Input"]["Yes"]["Item"], character)
        event["After-effect"] = True
    else:
        if "Effect" in event.keys():
            event_with_effect(event["Input"]["No"]["Effect"], character)


def event_with_check_of_item(character: dict, event: dict):
    if has_item(event["Input"]["Yes"]["Check item"], character):
        character["Inventory"][event["Input"]["Yes"]["Check item"]] -= 1
        if "Effect" in event.keys():
            event_with_effect(event["Input"]["Yes"]["Effect"], character)
        elif "Item" in event.keys():
            event_with_item(event["Input"]["Yes"]["Item"], character)
    else:
        print("You have no such item.")


def event_with_effect(effects: list, character: dict):
    effect = random.choice(effects)
    print(effect[-1::])
    character["Current wounds"] = character["Max wounds"] if effect[0] == "Heal" else character["Current wounds"]
    if effect == "Damage":
        manage_wounds(4, character)
    character["Current experience"] += 50 if effect[0] == "Experience gain" else 0
    if effect[0] == "Random Stat Improvement":
        character[random.choice(list(character["Characteristics"].keys()))] += 2
    elif effect[0] == "Random Stat Deterioration":
        stat = random.choice(list(character["Characteristics"].keys()))
        character[stat] -= 2
        print(f"Your {stat} is decreased by 2")
    if effect[0] == "Battle":
        combat(character, generate_enemy(effect[1], effect[2]))


def event_with_item(items, character):
    item = random.choice(items)
    print(item[1])
    if "Armor" in item[0]:
        character["Max wounds"] += 2 if item[0] == "Armor" else 1
    elif item != "Nothing":
        if item[0] in character["Inventory"]:
            character["Inventory"][item[0]] += 1
        else:
            character["Inventory"].setdefault([item][0], 1)


def get_available_directions(character: dict, columns: int, rows: int) -> list:
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


def validate_option(choice: str, list_of_options: list) -> bool:
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


def process_command(command, character):
    if has_argument(command):
        command = get_command(command)
        command(character)
    else:
        command = get_command(command)
        command()


def move_character(character: dict, direction_index=None, available_directions=None) -> tuple:
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

    >>> protagonist = {"X-coordinate": 0, "Y-coordinate": 0, "Previous coordinates": (0, 1)}
    >>> move_character(protagonist, 0, ["south", "west"])
    >>> print(protagonist)

    >>>move_character(protagonist)
    {'X-coordinate': 0, 'Y-coordinate': 1}
    """
    directions_dictionary = {"north": -1, "south": 1, "west": -1, "east": 1}
    if available_directions is not None:
        direction = available_directions[direction_index]
        character["Previous coordinates"] = character["Y-coordinate"], character["X-coordinate"]
        if direction in "north south":
            character["Y-coordinate"] += directions_dictionary[direction]
        else:
            character["X-coordinate"] += directions_dictionary[direction]
    else:
        character["Y-coordinate"] = character["Previous coordinates"][0]
        character["X-coordinate"] = character["Previous coordinates"][1]
    return character["Y-coordinate"], character["X-coordinate"]


def is_goal_attained(character: dict) -> bool:
    """
    Check if goal is attained.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :postcondition: returns True if character has a Necronian artifact, else returns False
    :return: True if goal is attained, otherwise False

    >>> is_goal_attained({"Artifact": "Necronian Servo-Skull"})
    True
    >>> is_goal_attained({"Max wounds": 1000000000})
    False
    """
    return "Artifact" in character.keys()


def check_for_foes() -> bool:
    """
    Check if foe is encountered.

    :postcondition: returns True with 25% probability, else returns False
    :return: True if foe is encountered, otherwise False
    """
    return random.randrange(0, 6) == 0


def has_item(item: str, character: dict):
    return character["Inventory"][item] > 0


def generate_enemy(level, specific_enemy=None) -> dict:
    enemies_dictionary = {
        1:  # Level 1
        {
            "the rat":
            {
                "Name": "the rat",
                "Max wounds": 5,
                "Current wounds": 5,
                "Characteristics": {
                    "Intellect": 10,
                    "Strength": 15,
                    "Toughness": 15,
                    "Agility": 25
                },
                "Skills": {
                    "Flee Away": "The rat flees away.",
                    "Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)
                },
                "Will to fight": True,
                "Experience": 50
            },

            "the cultist":
                {
                    "Name": "the cultist",
                    "Max wounds": 10,
                    "Current wounds": 10,
                    "Characteristics": {
                        "Intellect": 30,
                        "Strength": 15,
                        "Toughness": 35,
                        "Agility": 35
                    },
                    "Skills": {
                        "Flee Away": "The rat flees away.",
                        "Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 10)
                    },
                    "Will to fight": True,
                    "Experience": 100
                },

            "the outlawed psyker":
                {
                    "Name": "the outlawed psyker",
                    "Max wounds": 15,
                    "Current wounds": 15,
                    "Characteristics": {
                        "Intellect": 30,
                        "Strength": 15,
                        "Toughness": 35,
                        "Agility": 35
                    },
                    "Skills": {
                        "Flee Away": "The rat flees away.",
                        "Enemy Attack": ("the outlawed psyker emits a banshee howl of psychic energy", 1, 15)
                    },
                    "Will to fight": True,
                    "Experience": 250
                }

        },
        2: {
            "the Necronian skeleton":
                {
                    "Name": "the Necronian skeleton",
                    "Max wounds": 25,
                    "Current wounds": 25,
                    "Characteristics": {
                        "Intellect": 45,
                        "Strength": 45,
                        "Toughness": 15,
                        "Agility": 25
                    },
                    "Skills": {
                        "Flee Away": "The skeleton flees away.",
                        "Enemy Attack": ("The skeleton cuts you with its hand blades", 1, 15)
                    },
                    "Will to fight": True,
                    "Experience": 250
                },

            "the giant spider":
                {
                    "Name": "the giant spider",
                    "Max wounds": 20,
                    "Current wounds": 20,
                    "Characteristics": {
                        "Intellect": 15,
                        "Strength": 35,
                        "Toughness": 35,
                        "Agility": 55
                    },
                    "Skills": {
                        "Flee Away": "The spider flees away.",
                        "Enemy Attack": ("The spider bites you painfully", 1, 15)
                    },
                    "Will to fight": True,
                    "Experience": 200
                },

            "the mummified Necron":
                {
                    "Name": "the mummified Necron",
                    "Max wounds": 15,
                    "Current wounds": 15,
                    "Characteristics": {
                        "Intellect": 85,
                        "Strength": 15,
                        "Toughness": 55,
                        "Agility": 5
                    },
                    "Skills": {
                        "Flee Away": "The mummy flees away.",
                        "Enemy Attack": ("The mummified Necron spreads its plague", 1, 9)
                    },
                    "Will to fight": True,
                    "Experience": 180
                },
        },
        3: {
            "the leader of cultists":
                {
                    "Name": "the leader of cultists",
                    "Max wounds": 30,
                    "Current wounds": 30,
                    "Characteristics": {
                        "Intellect": 85,
                        "Strength": 55,
                        "Toughness": 25,
                        "Agility": 55
                    },
                    "Skills": {
                        "Flee Away": "The deamonhost flees away.",
                        "Enemy Attack": ("The deamonhost tortures you with demonic sounds", 2, 12)
                    },
                    "Will to fight": True,
                    "Experience": 650
                },
            "the deamonhost":
                {
                    "Name": "the deamonhost",
                    "Max wounds": 30,
                    "Current wounds": 30,
                    "Characteristics": {
                        "Intellect": 85,
                        "Strength": 55,
                        "Toughness": 25,
                        "Agility": 55
                    },
                    "Skills": {
                        "Flee Away": "The deamonhost flees away.",
                        "Enemy Attack": ("The deamonhost tortures you with demonic sounds", 2, 12)
                    },
                    "Will to fight": True,
                    "Experience": 650
                },

            "the entity of the warp":
                {
                    "Name": "the entity of the warp",
                    "Max wounds": 45,
                    "Current wounds": 45,
                    "Characteristics": {
                        "Intellect": 85,
                        "Strength": 55,
                        "Toughness": 65,
                        "Agility": 5
                    },
                    "Skills": {
                        "Flee Away": "The  flees away.",
                        "Enemy Attack": ("The entity corrupts your mind", 2, 12)
                    },
                    "Will to fight": True,
                    "Experience": 650
                },
        },
        "Boss": {
            "Name": "Goreclaw the Render, a Daemon Prince of Khorne",
            "Max wounds": 100,
            "Current wounds": 100,
            "Characteristics": {
                "Intellect": 45,
                "Strength": 100,
                "Toughness": 70,
                "Agility": 5},
            "Skills": {
                "Daemon's Trickery": "20% to deal 5k10 damage, roll is counted to damage only if it's even",
                "Blade of Chaos": ""
            }
        }
    }
    if specific_enemy is not None:
        return enemies_dictionary[level][specific_enemy]
    return enemies_dictionary[level][random.choices(list(enemies_dictionary[level].keys()),
                                                    weights=[50, 45, 5], k=1)[0]]


def is_alive(character: dict) -> bool:
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
    >>>

    """
    result = ""
    map_dictionary = {
        "Ancient Altar room": "✙\t",
        "Entrance": "🚪\t",
        "Empty Room": "☐"
    }
    for row in range(rows):
        for column in range(columns):
            if (row, column) in board.keys() and (row, column) == \
                    (character["Y-coordinate"], character["X-coordinate"]):
                result += green_text() + "U" + normal_text() + "\t"
            elif (row, column) not in board.keys():
                result += "*\t"
            elif (row, column) in board.keys() and board[(row, column)][0] not in map_dictionary.keys():
                result += "d\t"
            else:
                result += map_dictionary[board[(row, column)]]
        result += "\n"
    return result


def show_map(location_map) -> None:
    r"""

    :param location_map:

    >>>

    """
    print(location_map)
    print("* —— not discovered yet, ✙ —— room with an altar, U —— your character, ☐ —— an empty room"
          "\n🚪 —— entrance, d —— discovered")


def tutorial(character):
    time.sleep(3)
    print("\n\tYour inquisitor, Scythia, gave a you crucial tusk to retrieve a Necronian artifact. She enlightens you "
          "that it's a sphere of incredible power. Surprisingly, no one knows\nwhat it does, but every cultist desires"
          " it. Hence, it's now your job as an acolyte to retrieve the miserable artifact that lies among the ruins of"
          "great stasis-tombs."
          "\n\tYou arrive to unnamed, deserted planet. Nothing indicates that here was once a paramount nation of"
          "servants of C'tan. Eventually, you found the ruins matching the\nNecronian decor."
          "\n\tAs you enter the tomb, it strikes you as odd. The insides of this dungeon are far from being ruins;"
          "it is rather the complete opposite of what you saw before. The soft green\nlight of some unknown kind of "
          "latter kindly lightens the room. Apparently, it was a complete waste of time to bring torches with or was "
          "it?. A sudden feel of being watched\nstops your vague reflection. You turn around and notice a giant rat "
          "greedily watching you."
          "\n\tYour mission begins."
          "\nHere are some helpful tips for your path of inquisitor:")
    time.sleep(4)
    help_commands()
    print("\n\nTo choose an option from a numbered list enter its index.")
    time.sleep(2)
    combat(character, generate_enemy(1, "the rat"))


def boss(character) -> None:
    if character["Level"][0] != 3:
        print("Fear takes control over you as soon as you get close to this room.\n"
              "You feel like you have to get more experience before facing it.\n You decide to retreat.")
        character["X-coordinate"] = 1
        character["Y-coordinate"] = 25
    else:
        print("You enter the dreadful room. The Necronian decor exactly matches the description the Inquisitor gave you"
              ". However, your joy deserves rapidly as you notice a gigantic daemon holding the precious artefact"
              "you are tasked to retrieve. The daemon notices you and smirks. His grotesque claws reveals his name ——"
              "Goreclaw the Render, a Daemon Prince of Khorne —— infamous among the inquisitors of this galaxy."
              "You know it will be a deadly battle with no opportunity to flee."
              "\n\"Bring. It. On.\", his monstrous majesty mandates")
        character.setdefault("Artifact", "Necronian artifact")
        character["Skills"]["Flee away"].pop()
        combat(character, generate_enemy("Boss"))


def game_over(character: dict) -> None:
    """
    Print game over phrase.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character keys must contain Current wounds string
    :precondition: character value with Current wounds key must be an integer
    :postcondition: prints "you died\n game over" ascii art if Current wounds <= 0,
                    else prints "congratulations" ascii art and victory phrase

    >>> game_over({"Current wounds": 0})
    ▓██***██▓****▒█████******█****██**********▓█████▄*****██▓***▓█████****▓█████▄****
    *▒██**██▒***▒██▒**██▒****██**▓██▒*********▒██▀*██▌***▓██▒***▓█***▀****▒██▀*██▌***
    **▒██*██░***▒██░**██▒***▓██**▒██░*********░██***█▌***▒██▒***▒███******░██***█▌***
    **░*▐██▓░***▒██***██░***▓▓█**░██░*********░▓█▄***▌***░██░***▒▓█**▄****░▓█▄***▌***
    **░*██▒▓░***░*████▓▒░***▒▒█████▓**********░▒████▓****░██░***░▒████▒***░▒████▓****
    ***██▒▒▒****░*▒░▒░▒░****░▒▓▒*▒*▒**********▒▒▓**▒******░▓*****░░*▒░*░**▒▒▓**▒****
    *▓██*░▒░******░*▒*▒░****░░▒░*░*░**********░*▒**▒*****▒*░****░*░**░****░*▒**▒****
    *░*░************░*░********░********************░********░********░**░******░*******
    *░*░******************************************░***************************░*********
    **▄████*****▄▄▄**********███▄*▄███▓***▓█████***********▒█████******██▒***█▓***▓█████*****██▀███**
    *██▒*▀█▒***▒████▄*******▓██▒▀█▀*██▒***▓█***▀**********▒██▒**██▒***▓██░***█▒***▓█***▀****▓██*▒*██▒
    ▒██░▄▄▄░***▒██**▀█▄*****▓██****▓██░***▒███************▒██░**██▒****▓██**█▒░***▒███******▓██*░▄█*▒
    ░▓█**██▓***░██▄▄▄▄██****▒██****▒██****▒▓█**▄**********▒██***██░*****▒██*█░░***▒▓█**▄****▒██▀▀█▄**
    ░▒▓███▀▒****▓█***▓██▒***▒██▒***░██▒***░▒████▒*********░*████▓▒░******▒▀█░*****░▒████▒***░██▓*▒██▒
    *░▒***▒*****▒▒***▓▒█░***░*▒░***░**░***░░*▒░*░*********░*▒░▒░▒░*******░*▐░*****░░*▒░*░***░*▒▓*░▒▓░
    **░***░******▒***▒▒*░***░**░******░****░*░**░***********░*▒*▒░*******░*░░******░*░**░*****░▒*░*▒░
    ░*░***░******░***▒******░******░*********░************░*░*░*▒**********░░********░********░░***░*
    ******░**********░**░**********░*********░**░*************░*░***********░********░**░******░*****
    ***********************************************************************░*************************
    >>> game_over({"Current wounds": 5})
    *▄████████**▄██████▄**███▄▄▄▄******▄██████▄*****▄████████****▄████████*****███*****███****█▄***▄█**********▄████████*****███******▄█***▄██████▄**███▄▄▄▄******▄████████*
    ███****███*███****███*███▀▀▀██▄***███****███***███****███***███****███*▀█████████▄*███****███*███*********███****███*▀█████████▄*███**███****███*███▀▀▀██▄***███****███*
    ███****█▀**███****███*███***███***███****█▀****███****███***███****███****▀███▀▀██*███****███*███*********███****███****▀███▀▀██*███▌*███****███*███***███***███****█▀**
    ███********███****███*███***███**▄███*********▄███▄▄▄▄██▀***███****███*****███***▀*███****███*███*********███****███*****███***▀*███▌*███****███*███***███***███********
    ███********███****███*███***███*▀▀███*████▄**▀▀███▀▀▀▀▀***▀███████████*****███*****███****███*███*******▀███████████*****███*****███▌*███****███*███***███*▀███████████*
    ███****█▄**███****███*███***███***███****███*▀███████████***███****███*****███*****███****███*███*********███****███*****███*****███**███****███*███***███**********███*
    ███****███*███****███*███***███***███****███***███****███***███****███*****███*****███****███*███▌****▄***███****███*****███*****███**███****███*███***███****▄█****███*
    ████████▀***▀██████▀***▀█***█▀****████████▀****███****███***███****█▀*****▄████▀***████████▀**█████▄▄██***███****█▀*****▄████▀***█▀****▀██████▀***▀█***█▀***▄████████▀**
    ***********************************************███****███*************************************▀*************************************************************************
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    You slain yet another blasphemous denizen of the Realm of Chaos and retrieved the accursed Necronian artifact.
    """
    if not is_alive(character):
        print(
                ("▓██***██▓****▒█████******█****██**********▓█████▄*****██▓***▓█████****▓█████▄****\n"
                 "*▒██**██▒***▒██▒**██▒****██**▓██▒*********▒██▀*██▌***▓██▒***▓█***▀****▒██▀*██▌***\n"
                 "**▒██*██░***▒██░**██▒***▓██**▒██░*********░██***█▌***▒██▒***▒███******░██***█▌***\n"
                 "**░*▐██▓░***▒██***██░***▓▓█**░██░*********░▓█▄***▌***░██░***▒▓█**▄****░▓█▄***▌***\n"
                 "**░*██▒▓░***░*████▓▒░***▒▒█████▓**********░▒████▓****░██░***░▒████▒***░▒████▓****\n"
                 "***██▒▒▒****░*▒░▒░▒░****░▒▓▒*▒*▒**********▒▒▓**▒******░▓*****░░*▒░*░**▒▒▓**▒****\n"
                 "*▓██*░▒░******░*▒*▒░****░░▒░*░*░**********░*▒**▒*****▒*░****░*░**░****░*▒**▒****\n"
                 "*░*░************░*░********░********************░********░********░**░******░*******\n"
                 "*░*░******************************************░***************************░*********\n"
                 "**▄████*****▄▄▄**********███▄*▄███▓***▓█████***********▒█████******██▒***█▓***▓█████*****██▀███**\n"
                 "*██▒*▀█▒***▒████▄*******▓██▒▀█▀*██▒***▓█***▀**********▒██▒**██▒***▓██░***█▒***▓█***▀****▓██*▒*██▒\n"
                 "▒██░▄▄▄░***▒██**▀█▄*****▓██****▓██░***▒███************▒██░**██▒****▓██**█▒░***▒███******▓██*░▄█*▒\n"
                 "░▓█**██▓***░██▄▄▄▄██****▒██****▒██****▒▓█**▄**********▒██***██░*****▒██*█░░***▒▓█**▄****▒██▀▀█▄**\n"
                 "░▒▓███▀▒****▓█***▓██▒***▒██▒***░██▒***░▒████▒*********░*████▓▒░******▒▀█░*****░▒████▒***░██▓*▒██▒\n"
                 "*░▒***▒*****▒▒***▓▒█░***░*▒░***░**░***░░*▒░*░*********░*▒░▒░▒░*******░*▐░*****░░*▒░*░***░*▒▓*░▒▓░\n"
                 "**░***░******▒***▒▒*░***░**░******░****░*░**░***********░*▒*▒░*******░*░░******░*░**░*****░▒*░*▒░\n"
                 "░*░***░******░***▒******░******░*********░************░*░*░*▒**********░░********░********░░***░*\n"
                 "******░**********░**░**********░*********░**░*************░*░***********░********░**░******░*****\n"
                 "***********************************************************************░*************************"
                 ))
    else:
        print(
    "*▄████████**▄██████▄**███▄▄▄▄******▄██████▄*****▄████████****▄████████*****███*****███****█▄***▄█**********▄████████*****███******▄█***▄██████▄**███▄▄▄▄******▄████████*\n"
    "███****███*███****███*███▀▀▀██▄***███****███***███****███***███****███*▀█████████▄*███****███*███*********███****███*▀█████████▄*███**███****███*███▀▀▀██▄***███****███*\n"
    "███****█▀**███****███*███***███***███****█▀****███****███***███****███****▀███▀▀██*███****███*███*********███****███****▀███▀▀██*███▌*███****███*███***███***███****█▀**\n"
    "███********███****███*███***███**▄███*********▄███▄▄▄▄██▀***███****███*****███***▀*███****███*███*********███****███*****███***▀*███▌*███****███*███***███***███********\n"
    "███********███****███*███***███*▀▀███*████▄**▀▀███▀▀▀▀▀***▀███████████*****███*****███****███*███*******▀███████████*****███*****███▌*███****███*███***███*▀███████████*\n"
    "███****█▄**███****███*███***███***███****███*▀███████████***███****███*****███*****███****███*███*********███****███*****███*****███**███****███*███***███**********███*\n"
    "███****███*███****███*███***███***███****███***███****███***███****███*****███*****███****███*███▌****▄***███****███*****███*****███**███****███*███***███****▄█****███*\n"
    "████████▀***▀██████▀***▀█***█▀****████████▀****███****███***███****█▀*****▄████▀***████████▀**█████▄▄██***███****█▀*****▄████▀***█▀****▀██████▀***▀█***█▀***▄████████▀**\n"
    "***********************************************███****███*************************************▀*************************************************************************\n"
    "\n\n\n"
    "You slain yet another blasphemous denizen of the Realm of Chaos and retrieved the accursed Necronian artifact.")


def main() -> None:
    """
    Drive the program.

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
        "threat from aliens, heretics, mutants and worse."), (
        "\n\tTo be a man in such times is to be one amongst untold billions. It "
        "is to live in the cruellest and most bloody regime imaginable. Forget the power of "
        "technology and \nscience, for so much has been forgotten, never to be re-learned. "
        "Forget the promise of progress and understanding, for in the grim darkness of "
        "the far future, there is \nonly war. There is no peace amongst the stars, "
        "only an eternity of carnage and slaughter, and the laughter of thirsting gods."),
        "\n\nAll rights belong to Games Workshop.")
    time.sleep(2)
    print("\n\n\n{:^160}".format("Welcome to the nightmarish world of Warhammer 40k Dark Heresy"))
    print("\n\nYou may desert anytime by typing {0}q{1}.\n\n".format(green_text(), normal_text()))
    game()


if __name__ == '__main__':
    main()
