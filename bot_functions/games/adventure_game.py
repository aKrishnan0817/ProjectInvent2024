def main():
    player_data = {
        "pass": [-1, -1, -1, -1],
        "key_one": False,  # red
        "key_two": False,  # blue
        "power": False,
        "coins": False,
        "location": "start"
    }

    game_map = {
        "start": {
            "initial_description": "You find yourself at the start, and will only see this message once",
            "description": "You are back at the start",
            "visited": False,
            "choices":
                {
                    "left": "crossroads",
                    "right": "house",
                }
        },

        "crossroads": {
            "initial_description": "You are at the crossroads, and will only see this message the first time you enter this area",
            "description": "You are at the crossroads",
            "visited": False,
            "choices":
                {
                    "backwards": "start"
                }
        },

        "house": {
            "initial_description": "You are at the house, and will only see this message the first time you enter this area",
            "description": "You are at the house",
            "visited": False,
            "choices":
                {
                    "backwards": "start"
                }
        }
    }

    # Game Loop
    while True:
        if not game_map[player_data['location']]['visited']:
            print(game_map[player_data['location']]['initial_description'])
            game_map[player_data['location']]['visited'] = True
        else:
            print(game_map[player_data['location']]['description'])




if __name__ == "__main__":
    main()
