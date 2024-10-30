import pprint


from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()


PLAYER_NUMBER={'P1':0,'P2':0,'P3':0,'P4':0}

CARD_SUITS=['Swords', 'Cups', 'Clubs' 'Coins']

CARD_VALUES=['2','4','5','6','7','J','H','K','3','A']
VALUES=list(range(0,10))

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
        self.val2 = brisc_suit

    def _prop_name(self):
        return f"{self.card['suit']} is apart of {self.val2}, the current briscola suit."

# New proposition to say that a card is the same suit as another card or not between two cards
class card_is_same_suit:

    def __init__(self, card1, card2) -> None:
        assert card1 in CARDS
        assert card2 in CARDS
        self.card1 = card1
        self.card2 = card2

    def _prop_name(self):
        return f"{self.card1} is the same suit as {self.card2}"
    

# New proposition to say that a card beats another card or not between two cards
class card_beats_card:

    def __init__(self, card1, card2) -> None:
        assert card1 in CARD_VALUES
        assert card2 in CARD_VALUES
        self.val1 = card1
        self.val2 = card2

    def _prop_name(self):
        return f"{self.card1} beats {self.card2}"
    
# New proposition to say that a player wins a trick, given a round configuration and player.
class player_wins_trick:

    def __init__(self, cards_in_play, player) -> None:
        #TODO: Add a for loop here to check each card in the array (for now I'm just asserting that the cards exist as a placeholder)
        assert cards_in_play in CARDS 
        assert player in PLAYER_NUMBER
        self.cards_in_play = cards_in_play
        self.player = player

    def _prop_name(self):
        return f"{self.player} wins the trick of configuration {self.cards_in_play}"

# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():

    #TODO: Address equal cases (What is Sword 2 = Coin 2 somehow)

    # Initalizes the first few values
    value_propositions=[]
    # Base Constraint: Each value in CARD_VALUES is greater than the value preceeding it.
    for i in range (0, len(CARD_VALUES) - 1):
        # For every index except the final index, say the value at i+1 is greater than the value at i+1.
        value_propositions.append(val_is_greater(CARD_VALUES[i+1], CARD_VALUES[i]))
    
    #TODO: Find out why the constaints won't work
    """ for val1 in CARD_VALUES:
        for val2 in CARD_VALUES:
            if val1 == val2:
                print("lmao")
                continue
            for val3 in CARD_VALUES:
                if val2 == val3 or val1 == val3:
                    print("lol")
                    continue
                # Example: 4 > 2 5 > 4 >> 5 > 2
                print("work dammit")
                E.add_constraint((val_is_greater(val2, val1) & val_is_greater(val3, val2)) >> val_is_greater(val3, val1))
    """

    for val in value_propositions:
        print(val._prop_name())

    # Initalize all cards with the same suit (this method will automatically make cards suits symmetric as well)
    same_suit_propositions=[]
    for card1 in CARDS:
        for card2 in CARDS:
            if card1 == card2:
                continue
            if CARDS[card1]["suit"] == CARDS[card2]["suit"]:
                same_suit_propositions.append(card_is_same_suit(card1, card2))

    for val in same_suit_propositions:
        print(val._prop_name())

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
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
