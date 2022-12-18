import random
from classes import card_info as c_info
from ai import comp


class Player:
    def __init__(self, name, balance, cards_owned, current_pos, in_jail, railroads_owned, doubles_counter, amount_owed, bankruptcy_status):
        self.name = name                            # str
        self.balance = balance                      # int
        self.cards_owned = cards_owned              # list
        self.current_pos = current_pos              # int (index)
        self.in_jail = in_jail                      # bool
        self.railroads_owned = railroads_owned      # int
        self.doubles_counter = doubles_counter      # int
        self.amount_owed = amount_owed              # int
        self.bankruptcy_status = bankruptcy_status  # bool

    def roll_dice(self):  # TODO: add check for doubles.
        
        random.seed()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        n = dice1 + dice2
        print(f"{self.name} threw {n}")
        return n

    def player_turn(self, dice_amt):
        
        self.current_pos += dice_amt
        return self.current_pos

    def position_check(self, board):
        
        self.current_pos = self.current_pos % 40
        brd_property = board[self.current_pos]

        if brd_property.card_cost == "N/A":  # this means the player cannot purchase the card

            if brd_property.card_name == 'Jail/Visiting Jail':
                print(f"{self.name} is visiting jail.")

            elif brd_property.card_name == 'Luxury Tax':
                print(f"{self.name} landed on Luxury Tax and has been fined $75")
                self.deduct_amount(75)

            elif brd_property.card_name == 'Income Tax':
                print(f"{self.name} landed on Income Tax and has been fined $200")
                self.deduct_amount(200)

            elif brd_property.card_name == 'Go to Jail':
                print(f"{self.name} landed on Go to Jail and has been arrested!")
                self.send_to_jail()

            else:
                print(f"{self.name} landed on {brd_property.card_name}")

        else:
            if brd_property.mortgaged:
                print(f"{self.name} landed on a mortgaged property.")

            elif brd_property.owner != 'Bank':  # and brd_property.owner.name != self.name:
                if brd_property.owner.name == self.name:
                    print(f"{self.name} landed on {brd_property.card_name}, a property they own.")
                else:
                    print(f"{self.name} landed on {brd_property.card_name}, a property owned by {brd_property.owner.name}")
                    self.charge_rent(brd_property)

            else:
                print(f"{self.name} landed on {brd_property.card_name}")
                if self.name == "Nick":
                    return 1  
                else:
                    user_action = input("Do you want to buy the property? (y/n) ")
                    if user_action == 'y':
                        brd_property.purchase_card(self)

    def total_amount(self, amount):
        
        self.balance += amount
        return self.balance

    def charge_rent(self, card):
        
        if card.color_group == "Railroad":
            rent_amt = 25 * card.owner.railroads_owned
        else:
            rent_amt = card.rent_prices[1]
        print(f"{self.name} is paying ${rent_amt} as a rental charge to {card.owner.name}")
        self.deduct_amount(rent_amt)
        card.owner.total_amount(rent_amt)

    def deduct_amount(self, amount):
        
        if self.balance < amount:
            print("Your balance is insufficient for this action.")
            bankrupt = self.check_if_bankrupt(amount)
            if not bankrupt:
                print("You need to sell or mortgage certain properties.")
                user_action = input("Do you want to sell or mortgage? (s/m)")
                if user_action == 's':
                    pass  # sell()  TODO: implement this function.
                else:
                    pass  # mortgage()  TODO: implement this function.
        else:
            self.balance -= amount

    def bankrupt_player(self):
        
        self.balance = 0

        if len(self.cards_owned):
            for card in self.cards_owned:
                card.owner = "Bank"
        self.railroads_owned = 0

        self.bankruptcy_status = True

    def check_if_bankrupt(self, amt_owed):
       
        net_worth = 0

        for card in self.cards_owned:
            if card.mortgaged:
                net_worth -= card.mortgage_amt
                net_worth += card.card_cost
            else:
                net_worth += card.card_cost

        if (self.balance + net_worth) < amt_owed:
            print(f"Unfortunately, {self.name} is now bankrupt! It's game over for them!")
            self.bankrupt_player()
            return True
        else:
            return False

    def player_properties(self):
        
        total = 0
        for card in self.cards_owned:
            print(f"{card.card_name}: ${card.card_cost}")
            total += card.card_cost
        print(f"The sum of your card costs is: ${total}")

    def game_options(self, user_choice, player_list, computer, board):
        
        # TODO: add sell, mortgage, and construct house functions.
        val = -1
        if user_choice == "1":
            val = self.roll_dice()
        elif user_choice == "2":
            print(f"Your balance is: ${self.balance}")
        elif user_choice == "3":
            print("Your properties are:")
            self.player_properties()
        elif user_choice == "4":
            print("Sell property feature coming soon.")

        else:
            print("Please enter a valid command.")

        return val

    def send_to_jail(self):
        
        self.current_pos = 10
        self.doubles_counter = 0

    def release_from_jail(self):
        
        self.doubles_counter = 0
        bail_choice = input("Would you like to pay the $50 bail? (y/n) ")
        if bail_choice == "y":
            self.reduce_balance(50)
            self.in_jail = False
            dice_result = self.roll_dice()
            self.player_turn(dice_result)
        else:
            self.roll_dice()
            if self.doubles_counter == 1:
                self.doubles_counter = 0
                dice_result = self.roll_dice()
                self.player_turn(dice_result)

    def trade_with_human(self, player_reference, player_list, board):

        for player in player_list:
            if player.name == player_reference:
                other_player = player

        cash_given = int(input("How much cash are you giving away? "))
        props_given= input("Enter the properties do you want to offer separated by commas\n").split(',')

        cash_received = int(input(f"How much cash is {other_player.name} giving you?"))
        received_props = input(f"Which properties is {other_player.name} giving you?\n").split(',')

        if props_given[0] == '':
            pass
        else:
            for card in props_given:
                card_object = c_info.identify_card(card, board)
                other_player.cards_owned.append(card_object)

        self.reduce_balance(cash_given)
        other_player.total_amount(cash_given)

        if received_props[0] == '':
            pass
        else:
            for card in received_props:
                card_object = c_info.identify_card(card, board)
                self.cards_owned.append(card_object)

        other_player.reduce_balance(cash_received)
        self.total_amount(cash_received)

        print(f"{self.name} has given ${cash_given} and the following properties: {props_given}")
        print(f"{other_player.name} has received ${cash_received} and the following properties: {received_props}")

    def trade_nick(self, computer, board):
        cash_offered = int(input("How much cash do you want to offer? "))
        properties_to_offer = input("Enter the properties do you want to offer separated by commas\n").split(',')

        cash_wanted = int(input("How much cash do you want the nick to give you? "))
        properties_to_receive = input("Enter the properties you want the nick to give you (separated by commas)\n").split(',')

        if comp.evaluate_trade(self, computer, cash_offered, properties_to_offer, cash_wanted, properties_to_receive, board):
            print(f"The nick has accepted your trade offer and the trade has been completed.")

        else:
            retry = input("The nick has rejected your trade offer. Do you want to suggest a different trade? (y/n")
            if retry == "y":
                self.trade_nick(computer, board)
