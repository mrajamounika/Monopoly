from classes import card_info as c_info


def move(nick, board):

    if nick.in_jail:
        leave_jail(nick, board)

    dice_roll = nick.roll_dice()
    nick.player_turn(dice_roll)
    curr_card = board[nick.current_pos % 40]
    purchasable = nick.position_check(board)

    if purchasable and nick.balance > curr_card.card_cost:
        curr_card.purchase_card(nick)
        print(f"{nick.name} has purchased {curr_card.card_name}")


def leave_jail(nick, board):
    nick.reduce_balance(50)
    nick.in_jail = False
    print(f"{nick.name} has paid the $50 bail and has been released from jail.")
    move(nick, board)


def evaluate_trade(human, nick, money_offered, props_present, money_wanted, properties_wanted, board):
    personal_gain = 0
    human_gain = 0

    properties_valuation_personal = 0

    benefit = 0

    if nick.balance < 200:
        multiplier = 5
    else:
        multiplier = 2.5

    if props_present[0] == '':
        pass
    else:
        for card_name in props_present:
            card_object = c_info.identify_card(card_name, board)
            personal_gain += card_object.card_cost

    if properties_wanted[0] == '':
        pass
    else:
        for card_name in properties_wanted:
            card_object = c_info.identify_card(card_name, board)
            human_gain += card_object.card_cost

       
        for card_name in props_present:

            card_offered = c_info.identify_card(card_name, board)

            properties_valuation_personal += (money_offered-card_offered.card_cost) / card_offered.card_cost * multiplier

            
            card_group = card_offered.color_group
            num_properties_in_group = 0

            for card in nick.cards_owned:
                if card.color_group == card_group:
                    num_properties_in_group += 1

            benefit += 10 + (10 * num_properties_in_group)

        for card_name in properties_wanted:

            card_wanted = c_info.identify_card(card_name, board)

            

            card_group = card_wanted.color_group
            num_properties_in_group = 0

            for card in nick.cards_owned:
                if card.color_group == card_group:
                    num_properties_in_group += 1

            benefit -= 40 + (num_properties_in_group * 10)

   
    personal_gain += (money_offered - money_wanted) * multiplier/10


    print(f"Personal gain: {personal_gain}. Human gain: {human_gain}")
    if personal_gain > human_gain + 10:
        return 1
    else:
        return 0

