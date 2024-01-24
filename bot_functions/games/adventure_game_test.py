def main():
    player_data = {
        "pass": [-1, -1, -1, -1],
        "key_one": False,  # red
        "key_two": False,  # blue
        "power": False,
        "coins": False,
        "location": "start"
    }

    # Game Loop
    while True:
        if player_data["location"] == "start":
            print("Start")

        input()




if __name__ == "__main__":
    main()