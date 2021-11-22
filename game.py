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
            "Entrance",
        (24, 0):
            boss
    }
    tutorial(character)
    while is_alive(character) and not is_goal_attained(character):
        available_directions = get_available_directions(character, rows, columns)
        show_map(get_map(board, character, columns, rows))
        show_wounds(character["Current wounds"], character["Max wounds"])
        print("\nWhere would you like to go?")
        print_numbered_list_of_possibilities(available_directions)
        user_input = int(process_input(character, available_directions)) - 1
        add_room_to_the_board(move_character(character, user_input, available_directions), board)
        show_wounds(character["Current wounds"], character["Max wounds"])
        show_level(character)
        manage_events(board, character)
        if check_for_foes():
            enemy = generate_enemy(character["Level"][0])
            print("\n{0}You encounter an enemy. {1} attacks you!{2}".format(red_text(), enemy["Name"].capitalize(),
                                                                            normal_text()))
            combat(character, enemy)  # Combat begins
        if reached_new_level(character):
            level_up(character)
            proceed_further()
    game_over(character)


#  -----------------------------------------Board Manipulations------------------------------------------------------  #
def add_room_to_the_board(coordinates: tuple, board: dict) -> None:
    """
    Add a room to the board if the board doesn't have a room at the given coordinates.

    :param board: a dictionary
    :param coordinates: tuple of positive integers
    :precondition: board must be a dictionary
    :precondition: board keys must be tuples of integers
    :precondition: coordinates items must be positive integers
    :postcondition: Adds a room with a random event to the board if the board doesn't have a room at
                    the given coordinates
    """
    if coordinates not in board.keys():
        board.setdefault(coordinates, generate_random_room_event())


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


#  -----------------------------------------Input Manipulations------------------------------------------------------  #
def process_input(character=None, list_of_options=None, is_setting_name=False) -> str:
    """
    Process the user input

    :param character: an optional dictionary
    :param list_of_options: an optional list
    :param is_setting_name: an optional boolean
    :precondition: character must be either none or dictionary
    :precondition: list_of_options must be either none or list
    :precondition: list_of_options must be a boolean, False by default
    :postcondition: prompts user for input
    :postcondition: returns user_input if list_of_options is not None and if it passed the validation by
                    validate_option function
    :postcondition: executes the command in input if user_input in in list returned by get_command_list function and
                    character is not None
    :postcondition: returns user_input if is_setting_name is True and if user_input is not equal to an empty string
    :postcondition: repeats while loop if None of the above is True
    :return: user_input as a string if if list_of_options is not None and if it passed the validation by
                    validate_option function or if is_setting_name is True and if user_input is not equal to an empty
                    string
    """
    user_input = str(input())
    input_is_processed = True
    while input_is_processed:
        if list_of_options is not None and validate_option(user_input, list_of_options):
            return user_input
        elif character is not None and user_input in get_command_list():
            process_command(user_input, character)
            print_numbered_list_of_possibilities(list_of_options)
        elif is_setting_name and user_input != "":
            return user_input
        else:
            print("{0} is invalid input. Please, try again:".format(user_input))
        user_input = str(input())


def proceed_further() -> None:
    """
    Proceed further or quit.

    :postcondition: executes quit_game function if input is q, else proceeds further
    """
    print(green_text() + "\nEnter anything to continue:" + normal_text())
    if input() == "q":
        quit_game()


def get_command_list() -> list:
    """
    Get the list of commands.

    This is a helper function for process_input.

    :postcondition: returns the list of commands as a list
    :return: the list of commands as a list
    """
    commands_list = ["q", "h", "b", "s", "i", "c"]
    return commands_list


#  -----------------------------------------Character Creation-------------------------------------------------------  #
def character_creation() -> dict:
    """
    Create a character

    :postcondition: creates a character
    :return: character as a dictionary
    """
    character = {
        "Name": set_name(),
        "Adeptus": set_adeptus(),
        "Max wounds": 0,
        "Current wounds": 0,
        "Characteristics": {},
        "Level": [1, None],
        "Skills": {
            "Flee Away": "You retreat to the previous room."},
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
    character["Max wounds"] = set_wounds(character)
    character["Current wounds"] = character["Max wounds"]
    character["Characteristics"] = get_characteristics(character)
    proceed_further()
    show_characteristics(character)
    proceed_further()
    get_skills(character)
    show_list_of_skills(character)
    proceed_further()
    character["Level"] = get_level_name(character["Adeptus"], character["Level"][0])
    show_level(character)
    return character


def set_name() -> str:
    """
    Set character's name.

    This is a helper function for character_creation function.

    :postcondition: returns capitalized, non-empty string
    :return: name as a string
    """
    print("Enter your name:")
    name = process_input(is_setting_name=True)
    return name.capitalize()


def set_adeptus() -> str:
    """
    Set adeptus.

    This is a helper function for character_creation function.

    :postcondition: prints information about adepts
    :postcondition: prints how to choose from the list of options
    :postcondition: returns a chosen string from the adepts_list
    :return: adeptus as a string
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
    choice = process_input(list_of_options=adepts_list)
    return adepts_list[int(choice) - 1]


def set_wounds(character: dict) -> int:
    """
    Set the maximum amount of wounds.

    This is a helper function for character_creation function.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be created with character_creation function
    :postcondition: prints the information about wounds
    :postcondition: prints the information about wounds determination
    :postcondition: prints the information about how many wounds a chosen adeptus has
    :postcondition: prints the information about how many wounds a character has
    :postcondition: returns the maximum amount of wounds
    :return: the maximum amount of wounds as an integer
    """
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
    proceed_further()
    return max_wounds


def get_characteristics(character: dict) -> dict:
    """
    Get characteristics.

    This is a helper function for character_creation function.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be created with character_creation function
    :postcondition: prints the information about characteristics
    :postcondition: returns characteristics
    :return: characteristics as a dictionary
    """
    print("\n\tCharacteristics are crucial part of the game. They determine the results of evasion, fleeing, avoiding "
          "traps. Meanwhile, bonus of your characteristic\n(first digit of the characteristic) affects your damage. "
          "The Characteristics your character has propensities for are equal to 30 + 3k10 dice rolls,\nwhile others "
          " are equal to 30 + 2k10 dice rolls.\n\nCalculating stats...")
    proceed_further()
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
        "Intellect": characteristics_dictionary[character[
            "Adeptus"]][0][0] + roll(characteristics_dictionary[character["Adeptus"]][0][1], 10, character["Name"]),
        "Strength": characteristics_dictionary[character[
            "Adeptus"]][1][0] + roll(characteristics_dictionary[character["Adeptus"]][1][1], 10, character["Name"]),
        "Toughness": characteristics_dictionary[character[
            "Adeptus"]][2][0] + roll(characteristics_dictionary[character["Adeptus"]][2][1], 10, character["Name"]),
        "Agility": characteristics_dictionary[character[
            "Adeptus"]][3][0] + roll(characteristics_dictionary[character["Adeptus"]][3][1], 10, character["Name"])
    }
    return characteristics


def get_skills(character: dict) -> None:
    """
    Get a skill.

    This is a helper function for character_creation function.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be created with character_creation function
    :postcondition: adds a new skill to the Skills dictionary inside of character dictionary based on
                    the chosen Adeptus
    :return: None

    >>> d = {"Skills": {}, "Adeptus": "Adeptus Astra Telepathica"}
    >>> get_skills(d)
    >>> print(d)
    {'Skills': {'Lightning': 'A bolt of blinding lightning strikes from your hand dealing 2k10 damage.'}, 'Adeptus':\
 'Adeptus Astra Telepathica'}
    """
    dictionary_of_skills = {
        "Adeptus Astra Telepathica": (
            "Lightning", "A bolt of blinding lightning strikes from your hand dealing 2k10 damage."),
        "Adeptus Astra Militarum": (
            "Colossus Smash", "A devastating blow of your weapon that deals (1k10 + Strength Bonus) damage."),
        "Adeptus Mechanicus": (
            "Laser Shot", "Your servo-skull shots a laser beam from its eyes dealing (3 + Intellect Bonus) damage."),
        "Adeptus Officio Assassinorum": (
            "Deadly Burst", "You give your foe a burst of fire from two plasma-pistols dealing"
            " (2 + 1k10 + Agility Bonus) damage.")
    }
    character["Skills"].setdefault(dictionary_of_skills[character["Adeptus"]][0],
                                   dictionary_of_skills[character["Adeptus"]][1])


#  -------------------------------------------Character Manipulations------------------------------------------------  #
def get_level_name(adeptus: str, level: int):
    """
    Get level name.

    :param level: an integer
    :param adeptus: an alphabetic string
    :precondition: level must be an integer
    :precondition: adeptus must me an alphabetic string
    :postcondition: returns a common for all adepts name if level is not 3
    :postcondition: returns a unique name based on the chosen adeptus if level is 3
    :return: a unique name if level is 3, else a common name

    >>> get_level_name("Adeptus Officio Assassinorum", 3)
    Night Haunter
    >>> get_level_name("Adeptus Astra Telepathica", 2)
    Inquisitor
    """
    level_dictionary = {"Adeptus Astra Telepathica": "Magister Telepathicae", "Adeptus Astra Militarum":
                        "Legionary Astartes", "Adeptus Mechanicus": "Techno-Priest", "Adeptus Officio Assassinorum":
                        "Night Haunter", 1: "Acolyte", 2: "Inquisitor"}
    if level != 3:
        return [level, level_dictionary[level]]
    else:
        return [level, level_dictionary[adeptus]]


#                              Character Manipulations subsection: Wounds Management                                   #
def has_evaded(enemy: dict) -> bool:
    """
    Check if enemy enemy evaded the attack.

    This is a helper function for manage_wounds

    :param enemy: a dictionary
    :precondition: enemy must be created with character_creation function or with generate_enemy function
    :postcondition: returns True if 1k100 roll <= enemy's Agility, else returns False
    :postcondition: prints the evasion check phrase
    :return: True if evaded, otherwise False
    """
    print("{0}----------------------------------Evasion Check-------------------------------------------------------{1}"
          .format(green_text(), normal_text()))
    return roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Agility"]


def has_sustained(enemy: dict) -> bool:
    """
    Check if enemy enemy sustained the attack.

    This is a helper function for manage_wounds

    :param enemy: a dictionary
    :precondition: enemy must be created with character_creation function or with generate_enemy function
    :postcondition: returns True if 1k100 roll <= enemy's Toughness, else returns False
    :postcondition: prints the toughness check phrase
    :return: True if sustained, otherwise False
    """
    print("{0}----------------------------------Toughness Check-----------------------------------------------------{1}"
          .format(green_text(), normal_text()))
    return roll(1, 100, enemy["Name"]) <= enemy["Characteristics"]["Toughness"]


def manage_wounds(damage: int, enemy: dict, unavoidable=False) -> None:
    """
    Manage wounds.

    :param unavoidable: optional, a boolean
    :param enemy: a dictionary
    :param damage: an integer
    :precondition: enemy must be created with character_creation function or with generate_enemy function
    :precondition: damage must be an integer
    :precondition: unavoidable must be a boolean
    :postcondition: prints successful evasion phrase if unavoidable is False and has_evaded helper function returns
                    True
    :postcondition: prints unsuccessful evasion phrase if unavoidable is False and has_evaded helper function returns
                    False
    :postcondition: prints successful toughness check phrase and decrements Current wounds by damage divided by 2 if
                    all of the above conditions are False and if has_sustained helper function returns True
    :postcondition: prints unsuccessful toughness check phrase and decrements Current wounds by damage if all of the
                    above conditions are False
    :return: None
    """
    if not unavoidable and has_evaded(enemy):
        print("{0}However, {1} evades it.{2}".format(green_text(), enemy["Name"], normal_text()))
    else:
        if not unavoidable:
            print("{0}{1} was not able to evade.{2}".format(red_text(), enemy["Name"].capitalize(), normal_text()))
        if has_sustained(enemy):
            damage = math.floor(damage / 2)
            enemy["Current wounds"] -= damage
            print("{0}However, {1} sustains it and only receives {2} damage.{3}".format(green_text(), enemy["Name"],
                                                                                        damage, normal_text()))
        else:
            print("{0}{1} was not able to sustain.{2}".format(red_text(), enemy["Name"].capitalize(), normal_text()))
            enemy["Current wounds"] -= damage
    proceed_further()


def level_up(character: dict) -> None:
    """
    Perform level up.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints the new level phrase
    :postcondition: increases character's Level by 1
    :postcondition: multiplies character's Experience for the next level by 2 if level is not 3, else makes it a string
                    "Reached the maximum level"
    :postcondition: adds a new skill to character's Skills based on adeptus and level
    :postcondition: increases character's Max wounds by the number based on adeptus and level
    :postcondition: changes character Level name based on adeptus and level
    :postcondition: prints new skill's name and description
    :postcondition: prints new level name
    :return: None
    """
    dictionary_of_skills = {
        2: {
            "Adeptus Astra Telepathica":
                ("Spontaneous Combustion", "The power of your mind ignites your enemy dealing (Bonus Intellect)k10"
                                           " damage"),
            "Adeptus Astra Militarum":
                ("Charge", "You charge into your enemy dealing (3 * Bonus Strength) damage. Prosaic, yet effective"
                           ""),
            "Adeptus Mechanicus":
                ("Robotic Wrath", "Another runtime error infuriates your servitor and makes it destroy everything in "
                                  "its way dealing (Bonus Intellect + 3k(Bonus Intellect)) damage"),
            "Adeptus Officio Assassinorum":
                ("Killer Instinct", "You spray a fan of venomous knives dealing (Bonus Agility)k5 damage")
        },
        3: {
            "Adeptus Astra Telepathica":
                ("Chaos of Warp", "One is always equal in death. You make your enemy's wounds equal to yours"),
            "Adeptus Astra Militarum":
                ("Rampage", "Those who live by the sword shall die by your blade.\nYou make a series of bloodthirsty"
                            " slashes dealing (1k(Bonus Strength))k10 damage"),
            "Adeptus Mechanicus":
                ("Deus ex Machina", "You pray Omnissiah to slay fools who cannot see the stupor mundi of machines.\n"
                                    "You use 1k10 of your skills in one round. Skills are chosen randomly"
                                    " between Robotic Wrath and Laser Shot"),
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
    print("\nYou reached new level!")
    character["Level"][0] += 1
    character["Experience for the next level"] = character["Experience for the next level"] * 2 if \
        character["Level"][0] != 3 else "Reached the maximum level"
    skill_name, skill_description = dictionary_of_skills[character["Level"][0]][character["Adeptus"]][0], \
                                    dictionary_of_skills[character["Level"][0]][character["Adeptus"]][1]
    character["Skills"].setdefault(skill_name, skill_description)
    character["Max wounds"] += dictionary_of_wounds[character["Level"][0]][character["Adeptus"]]
    character["Current wounds"] = character["Max wounds"]
    character["Level"] = get_level_name(character["Adeptus"], character["Level"][0])
    print("You have got a new skill:", skill_name + ".", "\n" + skill_description + ".", "\nYou have now",
          character["Current wounds"], "wounds.")
    show_level(character)


#  -----------------------------------------------Combat-------------------------------------------------------------  #
def combat(character: dict, enemy: dict) -> None:
    """
    Drive the combat.

    :param character: a dictionary
    :param enemy: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid enemy generated by generate_enemy function
    :postcondition: battle ends if character wounds is <= zero or if character decides to flee
    :postcondition: battle ends if enemy wounds is <= zero or if enemy decides to flee
    :postcondition: character receives experience only if they are alive and not decided to flee away
    :postcondition: character receives full experience if enemy is killed, half experience if enemy flees
    :postcondition: prints the beginning combat phrase
    :postcondition: prints the ending combat phrase
    :postcondition: prints turn phrases if in while loop
    :postcondition: prints the phrase about enemy's death if enemy is dead
    """
    print("\nCombat between {0} and {1} begins.".format(character["Name"], enemy["Name"]))
    while enemy["Will to fight"]:
        print("{0}----------------------------------Player's turn---------------------------------------------------{1}"
              .format(green_text(), normal_text()))
        show_wounds(character["Current wounds"], character["Max wounds"])
        print_numbered_list_of_possibilities(list(character["Skills"].keys()))
        user_input = int(process_input(character, list(character["Skills"].keys()))) - 1
        damage = use_skill(character, list(character["Skills"].keys())[user_input], enemy)  # player's turn
        if not character["Will to fight"]:
            break
        manage_wounds(damage, enemy)
        if not is_alive(enemy):
            break
        print("{0}----------------------------------Enemy's turn----------------------------------------------------{1}"
              .format(green_text(), normal_text()))
        damage = use_skill(enemy, random.choice(list(enemy["Skills"].keys())[1::]), character)  # enemy's turn
        manage_wounds(damage, character)
        if not is_alive(character):
            break
        if random.randrange(1, 6) == 1:
            use_skill(enemy, list(enemy["Skills"].keys())[0], character)  # Enemy fleeing, boss' additional attack
    if is_alive(character) and character["Will to fight"]:
        character["Current experience"] += enemy["Experience"] if not is_alive(enemy)\
            else math.floor(enemy["Experience"] / 2)
    if not is_alive(enemy):
        print("\n{0} dies.".format(enemy["Name"].capitalize()))
    if not character["Will to fight"]:
        move_character(character)
    print("\nThe battle is over.")
    show_level(character)
    character["Will to fight"] = True
    proceed_further()


#                                       Combat subsection: Skills management                                           #
def use_skill(attacker: dict, skill_name: str, defender: dict) -> int:
    """
    Use the chosen skill.

    This is a helper function for combat function.

    :param attacker: a dictionary
    :param skill_name: an alphabetic string
    :param defender: a dictionary
    :precondition: attacker must be a dictionary
    :precondition: attacker must be a valid character created by character_creation function or generated by
                   generate_enemy function
    :precondition: defender must be a dictionary
    :precondition: defender must be a valid enemy generated by generate_enemy function or created by character_creation
                   function
    :precondition: skill_name must be an alphabetic string
    :precondition: skill_name must be in skills_dictionary
    :postcondition: invokes the function associated with skill_name using attacker as an attacker and defender as a
                    defender
    :return: damage made by invoked function
    """
    skills_dictionary = {
        "Lightning": lightning,
        "Colossus Smash": colossus_smash,
        "Laser Shot": laser_shot,
        "Deadly Burst": deadly_burst,
        "Flee Away": flee_away,
        "Enemy Attack": enemy_attack,
        "Daemon's Trickery": daemon_trickery,
        "Spontaneous Combustion": spontaneous_combustion,
        "Charge": charge,
        "Robotic Wrath": robotic_wrath,
        "Killer Instinct": killer_instinct,
        "Chaos of Warp": chaos_of_warp,
        "Rampage": rampage,
        "Deus ex Machina": deus_ex_machina,
        "Vendetta": vendetta}
    return skills_dictionary[skill_name](attacker, defender)


def lightning(character: dict, enemy: dict) -> int:
    """
    Use lighting skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to 2k10 dice rolls
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = roll(2, 10, character["Name"])
    print("\nA bolt of blinding lightning strikes from {0}'s hand dealing {1} damage to {2}.".format(
        character["Name"], damage, enemy["Name"]))
    return damage


def spontaneous_combustion(character: dict, enemy: dict) -> int:
    """
    Use Spontaneous Combustion skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (Intellect divided by 10)k10 dice rolls
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = roll(math.floor(character["Characteristics"]["Intellect"] / 10), 10, character["Name"])
    print("\nThe power of your mind ignites {0} dealing {1} damage.".format(enemy["Name"], damage))
    return damage


def chaos_of_warp(character: dict, enemy: dict) -> int:
    """
    Use Chaos of Warp skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: makes enemy Max wounds and Current wounds be equal to Max Wounds of a character
    :postcondition: prints the skill's phrase
    :postcondition: returns 0
    :return: 0
    """
    enemy["Max wounds"] = character["Max wounds"]
    enemy["Current wounds"] = enemy["Max wounds"]
    print("\nYou make wounds of {0} equal to {1}.\n".format(enemy["Name"], enemy["Current wounds"]))
    return 0


def colossus_smash(character: dict, enemy: dict) -> int:
    """
    Use Colossus Smash skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (1k10 dice roll + Strength divided by 10)
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = math.floor(character["Characteristics"]["Strength"] / 10) + roll(1, 10, character["Name"])
    print("\nA devastating blow of {0} weapon rips and tears {1} dealing {2} damage\n".format(
        character["Name"], enemy["Name"], damage))
    return damage


def charge(character: dict, enemy: dict) -> int:
    """
    Use Charge skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (Strength divided by 10 and multiplied by 3)
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = math.floor(character["Characteristics"]["Strength"] / 10) * 3
    print("\n{0}'s enormous body charges into {1} dealing {2} damage\n".format(
        character["Name"], enemy["Name"], damage))
    return damage


def rampage(character: dict, enemy: dict) -> int:
    """
    Use Rampage skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (1k(Strength divided by 10)k10 dice rolls
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = roll(roll(1, math.floor(character["Characteristics"]["Strength"] / 10), character["Name"]), 10,
                  character["Name"])
    print("\n{0} makes a series of bloodthirsty slashes dealing {1} damage to {2}.\n".format(
        character["Name"], damage, enemy["Name"]))
    return damage


def laser_shot(character: dict, enemy: dict) -> int:
    """
    Use Laser Shot skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (3 + (Intellect divided by 10)
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = 3 + math.floor(character["Characteristics"]["Intellect"] / 10)
    print("\nYour servo-skull shots a laser beam from its eyes dealing {0} damage to {1}.".format(damage,
                                                                                                  enemy["Name"]))
    return damage


def robotic_wrath(character: dict, enemy: dict) -> int:
    """
    Use Robotic Wrath skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to ((Intellect divided by 10) + 3k(Intellect divided by 10))
                    dice rolls
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = math.floor(character["Characteristics"]["Intellect"] / 10) +\
             roll(3, math.floor(character["Characteristics"]["Intellect"] / 10), character["Name"])
    print("\n\"TRACEBACK (MOST RECENT CALL LAST):\nFILE ROOT/SERVITOR/BRAIN/COMBAT/ATTACK.py LINE 42, IN <module>\n"
          "ZERO DIVISION ERROR: DIVISION BY ZERO\n"
          "[FINISHED IN 0.314s WITH EXIT CODE ROBOTIC WRATH],\" your Servitor roars robotically."
          "\nThe enraged servitor destroys everything in the way dealing {0} damage to {1}.".format(damage,
                                                                                                    enemy["Name"]))
    return damage


def deus_ex_machina(character: dict, enemy: dict) -> int:
    """
    Use Deus ex Machina skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: invokes 1k10 dice roll of random skills from skills_list
    :postcondition: calculates damage
    :postcondition: prints the skill's phrase
    :return: damage as integer
    """
    skills_list = ["Robotic Wrath", "Laser Shot"]
    skills_list = random.choices(skills_list, k=roll(1, 10, character["Name"]))
    damage = 0
    print("\nYou pray Omnissiah to slay fools who cannot see the stupor mundi of machines.")
    for skill in skills_list:
        damage += use_skill(character, skill, enemy)
    return damage


def deadly_burst(character: dict, enemy: dict) -> int:
    """
    Use Deadly Burst skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (1k10 dice roll + 2 + (Agility divided by 10))
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = math.floor(character["Characteristics"]["Agility"] / 10) + 2 + roll(1, 10, character["Name"])
    print("\nYou give {0} a burst of fire from two plasma-pistols dealing {1} damage.\n".format(enemy["Name"], damage))
    return damage


def killer_instinct(character: dict, enemy: dict) -> int:
    """
    Use Killer Instinct skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to (Agility divided by 10)k5 dice rolls
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = roll(math.floor(character["Characteristics"]["Agility"] / 10), 5, character["Name"])
    print("\nYou spray a fan of venomous knives dealing dealing {0} damage to {1}.".format(damage, enemy["Name"]))
    return damage


def vendetta(character: dict, enemy: dict) -> int:
    """
    Use Vendetta skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to 1k100 dice roll
    :postcondition: prints the skill's phrase and damage the ability did
    :return: damage as integer
    """
    damage = roll(1, 100, character["Name"])
    print("\nYour fatal shot deals {0} damage to {1}.".format(damage, enemy["Name"]))
    if damage < 20:
        print("V means very random.")
    return damage


def flee_away(character: dict, enemy: dict) -> 0:
    """
    Use Flee Away skill.

    This is a helper function for use_skill

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: prints the fleeing phase phrase
    :postcondition: prints the fleeing phrase
    :postcondition: prints the fleeing with damage phrase and decrements Current wounds by damage of random enemy's
                    attack if 1k100 roll > Agility
    :postcondition: prints the damageless fleeing phrase if the condition above is False
    :postcondition: sets Will to fight to False
    :postcondition: returns 0
    :return: 0
    """
    print("{0}----------------------------------------Fleeing-------------------------------------------------------{1}"
          .format(green_text(), normal_text()))
    print("\n{0}{1} decides to flee away.{2}".format(green_text(), character["Name"].capitalize(), normal_text()))
    if roll(1, 100, character["Name"]) > character["Characteristics"]["Agility"]:
        print("{0} is not quick enough to flee without damage.".format(character["Name"]))
        manage_wounds(use_skill(enemy, random.choice(list(enemy["Skills"].keys())[1::]), character), character)
    else:
        print("{0} flees without damage.".format(character["Name"].capitalize()))
    character["Will to fight"] = False
    return 0


def enemy_attack(enemy: dict, character: dict) -> int:
    """
    Use Enemy Attack skill.

    This is a helper function for use_skill

    :param character: a dictionary
    :param enemy: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to
                    (second element in Enemy Attack tuple)k(second element in Enemy Attack tuple) dice rolls
    :return: damage as integer
    """
    damage = roll(enemy["Skills"]["Enemy Attack"][1],
                  enemy["Skills"]["Enemy Attack"][2], enemy["Name"])
    print("\n" + enemy["Skills"]["Enemy Attack"][0] + " dealing {0} damage to {1}.".format(damage,
                                                                                           character["Name"]))
    return damage


def daemon_trickery(enemy: dict, character: dict) -> int:
    """
    Use Daemon Trickery skill.

    This is a helper function for use_skill.

    This is a function the boss uses instead of Flee Away. The chance of using this skill is equal to 20%

    :param character: a dictionary
    :param enemy: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: calculates damage that is equal to 5k10 dice rolls; roll is counted toward damage only
                    if it's an even number.
    :return: damage as integer
    """
    print("\n{0} dirtily makes another attack\n".format(enemy["Name"]))
    damage = sum(list(map(lambda number: number if number % 2 == 0 else 0, [roll(1, 10, enemy["Name"]) for _ in
                                                                            range(5)])))
    print("\n{0} deals {1} damage to {2}\n".format(enemy["Name"], damage, character["Name"]))
    return damage


def blade_of_chaos(enemy: dict, character: dict) -> int:
    """
    Use Blade of Chaos skill.

    This is a helper function for use_skill.

    :param enemy: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: enemy must be a dictionary
    :precondition: enemy must be a valid character generated by generate_enemy function
    :postcondition: returns 0
    :postcondition: decrements enemy Current wounds by 8 if the player's guess is not in correct_answer
    :postcondition: prints attack phrase
    :postcondition: prints success phrase if the player's guess is in correct_answer, else prints failure phrase
    :return: 0
    """
    print("\nYou notice how this fiend of Khorne prepares a slash attack. You have an opportunity to deflect it if you"
          "guess the 2 body parts he aims for H(head), B(body), A(arms), F(feet). He certainly will not be able to"
          "evade or sustain it."
          "\nEnter the first letters of 2 body parts (AB for arms and body):")
    correct_answer = random.choice(list(itertools.combinations("HBAF", 2)))
    correct_answer = [correct_answer, correct_answer[::-1]]
    if str(input()).replace(" ", "").upper() in correct_answer:
        print("Success! You deflect the attack! Who is smirking now? {0} receives 8 damage".format(enemy["Name"]))
        enemy["Current wounds"] -= 8
    else:
        print("Failure! {0} smirks and deals 8 damage to {1}.".format(enemy["Name"], character["Name"]))
    character["Current wounds"] -= 8
    return 0


#  --------------------------------------Printing Functions and Text Manipulation------------------------------------  #
def print_numbered_list_of_possibilities(list_of_options: list) -> None:
    """
    Print a numbered list of options

    :param list_of_options: a non-empty list
    :precondition: list_of_options is a non-empty list
    :postcondition: prints a numbered list of options where index has a green color
    """
    for index, option_name in enumerate(list_of_options, 1):
        print(green_text() + str(index) + normal_text(), option_name)


def print_dictionary_items(dictionary: dict) -> None:
    """
    Print dictionary items

    :param dictionary: a non-empty dictionary
    :precondition: dictionary must a non-empty dictionary
    :postcondition: prints dictionary items where each key has a green color
    """
    for key in dictionary.keys():
        print(green_text() + key + normal_text() + ":", dictionary[key])


def green_text() -> str:
    """
    Returns the green color escape sequence.

    :postcondition: returns the green color escape sequence
    :return: the green color escape sequence as a string
    """
    return "\x1b[1;32m"


def red_text() -> str:
    """
    Returns the red color escape sequence.

    :postcondition: returns the red color escape sequence
    :return: the red color red sequence as a string
    """
    return "\x1b[1;31m"


def normal_text() -> str:
    """
     Returns PyCharm's default color escape sequence.

     :postcondition: returns PyCharm's default color escape sequence
     :return: PyCharm's default color sequence as a string
     """
    return "\x1b[0;20m"


def show_wounds(wounds, maximum_wounds) -> None:
    """
    Prints the player's current wounds and maximum wounds

    :param wounds: an integer
    :param maximum_wounds: an integer
    :precondition: wounds must be an integer
    :precondition: maximum_wounds must be an integer
    :postcondition: prints wounds status

    >>> show_wounds(3, 25)
    <BLANKLINE>
    Wounds: 3/25
    """
    print("\nWounds: {0}/{1}".format(wounds, maximum_wounds))


def show_level(character: dict) -> None:
    """
    Prints character's Level

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints 2 different versions of character's Level based on character's Level
    :postcondition: prints character's Current experience if character Level is not 3
    :return: None

    >>> show_level({"Level": (1, "Acolyte"), "Current experience": 100, "Experience for the next level": 1000})
    <BLANKLINE>
    Level: 1, Acolyte
    Experience: 100/1000
    >>> show_level({"Level": (3, "Night Haunter"), "Current experience": 2100, "Experience for the next level": \
    "Reached the maximum level"})
    <BLANKLINE>
    Level: 3, Night Haunter
    Experience: Reached the maximum level
    """
    if character["Level"][0] != 3:
        print(
            "\nLevel: {0}, {1}\n"
            "Experience: {2}/{3}".format(
                character["Level"][0],
                character["Level"][1],
                character["Current experience"],
                character["Experience for the next level"]
            )
        )
    else:
        print(
            "\nLevel: {0}, {1}\n"
            "Experience: {2}".format(
                character["Level"][0],
                character["Level"][1],
                character["Experience for the next level"]
            )
        )


#  --------------------------------------------Universal Helper Functions--------------------------------------------  #
def roll(number_of_dice: int, number_of_sides: int, name: str) -> int:
    """
    Roll the chosen amount of dice with the chosen sides

    :param number_of_dice: a positive integer
    :param number_of_sides: a positive integer
    :param name: a string
    :precondition: number_of_dice: must be a positive integer
    :precondition: number_of_sides must be a positive integer
    :precondition: name must be a string
    :postcondition: prints the beginning roll phrase
    :postcondition: prints every roll
    :postcondition: prints the sum of rolls where the sum has a green color
    :return: sum of rolls as an integer
    """
    list_of_rolls = [random.randrange(1, number_of_sides + 1) for _ in range(number_of_dice)]
    print("\n{0} rolled:".format(name.capitalize()))
    for single_roll in list_of_rolls:
        time.sleep(1)
        print("{0}{1}{2}".format(single_roll, green_text(), normal_text()))
    time.sleep(1)
    print("The sum of rolls of {0} is {1}{2}{3}".format(name, green_text(), sum(list_of_rolls), normal_text()))
    return sum(list_of_rolls)


def has_item(item: str, character: dict):
    """
    Check if character has the item.

    :param item: a string
    :param character: a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondtition: returns True if item in character["Inventory"] and the amount of character["Inventory"][item] > 0,
                     else False
    :return: True if item is present, otherwise False

    >>> has_item("Bandage", {"Inventory": {"Bandage": 5}})
    True
    >>> has_item("Torch", {"Inventory": {"Anything else": 10000}})
    False
    """
    return item in character["Inventory"].keys() and character["Inventory"][item] > 0


def is_alive(character: dict) -> bool:
    """
    Determine if character is alive.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: returns True if character["Current wounds"] > 0, else return False
    :return: True if character is alive, otherwise False

    >>> is_alive({"Current wounds": 5})
    True
    >>> is_alive({"Current wounds": 0})
    False
    >>> is_alive({"Current wounds": -1})
    False
    """
    return character["Current wounds"] > 0


def generate_enemy(level, specific_enemy=None) -> dict:
    """
    Generates an enemy

    :param level: a positive integer or "Boss" string
    :param specific_enemy: an alphabetic string
    :precondition: level must be a positive integer in range [1, 3] or "Boss" string
    :precondition: specific_enemy must be an alphabetic string that is a part of enemies_dictionary
    :postcondition: returns a random enemy based on level if specific enemy is None, else returns name based on level
                     and specific_enemy
    :return: enemy as a dictionary
    """
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
                "Experience": 150
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
                        "Enemy Attack": ("The cultist gives you a taste of their blade", 1, 10)
                    },
                    "Will to fight": True,
                    "Experience": 200
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
                    "Experience": 350
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
                    "Experience": 450
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
                    "Experience": 600
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
                    "Experience": 500
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
                    "Experience": 1000
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
                    "Experience": 1500
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
                    "Experience": 2000
                },
        },
        "Boss": {
            "Boss":
            {
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
                },
                "Will to fight": True,
                "Experience": 2000
            }
        }
    }
    if specific_enemy is not None:
        return enemies_dictionary[level][specific_enemy]
    return enemies_dictionary[level][random.choices(list(enemies_dictionary[level].keys()),
                                                    weights=[50, 45, 5], k=1)[0]]


#  --------------------------------------------Game Helper Functions-------------------------------------------------  #
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


def reached_new_level(character: dict) -> bool:
    """
    Check if character reached new level.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: returns True if character's Current experience >= character's Experience for the next level and
                    if character's Level is not 3, else returns False
    :return: True if new level is reached, otherwise False
    """
    if character["Level"][0] == 3:
        return False
    return character["Current experience"] >= character["Experience for the next level"]


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


def validate_option(choice: str, list_of_options: list) -> bool:
    """
    Validate option availability.

    :param choice: a string
    :param list_of_options: a list of strings
    :precondition: choice must be a string
    :precondition: list_of_options must be a list
    :postcondition: returns False if choice is not a number
    :postcondition: returns False if choice - 1 is not in rage of available_direction length
    :postcondition: returns true otherwise
    :return: True if choice is valid, else False

    >>> validate_option("1", ["south", "east"])
    True
    >>> validate_option("0", ["yes", "no"])
    False
    >>> validate_option("wait what", ["Vendetta", "Deadly Burst"])
    False
    """
    return choice.isnumeric() and (int(choice) - 1) in range(len(list_of_options))


def move_character(character: dict, direction_index=None, available_directions=None) -> tuple:
    """
    Change character's coordinates.

    :param character: a dictionary
    :param direction_index: a non-negative integer, optional
    :param available_directions: a list of strings, optional
    :precondition: character keys must contain "X-coordinate" and "Y-coordinate"
    :precondition: character values must be integers
    :precondition: direction_index must be a non-negative integer validated by validate_option function or None
    :precondition: availabe_directions each item must be either "north", "south", "east" or "west", or None
    :postcondition: updates character X or Y coordinate based on direction choice if availabe_directions is not None
    :postcondition: makes character X or Y coordinate be equal to the previous coordinates
    :return: new character's coordinates as a tuple

    >>> protagonist = {"Y-coordinate": 1, "X-coordinate": 1, "Previous coordinates": (0, 1)}
    >>> move_character(protagonist, 0, ["south", "west"])
    (2, 1)
    >>> protagonist = {"Y-coordinate": 1, "X-coordinate": 1, "Previous coordinates": (0, 1)}
    >>> move_character(protagonist)
    (0, 1)

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


def check_for_foes() -> bool:
    """
    Check if foe is encountered.

    :postcondition: returns True with 25% probability, else returns False
    :return: True if foe is encountered, otherwise False
    """
    return random.randrange(0, 4) == 0


def get_map(board: dict, character: dict, columns: int, rows: int) -> str:
    r"""
    Get a map.

    :param board: a dictionary
    :param character: a dictionary
    :param columns: a positive integer
    :param rows: a positive integer
    :precondition: board must be a dictionary
    :precondition: board is a valid board generated by generate_random_room_event
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: rows must be a positive integer
    :precondition: columns must be a positive integer
    :postcondition: returns the map as a string
    :return: the map as a string

    >>> char = {"Y-coordinate": 2,"X-coordinate": 2}
    >>> get_map({(0, 0): "Entrance", (0, 1): "Empty Room", (1, 1): "Ancient Altar Room"}, char, 5, 5)
    '🚪\t☐\t*\t*\t*\t\n*\t✙\t*\t*\t*\t\n*\t*\t\x1b[1;32mU\x1b[0;20m\t*\t*\t\n*\t*\t*\t*\t*\t\n*\t*\t*\t*\t*\t\n'
    """
    result = ""
    map_dictionary = {
        "Ancient Altar Room": "✙\t",
        "Entrance": "🚪\t",
        "Empty Room": "☐\t"
    }
    for row in range(rows):
        for column in range(columns):
            if (row, column) == (character["Y-coordinate"], character["X-coordinate"]):
                result += green_text() + "U" + normal_text() + "\t"
            elif (row, column) not in board.keys():
                result += "*\t"
            elif (row, column) in board.keys() and board[(row, column)] in map_dictionary.keys():
                result += map_dictionary[board[(row, column)]]
            else:
                result += "d\t"
        result += "\n"
    return result


def show_map(location_map) -> None:
    """
    Print the map

    :param location_map: a string
    :precondition: location map must be a string generated by get_map function
    :postcondition: prints the map and map's symbols meaning
    :return:
    """
    print(location_map)
    print("* —— not discovered yet, ✙ —— a room with an altar, U —— your character, ☐ —— an empty room"
          "\n🚪 —— entrance, d —— discovered")


#  --------------------------------------------Commands Management---------------------------------------------------  #
def process_command(command: str, character: dict) -> None:
    """
    Process command.

    :param command: an alphabetic string
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: command must be an alphabetic string and part of the list returned by get_command_list
    :precondition: character must be a valid character created by character_creation function
    :postcondition: invokes a command function
    :return: None
    """
    if has_argument(command):
        command = get_command(command)
        command(character)
    else:
        command = get_command(command)
        command()


def has_argument(command: str) -> bool:
    """
    Check if command has an argument.

    This is helper function for process_command

    :param command: an alphabetic string
    :precondition: command must be an alphabetic string and part of the list returned by get_command_list
    :postcondition: returns True if command has an argument, else False
    :return: True if command has an argument, otherwise False

    >>> has_argument("h")
    False
    >>> has_argument("b")
    True
    """
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
    Get command.

    This is helper function for process_command

    :param command_name: an alphabetic string
    :precondition: command_name must be an alphabetic string and part of the list returned by get_command_list
    :postcondition: returns function reference that is associated with command_name
    :return: function reference
    """
    commands_dictionary = {
        "q": quit_game,
        "h": help_commands,
        "b": bandage,
        "s": show_list_of_skills,
        "i": show_inventory,
        "c": show_characteristics}
    return commands_dictionary[command_name]


#                                           Commands Management: Commands                                              #
def help_commands() -> None:
    """
    Print all commands' keywords and their descriptions.

    This is a helper function for get_command.

    :postcondition: print all commands' keywords and their descriptions where keywords have a green color
    :return: None
    """
    print("\nThis is the list of the available commands:\n"
          "{0}h{1} —— show list of commands with a short description,\n"
          "{0}q{1} —— quit the game,\n"
          "{0}b{1} —— bandage your injuries and restore 4 wounds; you can use as many as you want per one turn,\n"
          "{0}s{1} —— show list of your skills,\n"
          "{0}c{1} —— show your characteristics,\n"
          "{0}i{1} —— show your inventory,\n"
          .format(green_text(), normal_text()))


def show_list_of_skills(character: dict) -> None:
    """
    Print the list of character's skills.

    This is a helper function for get_command.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: print all skills' names and their descriptions where skill's name has a green color
    """
    print("\nRight now you have the following skills:")
    print_dictionary_items(character["Skills"])


def bandage(character: dict) -> None:
    """
    Restore character's Current wounds.

    This is a helper function for get_command.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: increases character's Current wounds by 4 and prints how many bandages left if amount of Bandage in
                    character's Inventory > 0, else prints "You have no bandages"
    :postcondition: makes character's Current wounds be equal to character's Max wounds if Current wounds > Max wounds
    :return: None

    >>> bandage({"Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}})
    <BLANKLINE>
    Wounds: 14/20
    <BLANKLINE>
    4 bandages are left
    """
    if has_item("Bandage", character):
        character["Current wounds"] += 4
        if character["Current wounds"] > character["Max wounds"]:
            character["Current wounds"] = character["Max wounds"]
        character["Inventory"]["Bandage"] -= 1
        show_wounds(character["Current wounds"], character["Max wounds"])
        print("\n{0} bandage{1} {2} left".format(character["Inventory"]["Bandage"],
                                                 "s" if character["Inventory"]["Bandage"] != 1 else "",
                                                 "are" if character["Inventory"]["Bandage"] != 1 else "is"))
    else:
        print("You have no bandages")


def show_inventory(character: dict) -> None:
    """
    Print character's Inventory.

    This is a helper function for get_command.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints "You have the following items:"
    :postcondition: prints character's Inventory where its keys have a green color
    :return: None
    """
    print("\nYou have the following items:")
    print_dictionary_items(character["Inventory"])


def show_characteristics(character: dict) -> None:
    """
    Print character's Characteristics

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints character's Characteristics where its keys have a green color
    :postcondition: prints "Your characteristics are:"
    :return: None
    """
    print("\nYour characteristics are:")
    print_dictionary_items(character["Characteristics"])


def quit_game() -> None:
    """
    Quit the game.

    :postcondition: prints quit phrase
    :postcondition: quits the game.
    :return: None
    """
    print("\nYou may deserve now, but your duty to the Emperor will last forever.")
    quit()


#  ----------------------------------------------Events Management---------------------------------------------------  #
def manage_events(board: dict, character: dict) -> None:
    """
    Manage the event.

    :param board: a dictionary
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: character's X-coordinate and Y-coordinate must be in bounds of board
    :precondition: board must be a dictionary
    :precondition: board must be a valid board created with generate_random_room_event function
    :postcondition: manages the event that is associated with current character's X-coordinate and Y-coordinate
    :postcondition: launches the boss event if event is boss function
    :postcondition: passes event to event_with_input function if event has Input key
    :postcondition: passes event to event_with_effect function if event has Effect key
    :postcondition: changes the value of board dictionary at character's X-coordinate, Y-coordinate to "There is
                   nothing here anymore" and set value of After-effect to False if event's After-effect is a key in
                    event dictionary and its value is True
    :postcondition: prints the event's description
    :postcondition: print the ending phrase
    :return: None
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
                "This room has an ancient altar. It feels nostalgic somehow."
            ],
            "Effect": [
                ("Heal", "Despite its blasphemous appearance, it heals you innocently still."),
                ("Heal", "All your wounds are healed.")
            ]
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
                    "Item": [
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
                "This room has an altar in the form of a star that pierces a crescent moon; it reminds you of Slaanesh."
                "",
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
                        ("Nothing", "You do not want it anyway.")
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
                        ("Nothing", "You decide not to loot anything.")
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
                        ("Nothing", "You decide not to toy with the Necronian heresy.")
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
                        ("Nothing", "You have no time to waste.")
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
                        ("Nothing", "You decide not to wear anything.")
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
                "This room is full of robotic skulls.",
                "This room a robotic skeleton sitting on a throne."
            ],
            "Effect": [
                ("Nothing", "Dead men remain dead."),
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
                        ("Damage", "A small spider bites while you try to break through the web. It"
                                   " takes away 4 of your wounds"),
                        ("Battle", 2, "the giant spider", "A giant spider is not fond of your intrusion ")
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
                                                     " A shapeless congeries of protoplasmic bubbles and myriads of "
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
                        ("Nothing", "You decide not to wear anything.")
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
                        ("Nothing", "You clear path without a single problem."),
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
                        ("Nothing", "You eventually find your way.")
                    ]
                }
            }
         }
    }
    event = board[(character["Y-coordinate"], character["X-coordinate"])]
    if event == boss:
        event(character)
    else:
        print("\n" + random.choice(events_dictionary[event]["Description"]))
        if "Input" in events_dictionary[event].keys():
            event_with_input(character, events_dictionary[event])
        if "Effect" in events_dictionary[event].keys():
            event_with_effect(events_dictionary[event]["Effect"], character)
        if "After-effect" in events_dictionary[event].keys() and events_dictionary[event]["After-effect"]:
            board[(character["Y-coordinate"], character["X-coordinate"])] = "There is nothing here anymore"
            events_dictionary[event]["After-effect"] = False
    print("Time to move.")
    proceed_further()


def event_with_input(character: dict, event: dict) -> None:
    """
    Process the event with input.

    This is a helper function manage_events.

    :param character: a dictionary
    :param event: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: event must be a dictionary
    :precondition: event must be a valid event passed by manage_events from events_dictionary
    :postcondition: prints event's Input description
    :postcondition: prints the list of options to choose from where yes is 1 and 2 is no
    :postcondition: passes event["Input"]["Yes"] to event_with_check_of_item function if
                    user_input is 0 and if event["Input"]["Yes"]  dictionary has "Check item" in it
    :postcondition: passes event["Input"]["Yes"] to event_effect_or_item function and sets event's After-effect value
                    to true if user_input is 0, but event["Input"]["Yes"] dictionary has no "Check item" key in it
    :postcondition: passes event to event_effect_or_item function and sets the value of event["After-effect"] to True
                    if user_input is 0, but other conditions above are False
    :postcondition: passes event["Input"]["No"] to event_effect_or_item function if none of the above conditions are met
    :return: None
    """
    print(event["Input"]["Description"])
    print_numbered_list_of_possibilities(["Yes", "No"])
    user_input = int(process_input(character, ["Yes", "No"])) - 1
    if user_input == 0:
        if "Check item" in event["Input"]["Yes"]:
            event_with_check_of_item(character, event)
        else:
            event_effect_or_item(character, event["Input"]["Yes"])
            event["After-effect"] = True
    else:
        event_effect_or_item(character, event["Input"]["No"])


def event_effect_or_item(character: dict, effect_or_item: dict) -> None:
    """
    Process the event with effect or item.

    This is a helper function to event_with_input and event_with_check_of_item functions.

    :param character: a dictionary
    :param effect_or_item: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: effect_or_item must be a dictionary
    :precondition: effect_or_item must be part of a event dictionary passed by event_with_input or
                   event_with_check_of_item functions
    :postcondition: passes effect_or_item["Effect"] to event_with_effect function if effect_or_item dictionary has a
                    Effect as a key
    :postcondition: passes effect_or_item["Item"] to event_with_item function if effect_or_item dictionary has a
                    Item as a key
    :return: None
    """
    if "Effect" in effect_or_item.keys():
        event_with_effect(effect_or_item["Effect"], character)
    if "Item" in effect_or_item.keys():
        event_with_item(effect_or_item["Item"], character)


def event_with_check_of_item(character: dict, event: dict) -> None:
    """
    Process the event with check of item.

    This is a helper function to event_with_input.

    :param character: a dictionary
    :param event: a dictionary
    :precondition: event must be a valid event passed by event_with_input function from manage_events function
                   from events_dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: passes event["Input"]["Yes"] to event_effect_or_item function, decrements the amount of checked
                    item by and sets event["After-effect"] to True if has_item function returns True
    :postcondition: passes event["Input"]["No"]["Effect"] to event_with_effect function and prints failed check phrase
                    if has_item function returns False
    :return: None
    """
    if has_item(event["Input"]["Yes"]["Check item"], character):
        character["Inventory"][event["Input"]["Yes"]["Check item"]] -= 1
        event_effect_or_item(character, event["Input"]["Yes"])
        event["After-effect"] = True
    else:
        print("You have no such item.")
        event_with_effect(event["Input"]["No"]["Effect"], character)


def event_with_effect(effects: list, character: dict) -> None:
    """
    Process the random effect of the event.

    :param effects: a list of tuples
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: effects must be a list
    :precondition: effects must be a part of events_dictionary from manage_events function
    :postcondition: prints the effect description
    :postcondition: increases character["Current Wounds"] if effect is Heal
    :postcondition: deals 4 damage to character if effect is Damage
    :postcondition: increases character["Current experience"] by 50 if effect is Experience gain
    :postcondition: decreases the value of a random character["Characteristics"] key if effect is
                    Random Stat Deterioration
    :postcondition: increases the value of a random character["Characteristics"] key if effect is
                    Random Stat Improvement
    :postcondition: initiates combat of character with the effect's enemy if effect is Battle
    :return: None
    """
    effect = random.choice(effects)
    print(effect[-1])
    character["Current wounds"] = character["Max wounds"] if effect[0] == "Heal" else character["Current wounds"]
    if effect[0] == "Damage":
        manage_wounds(4, character, unavoidable=True)
    character["Current experience"] += 50 if effect[0] == "Experience gain" else 0
    if effect[0] == "Random Stat Improvement" or effect[0] == "Random Stat Deterioration":
        stat = random.choice(list(character["Characteristics"].keys()))
        character["Characteristics"][stat] += 2 if effect[0] == "Random Stat Improvement" else -2
        print("Your {0} is {1} by 2".format(stat, "increased" if effect[0] == "Random Stat Improvement"
                                            else "decreased"))
    if effect[0] == "Battle":
        combat(character, generate_enemy(effect[1], effect[2]))


def event_with_item(items: list, character: dict) -> None:
    """
    Process the random item of the event

    :param items: a list of tuples
    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :precondition: items must be a list
    :precondition: items must be a part of events_dictionary from manage_events function
    :postcondition: prints the item description
    :postcondition: increases character["Max wounds"] and character["Current wounds"] by 2 if item is Armor
    :postcondition: increases character["Max wounds"] and character["Current wounds"] by 1 if item is Broken Armor
    :postcondition: increases the amount of item in the character["Inventory"] if the conditions above are not met
    :return:
    """
    item = random.choice(items)
    print(item[1])
    if "Armor" in item[0]:
        character["Max wounds"] += 2 if item[0] == "Armor" else 1
        character["Current wounds"] += 2 if item[0] == "Armor" else 1
    elif item[0] in character["Inventory"]:
        character["Inventory"][item[0]] += 1
    else:
        character["Inventory"].setdefault(item[0], 1)


#                                           Event Management: Special Events                                           #
def tutorial(character: dict) -> None:
    """
    Guide the new player.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints story plot
    :postcondition: prints useful commands
    :postcondition: prints option choosing tip
    :postcondition: initiates combat between character and the rat
    :return: None
    """
    proceed_further()
    print("\n\tYour inquisitor, Scythia, gave a you crucial tusk to retrieve a Necronian artifact. She enlightens you "
          "that it's a sphere of incredible power. Surprisingly, no one\nknows what it does, but every cultist desires"
          " it. Hence, it's now your job as an acolyte to retrieve the miserable artifact that lies among the ruins of"
          "great stasis-tombs."
          "\n\tYou arrive to unnamed, deserted planet. Nothing indicates that here was once a paramount nation of"
          "servants of C'tan. Eventually, you found the ruins matching the\nNecronian decor."
          "\n\tAs you enter the tomb, it strikes you as odd. The insides of this dungeon are far from being ruins;"
          "it is rather the complete opposite of what you saw before. The\nsoft green light of some unknown kind of "
          "latter kindly lightens the room. Apparently, it was a complete waste of time to bring torches with or was "
          "it?. A sudden feel of being\nwatched stops your vague reflection. You turn around and notice a giant rat "
          "greedily watching you."
          "\n\tYour mission begins."
          "\nHere are some helpful tips for your path of inquisitor:")
    proceed_further()
    help_commands()
    print("\n\nTo choose an option from a numbered list enter its index.")
    proceed_further()
    combat(character, generate_enemy(1, "the rat"))


def boss(character: dict) -> None:
    """

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character must be a valid character created by character_creation function
    :postcondition: prints the "you are not ready" phrase and moves character to the previous coordinates if character
                    Level is not 3
    :postcondition: prints the boss' intro phrase, adds "Artifact" key with value of "Necronian artifact" to character,
                    initiates combat with the boss and removes Flee Away skill if character Level is 3
    :return: None
    """
    if character["Level"][0] != 3:
        print("Fear takes control over you as soon as you get close to this room.\n"
              "You feel like you have to get more experience before facing it.\nYou decide to retreat.")
        move_character(character)
    else:
        print("\n\tYou enter the dreadful room. The Necronian decor exactly matches the description "
              "the Inquisitor gave you"
              ". However, your joy deserves rapidly as you notice a gigantic\ndaemon holding the precious artefact"
              "you are tasked to retrieve. The daemon notices you and smirks. His grotesque claws reveals his name ——"
              "Goreclaw the Render, a\nDaemon Prince of Khorne —— infamous among the inquisitors of this galaxy."
              "\n\nYou know it will be a deadly battle with no opportunity to flee."
              "\n\"Bring. It. On,\" his monstrous majesty mandates")
        character.setdefault("Artifact", "Necronian artifact")
        character["Skills"].pop("Flee Away")
        combat(character, generate_enemy("Boss", "Boss"))


def game_over(character: dict) -> None:
    """
    Print game over phrase.

    :param character: a dictionary
    :precondition: character must be a dictionary
    :precondition: character keys must contain Current wounds string
    :precondition: character value with Current wounds key must be an integer
    :postcondition: prints "you died\n game over" ascii art if Current wounds <= 0,
                    else prints "congratulations" ascii art and victory phrase
    """
    if not is_alive(character):
        print(
                (red_text() +
                 "▓██***██▓****▒█████******█****██**********▓█████▄*****██▓***▓█████****▓█████▄****\n"
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
                 + normal_text()))
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
