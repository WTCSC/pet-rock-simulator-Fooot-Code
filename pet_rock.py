from colorama import Fore, Style, init
import time
from random import choice

def displayStatBar(statsDict: dict, bar_length=20):
    """
    Display a colored health bar for the main stats (Happiness, Hunger, Cleanliness, Age).
    """

    # Only include stats we want to display
    displayKeys = ["Happiness", "Hunger", "Cleanliness", "Age"]

    for statName in displayKeys:
        if statName not in statsDict:
            continue

        statValue = statsDict[statName]

        if isinstance(statValue, (float, int)):
            # Clamp values
            statValue = max(0, min(100, statValue)) if statName != "Age" else statValue  

            # Align names
            statNamePadded = statName.ljust(len(max(displayKeys, key=len)))

            # Calculate filled bar length
            filled_length = int((statValue / 100) * bar_length) if statName != "Age" else 0

            # Pick color
            if statName == "Age":
                color = Fore.CYAN
            elif statValue >= 70:
                color = Fore.GREEN
            elif statValue >= 30:
                color = Fore.YELLOW
            else:
                color = Fore.RED

            # Make bar
            if statName == "Age":
                # Show age as plain number, no bar
                print(f"{statNamePadded}: {color}{statValue:.2f} min{Style.RESET_ALL}")
            else:
                bar = color + "█" * filled_length + Style.RESET_ALL + "-" * (bar_length - filled_length)
                value_color = color + f"{statValue:.0f}" + Style.RESET_ALL
                print(f"{statNamePadded}: |{bar}| {value_color}/100")


def passiveStatUpdate(statsDict: dict):
    newDict = statsDict.copy()

    newDict["Happiness"] -= 10
    newDict["Hunger"] -= 10
    newDict["Cleanliness"] -= 10

    return newDict

def actionStatUpdate(statsDict: dict, happinessChange: int, hungerChange: int, cleanlinessChange: int):
    updatedDict = statsDict.copy()

    updatedDict["Happiness"] += happinessChange
    updatedDict["Hunger"] += hungerChange
    updatedDict["Cleanliness"] += cleanlinessChange

    return updatedDict
    

def checkDeath(statsDict: dict):
    newDict = statsDict.copy()
    
    # compute age in minutes
    age_minutes = (time.time() - newDict["BirthTime"]) / 60
    newDict["Age"] = age_minutes

    if (
        age_minutes < ROCK_MAX_AGE
        and newDict["Happiness"] > 0
        and newDict["Hunger"] > 5
        and newDict["Cleanliness"] > 10
    ):
        return newDict  # still alive

    # death checks
    if age_minutes >= ROCK_MAX_AGE:
        newDict["DeathType"] = "Age"
    elif newDict["Happiness"] <= 0:
        newDict["DeathType"] = "Happiness"
    elif newDict["Hunger"] <= 5:
        newDict["DeathType"] = "Hunger"
    elif newDict["Cleanliness"] <= 10:
        newDict["DeathType"] = "Cleanliness"

    return newDict


rockName = input("Welcome! What would you like to name your rock?\n")
ROCK_MAX_AGE = 2 # minutes
rockStats = {"Name": rockName, 
             "DeathType": None, 
             "Happiness": 100.0, 
             "Hunger": 100.0, 
             "Cleanliness": 100.0, 
             "BirthTime": time.time()}
foodChoices = ["Apple", "Banana", "Grape", "Pineapple"]

while rockStats["DeathType"] is None:
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

    #time.sleep(4)

    rockStats = passiveStatUpdate(rockStats)
    rockStats = checkDeath(rockStats)

if rockStats["DeathType"] == "Age":
    print(f"{rockStats["Name"]} lived to its full potential of {ROCK_MAX_AGE} minutes; Great Job!")
    print("If you would like to get another, please run the script again")

elif rockStats["DeathType"] == "Happiness":
    print(f"{rockStats["Name"]} decided that it did not like the life it lived, and decided to die. Shame on you. You should've done more with {rockStats["Name"]}.")
    print("I would ask you if you want a new pet rock, but you have proved you do not deserve them.")

elif rockStats["DeathType"] == "Hunger":
    print(f"{rockStats["Name"]} has died of hunger! You are a horrible owner who doesn't know how to simply feed their pet rock. Shame on you.")
    print("I would ask you if you want a new pet rock, but you have proved you do not deserve them.")

else: #died from cleanliness
    print(f"Wow. You are a filthy owner. {rockStats["Name"]} died of cleanliness. Shame on you. It doesnt take much effort to feed your rock some food.")
    print("I would ask you if you want a new pet rock, but you have proved you do not deserve them.")