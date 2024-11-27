# To run the code, use python3 run.py in a terminal, after changing the values in this file.

# Suits below can be one of the following: 'Swords', 'Cups', 'Clubs' or 'Coins'

briscola_suit='Swords' # Briscola suit is the trump suit of a round. This suit should beat every other suit regardless of value




# Note that at the start of the game, player 1 will always be the starting player.
starting_hands=[["A of Cups", "7 of Cups", "2 of Swords"],
                ["A of Coins","H of Swords","4 of Clubs"],
                ["A of Swords","J of Clubs","K of Coins"],
                ["A of Clubs","3 of Coins","5 of Cups"]]




# Below are values that cannot change results yet (these are works in progress).

# These 4 cards in play were originally used to test if the model could determine which set of cards would win 1 trick.
#cards_in_play=["H of Swords", "7 of Cups", "J of Clubs", "3 of Coins"]
#cards_in_play=["3 of Clubs", "A of Cups", "A of Clubs", "5 of Cups"]
#cards_in_play=["2 of Coins", "3 of Swords", "A of Swords", "6 of Cups"]
cards_in_play=["3 of Cups", "K of Coins", "A of Clubs", "2 of Cups"]