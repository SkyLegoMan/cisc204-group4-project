import pprint
import random

from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
from example import briscola_suit, starting_hands

# Encoding that will store all of your constraints
E = Encoding()

# Players
PLAYERS={'P1':0,'P2':0,'P3':0,'P4':0}

# Card suits and values
CARD_SUITS=['Swords', 'Coins', 'Clubs', 'Cups']
CARD_VALUES=['2','4','5','6','7','J','H','K','3','A']

# CARDS is a dictionary of cards tat specify suit and value, whilst CARD_DECK is just a list of card names
CARDS = {}
CARD_DECK = []

# Initialize valid cards, and a new randomized card deck
for s in CARD_SUITS:
    for v in CARD_VALUES:
        key_card = v + " of " + s
        CARDS[key_card] = {"suit" : s, "value" : v}
        CARD_DECK.append(key_card)

random.shuffle(CARD_DECK)


# HAS_CARD_PROP holds what cards players have, PLAYS_CARD_PROP holds what cards players have played.
HAS_CARD_PROP=[]
PLAYS_CARD_PROP=[]

# This is just for making the results look pretty :)
LINE="-----------------------------------------------------------------"

# Values below are values that can be dynamically changed, via an example doc.
BRISCOLA_SUIT=briscola_suit
STARTING_HANDS=starting_hands


# New proposition to say the one value is greater than another value or not between 2 values
@proposition(E)
class val_is_greater:

    def __init__(self, val1, val2) -> None:
        assert val1 in CARD_VALUES
        assert val2 in CARD_VALUES
        self.val1 = val1
        self.val2 = val2

    def _prop_name(self):
        return f"{self.val1} > {self.val2}"

# New proposition to say that a card is the current briscola suit or not
@proposition(E)
class card_is_brisc:

    def __init__(self, card, brisc_suit) -> None:
        assert card in CARDS
        assert brisc_suit in CARD_SUITS
        self.card = card
        self.brisc_suit = brisc_suit

    def _prop_name(self):
        return f"'{CARDS[self.card]['suit']}' is apart of '{self.brisc_suit}', the current briscola suit."
    

# New proposition to say that a card is the current suit leading the round of the round or not
@proposition(E)
class card_is_suit_of_round:

    def __init__(self, card, round_suit, trick_num) -> None:
        assert card in CARDS
        assert round_suit in CARD_SUITS
        self.card = card
        self.round_suit = round_suit
        self.trick_num = trick_num

    def _prop_name(self):
        return f"'{self.card}' is apart of '{self.round_suit}', the current round suit of trick #{self.trick_num}."

# New proposition to say that a current suit is the round suit or not
@proposition(E)
class suit_of_round:

    def __init__(self, round_suit, trick_num) -> None:
        assert round_suit in CARD_SUITS
        self.round_suit = round_suit
        self.trick_num = trick_num

    def _prop_name(self):
        return f"'{self.round_suit}', the current round suit of trick #{self.trick_num}."


# New proposition to say that a card is the same suit as another card or not between two cards
@proposition(E)
class card_is_same_suit:

    def __init__(self, card1, card2) -> None:
        assert card1 in CARDS
        assert card2 in CARDS
        self.card1 = card1
        self.card2 = card2

    def _prop_name(self):
        return f"'{self.card1}' is the same suit as '{self.card2}'"
    

# New proposition to say that a card beats another card or not between two cards on a certain trick.
@proposition(E)
class card_beats_card:

    def __init__(self, card1, card2, trick_num) -> None:
        assert card1 in CARDS
        assert card2 in CARDS
        self.card1 = card1
        self.card2 = card2
        self.trick_num = trick_num

    def _prop_name(self):
        return f"'{self.card1}' beats '{self.card2}' on trick #{self.trick_num}"


# New proposition to say that a player has a particular card on a trick.
@proposition(E)
class player_has_card:

    def __init__(self, card, player, trick_num) -> None:
        assert card in CARDS 
        assert player in PLAYERS
        self.card = card
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player} has the card '{self.card}' on trick #{self.trick_num}"
    
# New proposition to say that a player wins a trick, given a round configuration and player.
@proposition(E)
class player_wins_trick:

    def __init__(self, card, player, trick_num) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        assert card in CARDS
        assert player in PLAYERS
        self.card = card
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player}, with their card '{self.card}', wins the trick #{self.trick_num}."
    
# New proposition to say that a player plays a particular card on a particular trick
@proposition(E)
class player_plays_card:

    def __init__(self, card, player, trick_num) -> None:
        assert card in CARDS 
        assert player in PLAYERS
        self.card = card
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player} plays the card '{self.card}' on trick #{self.trick_num}"

# New proposition to say that a particular player is the starting player of a trick
@proposition(E)
class starting_player:

    def __init__(self, player, trick_num) -> None:
        assert player in PLAYERS
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player} is the starting player on trick #{self.trick_num}"

# New proposition to say that the card a player played is the first card played in the round (controls round suits)
@proposition(E)
class starting_player_card:

    def __init__(self, player, card, trick_num) -> None:
        assert card in CARDS
        assert player in PLAYERS
        self.card = card
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player}'s '{self.card}' is the starting card on trick #{self.trick_num}"
    
# New proposition to say that a player draws a particular card on a particular trick
@proposition(E)
class player_draws_card:

    def __init__(self, card, player, trick_num) -> None:
        assert card in CARDS 
        assert player in PLAYERS
        self.card = card
        self.player = player
        self.trick_num = trick_num

    def _prop_name(self):
        return f"{self.player} draws the card '{self.card}' on trick #{self.trick_num}"


# This test theory was a function used to attempt to see some more aspects present in the propositions the model was choosing.
def test_theory1():
    T = example_theory()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())

    S = T.solve()
    # Note: for loop print statements are separated to group together certain propositions, since the ordering of propositions in the solved model is random.
    for k in S:
        if (('round' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('starting player' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('starting card' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('has' in k._prop_name()) and ('#1' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('has' in k._prop_name()) and ('#2' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('plays' in k._prop_name()) and ('#1' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('plays' in k._prop_name()) and ('#2' in k._prop_name())):
            if S[k]:
                print(k)
    print("\n")
    for k in S:
        if (('wins' in k._prop_name())):
            if S[k]:
                print(k)

# This test theory was a function used to attempt to see some more aspects present in the propositions the model was choosing.
# This one in particular had a for loop to loop through several cases (this test_theory was created with an older iterative system in mind)
def test_theory3():
    T = example_theory()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())

    S = T.solve()
    # Note: for loop print statements are separated to group together certain propositions, since the ordering of propositions in the solved model is random.
    for i in range(2):
        for k in S:
            if (('starting card' in k._prop_name() and (f'#{i+1}' in k._prop_name()))):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('round' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('has' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('plays' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('wins' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('draws' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('Swords\' beats' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('Cups\' beats' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('Coins\' beats' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")
        for k in S:
            if (('Clubs\' beats' in k._prop_name()) and (f'#{i+1}' in k._prop_name())):
                if S[k]:
                    print(k)
        print("\n")

    # While debuging the program to try and see which card wins with what cards, I noticed that round suits didn't seem to be winning when they should have been.
    # So this test function was to pass in a a card set to see what will happen if I pass in no Briscola suits and only potnetial round suits.
def test_round_suits():
    test_hand1 = [["A of Cups", "7 of Cups", "2 of Coins"],
                    ["A of Coins","H of Cups","4 of Clubs"],
                    ["3 of Cups","J of Clubs","K of Coins"],
                    ["A of Clubs","3 of Coins","5 of Cups"]]
    test_hand2 = [["A of Cups"],
                    ["4 of Clubs"],
                    ["J of Clubs"],
                    ["5 of Cups"]]
    test_hand3 = [["2 of Coins"],
                    ["4 of Clubs"],
                    ["J of Clubs"],
                    ["A of Clubs"]]
    return test_hand1

# Test case with a smaller pre-defined deck to be able to track what cards are drawn/played.
def test_card_beats_card():
    sample_deck = ['A of Cups', '7 of Cups', '2 of Swords', 'A of Coins','H of Swords',
            '4 of Clubs', 'A of Swords','J of Clubs','K of Coins', 'A of Clubs','3 of Coins','5 of Cups', 
            '7 of Clubs', '4 of Coins', 'H of Clubs', '5 of Coins', 'K of Clubs', 'H of Coins', 'J of Coins', 'K of Swords']
    return sample_deck
    

# Example theory that defines the model's theory for a single trick. 
# Requires a specified trick number, a list of player hands, and a starting player proposition.
def example_theory(trick_number, hands, start_player):

    # Constraint: Say that the first starting player is the first starting player
    E.add_constraint(start_player)
    for player in PLAYERS.keys():
        if player == start_player.player:
            continue
        # Constraint: If a player is not the same as the starting player, they cannot be the starting player of the current trick
        E.add_constraint(~starting_player(player, trick_number))
    
    # Initialize player ownership over starting cards
    hand_i = 0
    for player1 in PLAYERS.keys():
        hand = hands[hand_i]
        for card in hand:
            # Constraint: Each player has the card that they have in their hand
            HAS_CARD_PROP.append(player_has_card(card, player1, trick_number))
            E.add_constraint(player_has_card(card, player1, trick_number))
            for player2 in PLAYERS.keys():
                if player1 == player2:
                    continue
                # Constraint: A second player does not have a card another player already has in their hand
                E.add_constraint(~player_has_card(card, player2, trick_number))
        hand_i += 1

    # Code to intialize base cases for values being greater than other values 
    for i in range (0, len(CARD_VALUES) - 1):
        # Constraint: Base cases for values being greater than each other. 
        E.add_constraint(val_is_greater(CARD_VALUES[i+1], CARD_VALUES[i]))
        # Constraint: Values cannot be greater than themselves.
        E.add_constraint(~val_is_greater(CARD_VALUES[i], CARD_VALUES[i]))
        # Constraint: If a val1 is greater than val2, val2 cannot be greater than val1
        E.add_constraint(val_is_greater(CARD_VALUES[i+1], CARD_VALUES[i]) >> ~val_is_greater(CARD_VALUES[i], CARD_VALUES[i+1]))
    
    # Code to ensure that values being greater follows transitive properties
    for val1 in CARD_VALUES:
        for val2 in CARD_VALUES:
            if val1 == val2:
                continue
            for val3 in CARD_VALUES:
                if val2 == val3 or val1 == val3:
                    continue
                # Constraint: If val2 > val1 and val3 > val2, then val3 must be greater than val1. (Example: 4 > 2 5 > 4 >> 5 > 2)
                E.add_constraint((val_is_greater(val2, val1) & val_is_greater(val3, val2)) >> val_is_greater(val3, val1))

    # Initalizes card suits as Briscola suits or not. (Briscola cards are static throughout the entire game)
    for card in CARDS:
        if CARDS[card]["suit"] == BRISCOLA_SUIT:
            # Constraint: If a card is apart of the suit that is the current Briscola suit, it is a Briscola (or trump) card in our game.
            E.add_constraint((card_is_brisc(card, BRISCOLA_SUIT)))
        else:
            # Constraint: Otherwise, the card is not apart of the current Briscola suit
            E.add_constraint((~card_is_brisc(card, BRISCOLA_SUIT)))
        
    # Initalize all cards with the same suit (this method will automatically make cards suits symmetric as well)
    for card1 in CARDS:
        # Constraint: Cards cannot be the same suit as themselves, as that wouldn't make sense as a solution
        E.add_constraint(~card_is_same_suit(card1, card1))
        for card2 in CARDS:
            if card1 == card2:
                continue
            if CARDS[card1]["suit"] == CARDS[card2]["suit"]:
                # Constraint: If the suits of the cards match, they are the same suit.
                E.add_constraint(card_is_same_suit(card1, card2))
            else:
                # Constraint: Otherwise, they are not the same suit.
                E.add_constraint(~card_is_same_suit(card1, card2))
    
    # Print the trick number
    print(f"Trick #{trick_number}\n")

    # Sets start_card of the round. Checks through the has_card props to find the starting player, and sets that card to the starting card.
    p1_card_prop=[]
    p2_card_prop=[]
    p3_card_prop=[]
    p4_card_prop=[]
    for prop in HAS_CARD_PROP:
        if (prop.player == "P1"):
            p1_card_prop.append(player_plays_card(prop.card, prop.player, trick_number))
        if (prop.player == "P2"):
            p2_card_prop.append(player_plays_card(prop.card, prop.player, trick_number))
        if (prop.player == "P3"):
            p3_card_prop.append(player_plays_card(prop.card, prop.player, trick_number))
        if (prop.player == "P4"):
            p4_card_prop.append(player_plays_card(prop.card, prop.player, trick_number))

        PLAYS_CARD_PROP.append(player_plays_card(prop.card, prop.player, trick_number))
    

    # Constraint(s): Make sure only one card is played from each player
    constraint.add_exactly_one(E, p1_card_prop)
    constraint.add_exactly_one(E, p2_card_prop)
    constraint.add_exactly_one(E, p3_card_prop)
    constraint.add_exactly_one(E, p4_card_prop)

    # Intializes if a card beats a card or not.
    start_card_prop=[]
    for prop in HAS_CARD_PROP:
        start_card = starting_player_card(prop.player, prop.card, trick_number)
        start_card_prop.append(start_card)
        # Constraint: If a player is not the starting player, this implies they cannot have a start card.
        E.add_constraint(~starting_player(prop.player, trick_number) >> ~start_card)
        # Constraint: If card is a starting card, that implies that the card was played.
        E.add_constraint(start_card >> player_plays_card(prop.card, prop.player, trick_number))
        # Constraint: A starting card implies its suit is the round suit of the trick
        E.add_constraint((start_card >> suit_of_round(CARDS[prop.card]["suit"], trick_number)))

    # Constraint: There is only ever one start card of each trick
    constraint.add_exactly_one(E, start_card_prop)

    suit_prop=[]
    for suit in CARD_SUITS:
        suit_prop.append(suit_of_round(suit, trick_number))
    # Constraint: There is only ever one round suit of each trick
    constraint.add_exactly_one(E, suit_prop)

    for card1 in CARDS:
        # Constraint: If the suit of a round is a card's suit, then the card is apart of the suit of the round
        E.add_constraint(suit_of_round(CARDS[card1]["suit"], trick_number) >> (card_is_suit_of_round(card1, CARDS[card1]["suit"], trick_number)))
        # Constraint: If the suit of a round is a not a card's suit, then the card is not apart of the suit of the round
        E.add_constraint(~suit_of_round(CARDS[card1]["suit"], trick_number) >> (~card_is_suit_of_round(card1, CARDS[card1]["suit"], trick_number)))

        for card2 in CARDS:
            if card1 == card2:
                continue
            # Make all the propositions variables (this is just more consise, since this is a long constraint)
            is_b1 = card_is_brisc(card1, BRISCOLA_SUIT)
            is_r1 = card_is_suit_of_round(card1, CARDS[card1]["suit"], trick_number)
            is_b2 = card_is_brisc(card2, BRISCOLA_SUIT)
            is_r2 = card_is_suit_of_round(card2, CARDS[card2]["suit"], trick_number)
            same_suit = card_is_same_suit(card1, card2)
            val_greater = val_is_greater(CARDS[card1]["value"], CARDS[card2]["value"])

            # If either card1 and card2 are the same suit and val1 has a higher value, or if card1 is brisc anc card2 is not, 
            # or if card1 is round and card2 is not and card2 is not a brisc suit, then this statement is true.
            statement = ((same_suit & val_greater) | (is_b1 & ~same_suit) | (is_r1 & ~is_b2 & ~same_suit))
            # Constraint: card1 beats card2 if and only if the statement above is true.
            E.add_constraint(statement >> card_beats_card(card1, card2, trick_number) & (card_beats_card(card1, card2, trick_number) >> statement))
        
    if (trick_number == 1):
        # Remove all starting hand cards from the deck (only on the starting trick)
        for hnds in STARTING_HANDS:
            for card in hnds:
                CARD_DECK.remove(card)
        
    # Check to see who won the trick
    card_win_prop=[]
    for prop1 in PLAYS_CARD_PROP:
        card1 = prop1.card
        for prop2 in PLAYS_CARD_PROP:
            card2 = prop2.card
            if card1 == card2:
                continue
            card_win_prop.append((player_plays_card(card1, prop1.player, trick_number) & player_plays_card(card2, prop2.player, trick_number)) >> card_beats_card(card1, card2, trick_number))
        for player in PLAYERS.keys():
            # NOTE: I had to seperate these constraints to get them to work properly
            # Constaint: If a player doesn't have a card, they can't win the trick with that card
            E.add_constraint((~player_plays_card(card1, player, trick_number)) >> ~player_wins_trick(card1, player, trick_number))
            # Constaint: If a player doesn't have a card, they can't play that card
            E.add_constraint((~player_has_card(card1, player, trick_number)) >> ~player_plays_card(card1, player, trick_number))
            # Constraint: If a player has a card but the card doesn't beat every other card, they don't win the trick that card
            E.add_constraint((~And(card_win_prop) & player_plays_card(card1, player, trick_number)) >> ~player_wins_trick(card1, player, trick_number))
            # Constraint: If a player has a card, it beats other card, and they play the card, they win the trick with that card and become the starting player in the next trick
            E.add_constraint((And(card_win_prop) & player_plays_card(card1, player, trick_number)) >> (player_wins_trick(card1, player, trick_number)))
            # Constraint: If a player wins a trick, they become the starting player in the next trick.
            E.add_constraint(player_wins_trick(card1, player, trick_number) >> starting_player(player, (trick_number + 1)))
        # Reset card propositions for each player
        card_win_prop=[]
    
    #Reset the HAS_CARD_PROP and PLAYS_CARD_PROP
    HAS_CARD_PROP.clear()
    PLAYS_CARD_PROP.clear()
    start_player_prop=[]

    # Code that allows players to draw cards
    for player1 in PLAYERS.keys():
        if len(CARD_DECK) != 0:
            drawn_card = CARD_DECK.pop(0)
            HAS_CARD_PROP.append(player_has_card(drawn_card, player1, (trick_number + 1)))
            # Constraint: Each player has the card that they have in their hand
            E.add_constraint(player_has_card(drawn_card, player1, (trick_number + 1)))
            E.add_constraint(player_draws_card(drawn_card, player1, trick_number))
            for player2 in PLAYERS.keys():
                if player1 == player2:
                    continue
                # Constraint: A second player does not have a card another player already has in their hand
                E.add_constraint(~player_has_card(drawn_card, player2, (trick_number + 1)))
            
        start_player_prop.append(starting_player(player1, (trick_number + 1)))
        
    #Constraint: Ensure that only one new starting player exists
    constraint.add_exactly_one(E, start_player_prop)

    return E

# Function that is called repeatedly to run through several different tricks with different hands and starting players.
def run_trick(t, h, s):
    T = example_theory(t, h, s)
    T = T.compile()

    S = T.solve()
    for k in S:
        if (('starting player' in k._prop_name()) and (f'#{t}' in k._prop_name())):
            if S[k]:
                print(f"- {k}")
    for k in S:
        if (('starting card' in k._prop_name()) and (f'#{t}' in k._prop_name())):
            if S[k]:
                print(f"- {k}")
    print("\n")
    for k in S:
        if (('plays' in k._prop_name()) and (f'#{t}' in k._prop_name())):
            if S[k]:
                print(f"- {k}")
    print("\n")
    for k in S:
        if (('wins' in k._prop_name()) and (f'#{t}' in k._prop_name())):
            if S[k]:
                print(f"- {k}")
    print("\n")
    for k in S:
        if (('draws' in k._prop_name()) and (f'#{t}' in k._prop_name())):
            if S[k]:
                print(f"- {k}")
    print("\n")
    return S

if __name__ == "__main__":
    #STARTING_HANDS = test_round_suits()
    #test_theory3()
    #CARD_DECK = test_card_beats_card()
    hands = STARTING_HANDS
    s_player = starting_player("P1", 1)
    tr = 1
    print(LINE)
    print("Starting Hands:\n")
    hand_i = 0
    for player in PLAYERS:
        print(f"{player}: {hands[hand_i]}")
        hand_i += 1
    print(LINE)
    while (len(hands[0]) != 0):
        T = run_trick(tr, hands, s_player)
        for k in T:
            for hand in hands:
                temp_hand = hand
                for card in temp_hand:
                    if (('plays' in k._prop_name()) and (card in k._prop_name()) and (f'#{tr}' in k._prop_name())):
                        if T[k]:
                            hand.remove(card)
        
            if (('draws' in k._prop_name()) and (f'#{tr}' in k._prop_name())):
                if T[k]:
                    if ('P1' in k._prop_name()):
                        hands[0].append(k.card)
                    if ('P2' in k._prop_name()):
                        hands[1].append(k.card)
                    if ('P3' in k._prop_name()):
                        hands[2].append(k.card)
                    if ('P4' in k._prop_name()):
                        hands[3].append(k.card)
            if (('wins' in k._prop_name()) and (f'#{tr}' in k._prop_name())):
                if T[k]:
                    if ('P1' in k._prop_name()):
                        PLAYERS['P1'] += 1
                    if ('P2' in k._prop_name()):
                        PLAYERS['P2'] += 1
                    if ('P3' in k._prop_name()):
                        PLAYERS['P3'] += 1
                    if ('P4' in k._prop_name()):
                        PLAYERS['P4'] += 1
            if (('starting player' in k._prop_name()) and (f'#{(tr + 1)}' in k._prop_name())):
                if T[k]:
                    if ('P1' in k._prop_name()):
                        s_player = starting_player("P1", (tr + 1))
                    if ('P2' in k._prop_name()):
                        s_player = starting_player("P2", (tr + 1))
                    if ('P3' in k._prop_name()):
                        s_player = starting_player("P3", (tr + 1))
                    if ('P4' in k._prop_name()):
                        s_player = starting_player("P4", (tr + 1))
        tr += 1
        print(LINE)
        if (len(hands[0]) != 0):
            print(f"Current Hands after Trick #{tr - 1}\n")
            hand_i = 0
            for player in PLAYERS:
                print(f"{player}: {hands[hand_i]}")
                hand_i += 1
            print(LINE)
        else:
            print ("Players are out of cards, so the game is over.")
            print(LINE)

    print("Final Results:")
    for player in PLAYERS:
        print(f"{player} wins: {PLAYERS[player]}")
    
    highest_wins = 0
    for player1 in PLAYERS:
        for player2 in PLAYERS:
            if player1 == player2:
                continue
            if ((PLAYERS[player1] >= PLAYERS[player2]) and (PLAYERS[player1] > highest_wins)):
                highest_wins = PLAYERS[player1]
            elif (PLAYERS[player1] < PLAYERS[player2] and (PLAYERS[player2] > highest_wins)):
                highest_wins = PLAYERS[player2]
    
    winners = []
    for player in PLAYERS:
        if PLAYERS[player] == highest_wins:
            winners.append(player)
    
    if len(winners) == 1:
        print(f"\nThe winner of this game is {winners[0]}!")
    else:
        # Multiple winners
        print("\nTheres a tie! Between the players:")
        for winner in winners:
            print(winner)

