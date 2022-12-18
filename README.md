# Monopoly

CPSC 335
Monopoly Project
Fall Semester 2022

Nicholas Harney
Sri Satya Gopisetty
Raja Mounika Meka


Our Monopoly project is written in Python code.  

To run the program and start the game, Open the monopolystart.py file and run the code.

On first initialization as the players are hardcoded with 2 players and a computer player, the game provides the options to choose the actions to be performed by the player.

On choosing the option it provides the information accordingly. On initiating the code in monopolystart.py it calls the instructions from the information.py.

Information.py contains all the information regarding the properties - their details like the group, cost and utilities – like jail, community chest, income taxes and their charges available in the game.

We have two classes – card_info.py and player_info.py

card_info.py: This class keeps the information regarding the card owner, identify, buy, and sell the property information.

Player_info.py: This class keeps the information about the options to choose when the player turn comes like if to roll the dice, to check the amount, properties owned by the player. This class keeps the record of 
1.Which player has to play
2.how much amount is present with every player
3. the position of players
4. Deduction of amount if a player buys a property or lands in utilities, or to pay rent.
5.To check if bankrupt.

comp.py: The code for automated actions are provided here, like the computer’s turn and how the actions are going to take place when a computer turns come.
