# To run the code, use python3 run.py in a terminal, after changing the values specified below in this file.

'''
Briscola suit is the trump suit of a round. This suit should beat every other suit regardless of value
Suits below can be one of the following: 'Swords', 'Cups', 'Clubs' or 'Coins'
'''
briscola_suit='Swords' 


'''
Change the configuration below to change the hands that players start with.
- Values can be, from lowest to highest priority, 2, 3, 4, 5, 6, 7, J, H, K, 3 or A. 
- Suits can be one of the following: Swords, Cups, Clubs or Coins
- Cards must be formated as "<value> of <suit>".
'''
starting_hands=[["A of Cups", "7 of Cups", "2 of Swords"],
                ["A of Coins","H of Swords","4 of Clubs"],
                ["A of Swords","J of Clubs","K of Coins"],
                ["A of Clubs","3 of Coins","5 of Cups"]]


# These 4 cards in play were originally used to test if the model could determine which set of cards would win 1 trick.
#cards_in_play=["H of Swords", "7 of Cups", "J of Clubs", "3 of Coins"]
#cards_in_play=["3 of Clubs", "A of Cups", "A of Clubs", "5 of Cups"]
#cards_in_play=["2 of Coins", "3 of Swords", "A of Swords", "6 of Cups"]
#cards_in_play=["3 of Cups", "K of Coins", "A of Clubs", "2 of Cups"]