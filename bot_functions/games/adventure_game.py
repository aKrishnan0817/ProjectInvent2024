def main():
    player_data = {
        "pass": [-1, -1, -1, -1],
        "inventory": {},
        "location": "start"
    }

    """
    "key_one": False,  # red
    "key_two": False,  # blue
    "power": False,
    "coins": False,
    """

    game_map = {
        "start": {
            "name": "start",
            "initial_description": "You are standing in an open field. There's nothing worth noticing here. There "
                                   "are, however, two roads. The right road leading into a house, the other into a "
                                   "forest.",
            "description": "You are at the field. You can go right into the house, and left into forest.",
            "visited": False,
            "choices":
                {
                    "left": "crossroads",
                    "right": "house",
                },
            "search": {}
        },

        "crossroads": {
            "name": "crossroads",
            "initial_description": "You walk through the forest, and suddenly find yourself standing at a crossroads. "
                                   "You will only see this message the first time you enter this area",
            "description": "You are at the crossroads",
            "visited": False,
            "choices":
                {
                    "backwards": "start"
                }
        },

        "house": {
            "name": "house",
            "initial_description": "You are at the house, and will only see this message the first time you enter "
                                   "this area",
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
        valid_moves = list(game_room['choices'].keys()) + ['search', 'help', 'look', 'inspect']

        if not game_room['visited']:
            print(game_room['initial_description'])
            game_room['visited'] = True
        else:
            print(game_room['description'])

        while True:
            print("Please enter a move: ", end='')
            player_move = input()
            while player_move not in valid_moves:
                print('That is not a valid move. The moves you can make right now are:', ', '.join(valid_moves))
                print("Please enter a move: ", end='')
                player_move = input()

            if player_move == "help":
                print('The moves you can make right now are:', ', '.join(valid_moves))

            elif player_move == 'look':
                if game_room['visited']:
                    print(game_room['initial_description'])
                else:
                    print(game_room['description'])
            else:
                break

        # check if player wants to move
        if player_move in ['right', 'left', 'forwards', 'backwards']:
            print("Travelling...")
            player_data["location"] = game_room["choices"][player_move]

        game_room['visited'] = True


if __name__ == "__main__":
    main()
