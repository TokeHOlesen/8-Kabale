import pygame


class Card(pygame.sprite.Sprite):
    """Instantiates a card with a suit and rank"""
    def __init__(self, rank, suit, surface, xy_pos=(0, 0)):
        super().__init__()
        self.rank = rank
        self.suit = suit
        self.rank_string = {  # Used to find the correct image file name
            1: "A_",
            2: "2_",
            3: "3_",
            4: "4_",
            5: "5_",
            6: "6_",
            7: "7_",
            8: "8_",
            9: "9_",
            10: "10_",
            11: "J_",
            12: "Q_",
            13: "K_"
        }
        self.back_img = pygame.image.load("Assets/Graphics/card_back.png").convert_alpha()  # Back of card image
        # Loads the image file depending on the card's suit and rank.
        # "Foundation" is a special suit for an invisible card put on top of an empty column that a King can attach to
        if not suit == "Foundation":
            self.card_img_path = f"./Assets/Graphics/Cards/{self.rank_string[rank]}{suit.lower()}.png"
            self.card_img = pygame.image.load(self.card_img_path).convert_alpha()
            self.card_img = pygame.transform.scale(self.card_img, (127, 177))
        else:
            self.card_img = self.back_img
        self.rect = self.card_img.get_rect()
        self.rect.x, self.rect.y = xy_pos
        self.surface = surface
        self.is_facing_up = 0  # Sets the visible side of the card
        self.card_sides = [self.back_img, self.card_img]

    def face_up(self):
        """Flips the card up"""
        self.is_facing_up = 1

    def face_down(self):
        """Flips the card down"""
        self.is_facing_up = 0

    def flip(self):
        """Flips the card to the other side"""
        self.is_facing_up = not self.is_facing_up

    def is_within_bounds(self, coords):
        """Checks if the passed coords are within the bounds of the card sprite"""
        if (self.rect.right > coords[0] > self.rect.left
                and self.rect.bottom > coords[1] > self.rect.top):
            return True
        return False

    def display_card(self):
        """Displays the card"""
        self.surface.blit(self.card_sides[self.is_facing_up], self.rect)

    def update(self):
        if not self.suit == "Foundation":
            self.display_card()
