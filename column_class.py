import pygame


class ColumnOfCards:
    def __init__(self, x_y_pos=(0, 0)):
        self.cards = []  # A list of Card objects in this column
        self.x_pos, self.y_pos = x_y_pos  # The position of the topmost card in this column
        self.card_offset = 50           # How many pixels between cards in y axis
        self.default_card_offset = 50  # Uses this value unless there's too many cards to fit on screen
        self.card_height = 177
        self.screen_height = 1024

    def clear(self):
        """Removes all cards from the column"""
        self.cards.clear()

    def add_card(self, card):
        """Adds a card to this column and updates its screen coords"""
        # Shifs the cards up by one if the uppermost card is the invisible "Foundation" (a temp anchor for a King)
        if not self.is_empty() and self.cards[0].suit == "Foundation":
            shift = -1
        else:
            shift = 0
        card.rect.x = self.x_pos
        card.rect.y = self.y_pos + (len(self.cards) + shift) * self.card_offset
        self.cards.append(card)

    def get_number_of_cards(self):
        """Returns the number of cards in the column"""
        if self.cards[0].suit == "Foundation":
            return len(self.cards) - 1
        return len(self.cards)

    def cards_can_fit_on_screen(self):
        """Returns true if the column can be displayed on the screen with the defauly y distance"""
        if self.y_pos + (
                self.get_number_of_cards() - 1) * self.default_card_offset + self.card_height > self.screen_height:
            return False
        return True

    def set_offset(self):
        """Sets the distance between cards in the y axis so the entire column can fit on the screen"""
        if self.cards_can_fit_on_screen():
            for i, card in enumerate(self.cards):
                card.rect.y = self.y_pos + (i * self.default_card_offset)
        else:
            self.card_offset = self.default_card_offset
            while self.y_pos + (
                    self.get_number_of_cards() - 1) * self.card_offset + self.card_height > self.screen_height:
                self.card_offset -= 1
            for i, card in enumerate(self.cards):
                card.rect.y = self.y_pos + i * self.card_offset

    def get_clicked_card_index(self):
        """Returns the index of the clicked card in self.cards[]"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < self.x_pos or mouse_x > self.x_pos + 127:
            return None
        for c, card in enumerate(self.cards):
            if c == len(self.cards) - 1:
                if card.rect.y <= mouse_y < card.rect.y + 177:
                    return c
            elif card.rect.y <= mouse_y < card.rect.y + self.card_offset:
                return c
        return None

    def get_clicked_card_position(self):
        """Returns the (x, y) coords of the top left corner of the clicked card"""
        index = self.get_clicked_card_index()
        return self.cards[index].rect.x, self.cards[index].rect.y

    def get_clicked_card(self):
        """Returns the clicked card object"""
        return self.cards[self.get_clicked_card_index()]

    def get_first_card(self):
        """Returns the top card in the column"""
        return self.cards[0]

    def get_last_card(self):
        """Returns the bottom card in the column"""
        return self.cards[-1]

    def is_empty(self):
        """Returns True if there are no cards in the column"""
        if len(self.cards) > 0:
            return False
        return True

    def move_cards(self, start_index, target):
        """Moves the cards from start_index on to another column or a base"""
        for card in self.cards[start_index:]:
            target.add_card(card)
        del self.cards[start_index:]

    def update_cards(self):
        """Adjusts y-offset if necessary and draws the cards"""
        self.set_offset()
        for card in self.cards:
            card.update()


class ColumnOfDraggedCards(ColumnOfCards):
    """A temporary column that holds the cards as they are being dragged across the screen"""
    def __init__(self):
        super().__init__()
        self.x_offset = 0  # Difference between mouse x pos and top left corner of the card x pos
        self.y_offset = 0  # Difference between mouse y pos and top left corner of the card y pos
        self.is_being_dragged = False  # True if the column is currently being dragged
        self.source_column = 0  # The column from which the cards in this columns originated

    def set_new_pos(self, xy_pos):
        """Updates the column's position"""
        self.x_pos, self.y_pos = xy_pos

    def set_mouse_offset(self, card_xy, mouse_xy):
        """Calculates the difference between the top left corner of the clicked card and the mouse position"""
        clicked_card_x, clicked_card_y = card_xy
        mouse_pos_x, mouse_pos_y = mouse_xy
        self.x_offset, self.y_offset = clicked_card_x - mouse_pos_x, clicked_card_y - mouse_pos_y

    def add_card(self, card):
        """Adds a card"""
        self.cards.append(card)

    def update_pos(self):
        """Updates the card's on screen position relative to the mouse cursor"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x_pos = mouse_x + self.x_offset
        self.y_pos = mouse_y + self.y_offset
        for i, card in enumerate(self.cards):
            card.rect.x = self.x_pos
            card.rect.y = self.y_pos + i * self.card_offset

    def update_cards(self):
        """Draws the cards"""
        for card in self.cards:
            if self.is_being_dragged:
                self.update_pos()
            card.update()
