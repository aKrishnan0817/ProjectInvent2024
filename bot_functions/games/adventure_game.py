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
            "initial_description": "You are standing in an open field. There's nothing worth noticing here. There are, however, two roads. The right road leading into a house, the other into a forest.",
            "description": "You are back at the field. You can go right into the house, and left into forest.",
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
        # movement + search + help
        game_room = game_map[player_data['location']]
        valid_moves = list(game_room['choices'].keys()) + ['search', 'help']

        if not game_room['visited']:
            print(game_room['initial_description'])
            game_room['visited'] = True
        else:
            print(game_room['description'])

        print("Please enter a move: ", end='')
        player_move = input()
        while player_move not in valid_moves:
            print('That is not a valid move. The moves you can make right now are:', ', '.join(valid_moves))



if __name__ == "__main__":
    main()
