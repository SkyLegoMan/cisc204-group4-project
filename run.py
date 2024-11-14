import pprint

from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
from utils import display_solution
from example import briscola_suit, round_suit, cards_in_play

# Encoding that will store all of your constraints
E = Encoding()


PLAYERS={'P1':0,'P2':0,'P3':0,'P4':0}

TRICK_NUMBER=0

# This is a fixed configuration of cards, for the sake of testing for now (CARDS would later feature every card in the deck, which will be created with a for loop)

CARD_SUITS=['Swords', 'Cups', 'Clubs', 'Coins']

CARD_VALUES=['2','4','5','6','7','J','H','K','3','A']

CARDS = {}

for s in CARD_SUITS:
    for v in CARD_VALUES:
        key_card = v + " of " + s
        CARDS[key_card] = {"suit" : s, "value" : v}

# Values below are values that can be dynamically changed, via an example doc.
BRISCOLA_SUIT=briscola_suit
ROUND_SUIT=round_suit
# Card order is based off of order in the list.
CARDS_IN_PLAY=cards_in_play

#CARD_TO_WIN=card_to_win
#PLAYER_TO_WIN=player_to_win

#TODO: Create a for loop that will create the card deck sequentially


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
        return f"{CARDS[self.card]['suit']} is apart of {self.brisc_suit}, the current briscola suit."
    

# New proposition to say that a card is the current suit leading the round of the round or not
@proposition(E)
class card_is_suit_of_round:

    def __init__(self, card, round_suit) -> None:
        assert card in CARDS
        assert round_suit in CARD_SUITS
        self.card = card
        self.round_suit = round_suit

    def _prop_name(self):
        return f"{CARDS[self.card]['suit']} is apart of {self.round_suit}, the current suit of the round."


# New proposition to say that a card is the same suit as another card or not between two cards
@proposition(E)
class card_is_same_suit:

    def __init__(self, card1, card2) -> None:
        assert card1 in CARDS
        assert card2 in CARDS
        self.card1 = card1
        self.card2 = card2

    def _prop_name(self):
        return f"{self.card1} is the same suit as {self.card2}"
    

# New proposition to say that a card beats another card or not between two cards
@proposition(E)
class card_beats_card:

    def __init__(self, card1, card2) -> None:
        assert card1 in CARDS
        assert card2 in CARDS
        self.card1 = card1
        self.card2 = card2

    def _prop_name(self):
        return f"{self.card1} beats {self.card2}"

# New proposition to say that a player owns a particular card.
@proposition(E)
class player_owns_card:

    def __init__(self, card, player) -> None:
        assert card in CARDS 
        assert player in PLAYERS
        self.card = card
        self.player = player

    def _prop_name(self):
        return f"{self.player} owns the card {self.card}"
    

# New proposition to say that a card is apart of a round
@proposition(E)
class card_in_round:

    def __init__(self, card, card_in_play) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        assert card in CARDS 
        for i in card_in_play:
            assert i in CARDS.keys()
        self.card = card
        self.card_in_play = card_in_play

    def _prop_name(self):
        return f"{self.card} is apart of the current round"
    
# New proposition to say that a trick has ended
@proposition(E)
class trick_ended:

    def __init__(self, trick_num) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        self.trick_num = trick_num

    def _prop_name(self):
        return f"Trick #{self.trick_num} has ended"


# New proposition to say that a player wins a trick, given a round configuration and player.
@proposition(E)
class player_wins_trick:

    def __init__(self, cards_in_play, card, player) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        for i in cards_in_play:
            assert i in CARDS.keys()
        assert card in CARDS
        assert player in PLAYERS
        self.cards_in_play = cards_in_play
        self.card = card
        self.player = player

    def _prop_name(self):
        return f"{self.player} wins the trick of configuration {self.cards_in_play} with their card {self.card}"


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():


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

    # Initalizes card suits as Briscola suits or not.
    for card in CARDS:
        if CARDS[card]["suit"] == BRISCOLA_SUIT:
            # Constraint: If a card is apart of the suit that is the current Briscola suit, it is a Briscola (or trump) card in our game.
            E.add_constraint((card_is_brisc(card, BRISCOLA_SUIT)))
        else:
            # Constraint: Otherwise, the card is not apart of the current Briscola suit
            E.add_constraint((~card_is_brisc(card, BRISCOLA_SUIT)))
        
        #TODO: Make the round suits dynamic
        # Initalizes card suits as round suits or not (this code may need to be tweaked later for more dynamic round suits)
        if CARDS[card]["suit"] == ROUND_SUIT:
            # Constraint: If a card is apart of the suit that is the current round suit, it is a round suit card in our round.
            E.add_constraint((card_is_suit_of_round(card, ROUND_SUIT)))
        else:
            # Constraint: Otherwise, the card is not apart of the current round suit
            E.add_constraint((~card_is_suit_of_round(card, ROUND_SUIT)))
    


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


    # Intializes if a card beats a card or not.
    for card1 in CARDS:
        for card2 in CARDS:
            if card1 == card2:
                continue
            # Make all the propositions variables (this is just more consise, since this is a long constraint)
            is_b1 = card_is_brisc(card1, BRISCOLA_SUIT)
            is_r1 = card_is_suit_of_round(card1, ROUND_SUIT)
            is_b2 = card_is_brisc(card2, BRISCOLA_SUIT)
            is_r2 = card_is_suit_of_round(card2, ROUND_SUIT)
            same_suit = card_is_same_suit(card1, card2)
            val_greater = val_is_greater(CARDS[card1]["value"], CARDS[card2]["value"])
            
            # Constraint: If either card1 and card2 are the same suit and val1 has a higher value, or if card1 is brisc anc card2 is not, or if card1 is round and card2 is not and card2 is not a brisc suit, .
            E.add_constraint(((same_suit & val_greater) | (is_b1 & ~same_suit) | (is_r1 & ~is_b2 & ~same_suit)) >> card_beats_card(card1, card2))
            # Constraint: If a card1 beats card2, card2 does not beat card1.
            E.add_constraint(card_beats_card(card1, card2) >> ~card_beats_card(card2, card1))
            # Constraint: If neither card1 nor card2 are brisc, neither are the round suit, and card1 and card2 are not the same suit, card1 does not beat card2 and card2 does not beat card1.
            E.add_constraint((~is_b1 & ~is_b2 & ~is_r1 & ~is_r2 & ~same_suit) >> (~card_beats_card(card1, card2) & ~card_beats_card(card2, card1)))

    
    # Set players to own cards and set what cards are in the round
    
    card_i = 0
    for player1 in PLAYERS.keys():
        E.add_constraint(player_owns_card(CARDS_IN_PLAY[card_i], player1))
        E.add_constraint(player_owns_card(CARDS_IN_PLAY[card_i], player1) >> card_in_round(CARDS_IN_PLAY[card_i], CARDS_IN_PLAY))
        for player2 in PLAYERS.keys():
            if player1 == player2:
                continue
            E.add_constraint(~player_owns_card(CARDS_IN_PLAY[card_i], player2))
        card_i += 1

    #TODO: Create constraints to say if a player should win a given round or not.
    card_win_prop=[]
    for card1 in CARDS_IN_PLAY:
        for card2 in CARDS_IN_PLAY:
            if card1 == card2:
                continue
            card_win_prop.append(card_beats_card(card1, card2))
        for player in PLAYERS:
            E.add_constraint((~player_owns_card(card1, player)) >> ~player_wins_trick(CARDS_IN_PLAY, card1, player))
            E.add_constraint((And(card_win_prop) & player_owns_card(card1, player)) >> player_wins_trick(CARDS_IN_PLAY, card1, player))
            E.add_constraint((~And(card_win_prop) & player_owns_card(card1, player)) >> ~player_wins_trick(CARDS_IN_PLAY, card1, player))
        # Reset card propositions for each player
        card_win_prop=[]
            

    print(E.constraints)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    #print("# Solutions: %d" % count_solutions(T))
    #print("   Solution: %s" % T.solve())
    S = T.solve()
    
    for k in S:
        if ('wins' in k._prop_name()):
            if S[k]:
                print(k)
    
    #display_solution(S)
    
    #print("\nVariable likelihoods:")
    #for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
    #    print(" %s: %.2f" % (vn, likelihood(T, v)))
    #print()
