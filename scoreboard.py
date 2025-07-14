import json
import os

SCOREBOARD_FILE = "scoreboard.json"

def load_scoreboard():
    '''
    Load scoarboard from JSON file
    If file doesn't exist, return empty dictionary
    '''
    if not os.path.exists(SCOREBOARD_FILE):
        return {}
    with open(SCOREBOARD_FILE, "r") as f:
        return json.load(f)

def save_scoreboard(scoreboard):
    '''
    Save given scoreboard dictionary to JSON file
    Use indentation for readability
    '''
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scoreboard, f, indent=4)

def update_scoreboard(winner_name=None, draw=False, player_names=[]):
    '''
    Updates scoreboard:
    - If draw, +1 to each player in player_names
    - If winner, +2 to winner
    Then save upaded scoreboard to file
    '''
    scoreboard = load_scoreboard()
    if draw:
        for name in player_names:
            scoreboard[name] = scoreboard.get(name, 0) + 1
    elif winner_name:
        scoreboard[winner_name] = scoreboard.get(winner_name, 0) + 2
    save_scoreboard(scoreboard)

def get_scoreboard():
    '''
    Return current scoreboard as dictionary
    Loads scoreboard from file each time
    '''
    return load_scoreboard()
