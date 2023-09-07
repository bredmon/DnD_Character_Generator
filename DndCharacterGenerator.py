# Dungeons & Dragons Character Generator

# Import all of the required libraries
import sys
import pandas as pd
from random import randrange
from colorama import Fore


# Asks the user if they want to generate another character and returns True or False
def restart_program():
    restart = (
        input(Fore.RESET + "Do you want to generate another character? (Y)es or (N)o\n")
        .strip()
        .lower()
    )
    if "y" not in restart:
        return False
    else:
        return True


# Prints the final character using color-coding
def output_character(
    multi_class, first_subclass, first_class, second_subclass, second_class
):
    if multi_class:
        print(
            Fore.RED
            + first_subclass.rstrip()
            + " "
            + Fore.BLUE
            + first_class.rstrip()
            + Fore.MAGENTA
            + " /// "
            + Fore.RED
            + second_subclass.rstrip()
            + " "
            + Fore.BLUE
            + second_class.rstrip()
            + Fore.RESET
        )
    else:
        print(
            Fore.RED + first_subclass.rstrip() + " " + Fore.BLUE + first_class.rstrip()
        )


# Chooses a valid sub-class for the given character class
def select_subclass(data_frame, character_class):
    valid_subclasses = data_frame[data_frame["Class"] == character_class]
    unique_subclasses = list(set(list(valid_subclasses["Subclass"])))
    return unique_subclasses[randrange(0, len(unique_subclasses))]


# Asks user if they want to multiclass and returns True or False
def select_multi_classing():
    while True:
        multi_class_choice = (
            input(Fore.RESET + "Do you want to multi-class? (Y)es or (N)o\n")
            .strip()
            .lower()
        )
        if "y" in multi_class_choice:
            return True
        elif "n" in multi_class_choice:
            return False


# Returns a filtered Pandas dataframe when using Standard content, or unfiltered for Expanded
def select_content(data_frame):
    # Loop until the user makes a valid choice
    while True:
        content_choice = (
            input(Fore.RESET + "Do you want to use (S)tandard or (E)xpanded content?\n")
            .strip()
            .lower()
        )

        # Standard content only uses content which contains the string "Player's Handbook" in the "Source" column
        if "s" in content_choice:
            data_frame = data_frame[
                data_frame["Source"].apply(lambda x: "Player's Handbook" in x)
            ]
            break
        # Expanded content uses all available source materials in the file
        elif "e" in content_choice:
            break
    return data_frame


# This part of the codes should only execute when this script is run directly
if __name__ == "__main__":
    # Greet the user
    print(Fore.GREEN + "Welcome to the D&D Character Generator!")

    # Loop until user cancels
    generate_class = True
    while generate_class == True:
        # Try to load the file into a Pandas dataframe, exit upon exception
        try:
            # Set the file path for the classes and subclasses
            file_path = r"./classes_and_subclasses.csv"
            data_frame = pd.read_csv(file_path)
        except:
            sys.exit("Could not open file - exiting...")
        try:
            # Prompt the user for Standard or Expanded content
            data_frame = select_content(data_frame)

            # Prompt the user for multi-classing
            multi_class = select_multi_classing()

            # Create a set of unique classes from a list of duplicate classes, and turn into a list for ease of use
            classes = data_frame["Class"]
            unique_classes = list(set(list(classes)))

            # Pick the 1st class and remove it from the list
            first_class = unique_classes.pop(randrange(0, len(unique_classes)))

            # Pick a valid subclass for the 1st class
            first_subclass = select_subclass(data_frame, first_class)

            # Pick the 2nd class
            second_class = None
            second_subclass = None
            if multi_class:
                second_class = unique_classes.pop(randrange(0, len(unique_classes)))

                # Pick a valid subclass for the 2nd class
                second_subclass = select_subclass(data_frame, second_class)

            # Output the sub-class and class combination(s)
            output_character(
                multi_class, first_subclass, first_class, second_subclass, second_class
            )

            # Prompt user to restart program
            generate_class = restart_program()

        # Exit when Control + C is pressed
        except KeyboardInterrupt:
            sys.exit("Exiting...")
        # Exit when other exceptions are caught
        except Exception as e:
            sys.exit(f"Encountered {e} - exiting...")
