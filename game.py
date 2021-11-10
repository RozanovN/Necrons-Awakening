"""
Your name:
Your student number:

All of your code must go in this file.

Questions to ask:
1. Can you use tabletop game's text and mechanics?
2. How to commit this assignment?
3. String formatting
4. Structure of classes (adepts)
5. Character creation functions in the dictionary
6. usage of quit()
7. text color globals


"""
import random
import time


def game():
    """

    """
    rows = 25
    columns = 25
    board = make_board(rows, columns)
    print("""You stand on the front line of a great and secret war. As an Acolyte of the powerful
    Inquisition, you will root out threats to the Imperium of Man. You will engage in deadly combat
    against heretics, aliens and witches.""")
    print("""But perhaps the biggest threat you face is your fellow man, for the human soul is such 
    fertile ground for corruption. It is your duty to shepherd mankind from the manifold paths 
    of damnation""")
    print("Prior to starting your service to the Emperor, you must first create a character")
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
