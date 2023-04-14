
import time
from colorama import init, Fore, Back, Style

def intro_text():
    # Initialize colorama
    init()

    # Define the animation frames
    frames = ["\U0001F34D", "\U0001F353", "\U0001F99E", "\n ***Welcome to super mark***", "\n Database created"]

    # Loop through frames and print each one with alternating colors 
    for i, frame in enumerate(frames):
        if i % 2 == 0:
            print(Back.BLUE + Fore.RED + frame + Style.RESET_ALL, end='', flush=True)
        else:
            print(Back.RED + Fore.BLUE + frame + Style.RESET_ALL, end='', flush=True)
        time.sleep(1)

