
# TO USE THIS DRAFT: Change the following suits below to see which cards should beat what in each scenario.

# Suits below can be one of the following: 'Swords', 'Cups', 'Clubs' or 'Coins'

briscola_suit='Swords' # Briscola suit is the trump suit of a round. This suit should beat every other suit regardless of value
round_suit='Cups' # 'Round Suit' is the leading suit of the round. This suit should beat any other suit, excluding the Briscola suit

check_suit='Swords' # Change this suit to see which suit will beat what kind of cards in the function output.

# To run the code, use python3 run.py in a terminal, after changing the values in this file.


starting_hands=[["A of Cups", "7 of Cups", "2 of Swords"],
                ["A of Coins","H of Swords","4 of Clubs"],
                ["A of Swords","J of Clubs","K of Coins"],
                ["A of Clubs","3 of Coins","5 of Cups"]]




# Below are values that cannot change results yet (these are works in progress).

# Card order is based off of order in the list.
#cards_in_play=["H of Swords", "7 of Cups", "J of Clubs", "3 of Coins"]
#cards_in_play=["3 of Clubs", "A of Cups", "A of Clubs", "5 of Cups"]
#cards_in_play=["2 of Coins", "3 of Swords", "A of Swords", "6 of Cups"]
cards_in_play=["3 of Coins", "K of Coins", "A of Clubs", "2 of Cups"]

#card_to_win="H of Swords"
#player_to_win="P2"