from random import shuffle
from card_class import *


# Defines a deck, at the base of which is a list of Card objects.
class DeckOfCards:
    def __init__(self, surface):
        self.__suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
        self.__ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.card_pile = []  # Cards that have not yet been drawn
        self.discard_pile = []  # Cards that have been drawn and won't be available again until deck is reshuffled
        self.surface = surface

        # Adds one of each card to the deck
        for suit in self.__suits:
            for rank in self.__ranks:
                self.card_pile.append(Card(rank, suit, self.surface))

    def shuffle(self):
        """Shuffles the deck and puts used cards back into play"""
        self.card_pile += self.discard_pile
        self.discard_pile = []
        shuffle(self.card_pile)

    def draw_card(self):
        """Draws a card"""
        drawn_card = self.card_pile[0]
        self.card_pile.remove(drawn_card)
        self.discard_pile.append(drawn_card)
        return drawn_card

    def no_of_playable_cards(self):
        """Returns the number of card that are still in the deck"""
        return len(self.card_pile)

    def no_of_discarded_cards(self):
        """Returns the number of cards that have already been drawn from the deck"""
        return len(self.discard_pile)
