from colorama import Fore, Style, init

# Initialize colorama (important for Windows compatibility)
init(autoreset=True)

def display_health_bar(stat_name, value, bar_length=20):
    """
    Display a colored health bar for any stat in the command line, formatted neatly.

    Args:
        stat_name (str): The name of the stat, e.g., 'Health' or 'Mana'.
        value (int): The current value of the stat, between 0 and 100.
        bar_length (int): The length of the visual bar. Default is 20.
    """
    # Clamp the value between 0 and 100
    value = max(0, min(100, value))
    
    # Align stat names to the same width
    stat_name = stat_name.ljust(8)  # Adjust 8 to fit your longest stat name

    # Calculate how many blocks are filled
    filled_length = int((value / 100) * bar_length)

    # Choose color based on value
    if value >= 70:
        color = Fore.GREEN
    elif value >= 30:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    # Create the bar
    bar = color + "█" * filled_length + Style.RESET_ALL + "-" * (bar_length - filled_length)

    # Color the numeric value too
    value_color = color + f"{value}" + Style.RESET_ALL

    # Print formatted bar
    print(f"{stat_name}: |{bar}| {value_color}/100")


# Example usage
display_health_bar("Health", 85)
display_health_bar("Mana", 45)
display_health_bar("Stamina", 15)
display_health_bar("Shield", 100)
