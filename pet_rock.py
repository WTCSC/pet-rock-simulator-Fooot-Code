from colorama import Fore, Style, init
import time
from random import choice

def displayStatBar(statsDict: dict, bar_length=20):
    """
    Display a colored health bar for any stat in the command line, formatted neatly.

    Args:
        stat_name (str): The name of the stat, e.g., 'Health' or 'Mana'.
        value (int): The current value of the stat, between 0 and 100.
        bar_length (int): The length of the visual bar. Default is 20.
    """

    for statName, statValue, in statsDict.items():
        if isinstance(statValue, float):
            # Clamp the value between 0 and 100
            statValue = max(0, min(100, statValue))
            
            # Align stat names to the same width
            statName = statName.ljust(len(max(statsDict.keys(), key=len)))  # Adjusts to fit longest stat name

            # Calculate how many blocks are filled
            filled_length = int((statValue / 100) * bar_length)

            # Choose color based on value
            if statValue >= 70:
                color = Fore.GREEN
            elif statValue >= 30:
                color = Fore.YELLOW
            else:
                color = Fore.RED

            # Create the bar
            bar = color + "█" * filled_length + Style.RESET_ALL + "-" * (bar_length - filled_length)

            # Color the numeric value too
            value_color = color + f"{statValue}" + Style.RESET_ALL

            # Print formatted bar
            print(f"{statName}: |{bar}| {value_color}/100")

def passiveStatUpdate(statsDict: dict):
    statsDict["Happiness"] -= 10
    statsDict["Hunger"] -= 10
    statsDict["Cleanliness"] -= 10
    statsDict["Age"] = (statsDict["Age"] - time.time()) / 60 # Age in minutes

def actionStatUpdate(dictToChange: dict, happinessChange: int, hungerChange: int, cleanlinessChange: int):
    dictToChange["Happiness"] += happinessChange
    dictToChange["Hunger"] += hungerChange
    dictToChange["Cleanliness"] += cleanlinessChange

    return dictToChange
    


def isAlive(statsDict: dict):
    if statsDict["Age"] > 3 or statsDict["Happiness"] <= 0 or statsDict["Hunger"] <= 5 or statsDict["Cleanliness"] <= 10:
        return False
    return True

rockName = input("Welcome! What would you like to name your rock?\n")
rockStats = {"Name": rockName, "Alive": True, "Happiness": 100.0, "Hunger": 100.0, "Cleanliness": 100.0, "Age": time.time()}
foodChoices = ["Apple", "Banana", "Grape", "Pineapple"]

while rockStats["Alive"]:
    print(f"{rockStats["Name"]}'s Stats: ")
    displayStatBar(rockStats)
    
    print("What would you like to do with your rock?")
    print("1. Play")
    print("2. Feed")
    print("3. Pet")
    print("4. Bathe")
    print("5. Do Nothing")
    activity = int(input())

    if activity == 1:
        print(f"You and {rockStats["Name"]} go outside and play fetch! {rockStats["Name"]} didn't really move that much, but it still had fun!")
        rockStats = actionStatUpdate(rockStats, 40, -20, -20)



    elif activity == 2:
        randomFood = choice(foodChoices)
        print(f"You feed {rockStats["Name"]} a {randomFood}! Despite it not eating the {randomFood}, {rockStats["Name"]} is less hungry!")
        rockStats = actionStatUpdate(rockStats, 20, 100 - rockStats["Hunger"], -5)

    elif activity == 3:
        print(f"{rockStats["Name"]} is now very happy! It did not react to your petting, but {rockStats["Name"]} still enjoyed it a lot!")
        rockStats = actionStatUpdate(rockStats, 20, -10, -10)

    elif activity == 4:
        print(f"You bathe {rockStats["Name"]}. It becomes more clean, but it is very scared of water! Why would you do this to {rockStats["Name"]}?!?!?!")
        rockStats = actionStatUpdate(rockStats, -20, -5, 100 - rockStats["Cleanliness"])
    
    elif activity == 5:
        print(f"Doing nothing with {rockStats["Name"]}, huh? Do you hate it??? Why did you even adopt it anyway???")

    else:
        print(f"{rockStats["Name"]} is confused. What do you want to do again?")
        answerOptions = [range(1, 6)]
        activity = input("Enter activity: ")
        while activity not in answerOptions:
            print(f"{rockStats["Name"]} is confused. What do you want to do again?")
            activity = input("Enter activity: ")

    time.sleep(4)

    passiveStatUpdate(rockStats)
    rockStats["Alive"] = isAlive(rockStats)