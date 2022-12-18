from classes import player_info as p_info
from game import information as info
from ai import comp 

board = info.properties_and_utilities()

Sam = p_info.Player("Sam", 2000, [], 0, False, 0, 0, 0, False)
Sri = p_info.Player("Sri", 2000, [], 0, False, 0, 0, 0, False)
Nick = p_info.Player("Nick", 2000, [], 0, False, 0, 0, 0, False)
player_list = [Sam, Sri, Nick]


def total_bankrupt_players(players):
   
    counter = 0
    for player in players:
        if player.bankruptcy_status:
            counter += 1
    return counter


def declare_winner(players):

    for player in players:
        if player.bankruptcy_status == False:
            return player.name


if __name__ == "__main__":
    print("Beginning game!")
    info.instructions()

    i = 0
    # continue running while there is more than one non-bankrupt player remaining.
    while total_bankrupt_players(player_list) != len(player_list)-1:
        i = i % len(player_list)

        print()
        print(f"{player_list[i].name}'s turn:")

        if player_list[i].name == "Nick":
            comp.move(Nick, board)

        else:
            user_choice = input("What do you want to do? ")
            result = player_list[i].game_options(user_choice, player_list, Nick, board)
            while result == -1:  # keep asking the user until they choose to roll the dice.
                user_choice = input("What do you want to do? ")
                result = player_list[i].game_options(user_choice, player_list, Nick, board)
            new_pos = player_list[i].player_turn(result)
            player_list[i].position_check(board)

        i += 1

    print(f"Game over! {declare_winner(player_list)} has won!")
