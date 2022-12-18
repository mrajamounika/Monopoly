class Card:
    def __init__(self, card_name, color_group, card_cost, house_cost, houses_built, rent_prices, mortgage_amt, owner, mortgaged):
        self.card_name = card_name                  
        self.color_group = color_group              
        self.card_cost = card_cost                  
        self.house_cost = house_cost                
        self.houses_built = houses_built            
        self.rent_prices = rent_prices              
        self.mortgage_amt = mortgage_amt            
        self.owner = owner                          
        self.mortgaged = mortgaged                  

    def sell(self, player):
        
        player.add_balance(self.card_cost)
        self.owner = 'Bank'

    def purchase_card(self, player):
        
        if self.card_cost > player.balance:
            print("You cannot afford this card at the moment.")
        else:
            player.cards_owned.append(self)
            player.deduct_amount(self.card_cost)
            self.owner = player
def identify_card(name, board):

    for card in board:
        if card.card_name == name:
            card_object = card
            break
    return card_object
