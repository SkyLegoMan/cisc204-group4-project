import pprint


from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"
from utils import display_solution

# Encoding that will store all of your constraints
E = Encoding()


PLAYER_NUMBER={'P1':0,'P2':0,'P3':0,'P4':0}

CARD_SUITS=['Swords', 'Cups', 'Clubs' 'Coins']

CARD_VALUES=['2','4','5','6','7','J','H','K','3','A']

TRICK_NUMBER=0

BRISCOLA_SUIT='Swords' 

# This is a fixed configuration of cards, for the sake of testing for now (CARDS would later feature every card in the deck, which will be created with a for loop)
CARDS={"7 of Cups" : {"suit" : 'Cups', "value" : '7'}, 
       "Horseman of Swords" : {"suit" : 'Swords', "value" : 'H'},
       "Jack of Clubs" : {"suit" : 'Clubs', "value" : 'J'},
        "3 of Coins" : {"suit" : 'Coins', "value" : '3'},
        "3 of Cups" : {"suit" : 'Cups', "value" : '3'} }

CARDS_IN_PLAY=["7 of Cups", "Horseman of Swords", "Jack of Clubs", "3 of Coins"]

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
    
# New proposition to say that a player wins a trick, given a round configuration and player.
@proposition(E)
class player_wins_trick:

    def __init__(self, cards_in_play, player) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        assert cards_in_play in CARDS 
        assert player in PLAYER_NUMBER
        self.cards_in_play = cards_in_play
        self.player = player

    def _prop_name(self):
        return f"{self.player} wins the trick of configuration {self.cards_in_play}"


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():

    #TODO: Address equal cases (What is Sword 2 = Coin 2 somehow)
    
    for i in range (0, len(CARD_VALUES) - 1):
        # For every index except the final index, say the value at i+1 is greater than the value at i+1.
        #value_propositions.append(val_is_greater(CARD_VALUES[i+1], CARD_VALUES[i]))
        E.add_constraint(val_is_greater(CARD_VALUES[i+1], CARD_VALUES[i]))
    
    
    # Code to ensure that values being greater follows transitive properties
    for val1 in CARD_VALUES:
        for val2 in CARD_VALUES:
            if val1 == val2:
                continue
            for val3 in CARD_VALUES:
                if val2 == val3 or val1 == val3:
                    continue
                # Example: 4 > 2 5 > 4 >> 5 > 2
                E.add_constraint((val_is_greater(val2, val1) & val_is_greater(val3, val2)) >> val_is_greater(val3, val1))
    
    # Initalizes card suits as Briscola suits or not. (also ensures that every card is unique)
    for card in CARDS:
        # There is exactly one of each card.
        constraint.add_exactly_one(E, card)
        if CARDS[card]["suit"] == BRISCOLA_SUIT:
            # If a card is apart of the suit that is the current Briscola suit, it is a Briscola (or trump) card
            E.add_constraint((card_is_brisc(card, BRISCOLA_SUIT)))

    
    # Initalize all cards with the same suit (this method will automatically make cards suits symmetric as well)
    for card1 in CARDS:
        # Constraint: Cards cannot be the same suit as themselves, as that wouldn't make sense
        E.add_constraint(~card_is_same_suit(card1, card1))
        for card2 in CARDS:
            if card1 == card2:
                continue
            if CARDS[card1]["suit"] == CARDS[card2]["suit"]:
                # If the suits of the cards match, they are the same suit.
                E.add_constraint(card_is_same_suit(card1, card2))
            else:
                # Otherwise, they are not the same suit.
                E.add_constraint(~card_is_same_suit(card1, card2))



    
    # Intializes if a card beats a card or not.
    for card1 in CARDS:
        for card2 in CARDS:
            # Make all the propositions variables (this is just more consise, since this is a long constraint)
            is_b = card_is_brisc(card1, BRISCOLA_SUIT)
            same_suit = card_is_same_suit(card1, card2)
            val_greater = val_is_greater(CARDS[card1]["value"], CARDS[card2]["value"])
            # card1 beats card2 either if card1 is brisc and card2 is not, or if both are the same suit and card1 has a higher value.
            E.add_constraint(((is_b & (~same_suit | (same_suit & val_greater)))) >> card_beats_card(card1, card2))
            # Constaint below should make sense, but the code ends up not returning any solutions if its present.
            # E.add_constraint(card_beats_card(card1, card2) >> ~card_beats_card(card2, card1))

    
    #TODO: Need to consider what happens if cards are of differing suits that aren't Briscola suit. Need to figure out how to say that they cannot beat eachother all the time.

    #TODO: Add in code for player_wins_trick

    


    print(E.constraints)
    


    # Add custom constraints by creating formulas with the variables you created. 
    #E.add_constraint((a | b) & ~x)
    # Implication
    #E.add_constraint(y >> z)
    ## Negate a formula
    #E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    #constraint.add_exactly_one(E, a, b, c)

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
    display_solution(S)
    #print("\nVariable likelihoods:")
    #for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
    #    print(" %s: %.2f" % (vn, likelihood(T, v)))
    #print()
