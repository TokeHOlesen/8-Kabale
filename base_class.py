import pygame


class CardBase(pygame.sprite.Sprite):
    """Starts up empty and accepts cards from Ace and up"""
    def __init__(self,
                 surface,  # The surface the card pile will be drawn on
                 position,  # X, Y coords of the base
                 suit):  # This base will only accept cards of this suit
        super().__init__()
        self.surface = surface
        self.base_img = pygame.image.load(f"./Assets/Graphics/base_{suit}.png").convert_alpha()  # Base image
        self.rect = self.base_img.get_rect()
        self.rect.x, self.rect.y = position
        self.suit = suit
        self.cards = []  # Holds the cards moved to this base

    def clear(self):
        """Removes all cards from this base"""
        self.cards.clear()

    def add_card(self, card):
        """Adds a card and updates its position on the screen"""
        card.rect.x = self.rect.x
        card.rect.y = self.rect.y
        self.cards.append(card)

    def get_current_rank(self):
        """Returns the rank of the card currently on top of the base"""
        if not self.is_empty():
            return self.cards[-1].rank
        else:
            return 0

    def get_number_of_cards(self):
        """Returns the number of cards on this base"""
        return len(self.cards)

    def is_empty(self):
        """Returns True if there are no cards in this base"""
        if self.cards:
            return False
        return True

    def display(self):
        """Draws the top card in this base; if empty, draws the base image"""
        if not self.cards:
            self.surface.blit(self.base_img, self.rect)
        else:
            self.cards[-1].display_card()

    def update(self):
        self.display()
