from deck_class import *
from column_class import *
from base_class import *
from double_click_class import *
from button_class import *
from graphics import *
from sys import exit


class Game:
    def __init__(self):
        self.deck = DeckOfCards(game_window)
        self.state = "Game"
        self.undo_stack = []  # A record of previous moves
        # Variables to keep track of the x position of the clicked card to make sure undo actions are recorded correctly
        # Since cards can't change position in the y axis, only records an undo action if the clicked card has changed
        # its x position after the player has let go of it. In other words, an action can only be undone if the moved
        # card's position at mousebuttondown and mousebutton up is not the same
        self.clicked_card = Card
        self.clicked_card_start_pos = 0
        self.clicked_card_end_pos = 0

        # Holds 8 ColumnOfCards objects
        self.columns = []
        for i in range(8):
            self.columns.append(ColumnOfCards((172 + i * 150, 20)))

        # Holds cards that are currently being dragged across the screen
        self.dragged_column = ColumnOfDraggedCards()

        # Creates a list of CardPile objects to serve as bases (aces and up)
        self.bases = [
            CardBase(game_window, (20, 20), "Spades"),
            CardBase(game_window, (20, 220), "Hearts"),
            CardBase(game_window, (20, 420), "Clubs"),
            CardBase(game_window, (20, 620), "Diamonds")
        ]

        # Buttons that are always visible in the lower left corner of the screen during gameplay
        self.on_screen_buttons = [
            Button(game_window, self.undo_last_move, (20, 820), 127, 54, "FORTRYD", font_size=24,
                   border_width=3, y_offset=16),
            Button(game_window, self.help, (20, 885), 127, 54, "HJÆLP", font_size=24,
                   border_width=3, y_offset=16),
            Button(game_window, self.really_quit, (20, 950), 127, 54, "AFSLUT", font_size=24,
                   border_width=3, y_offset=16)
        ]

        # Buttons shown in the "Hjælp" dialog window if the game is still playable
        self.ok_buttons = [
            Button(game_window, self.back_to_game, (560, 560), 250, 80, "OK", font_size=60, y_offset=14)
        ]

        # Buttons shown in the "Hjælp" dialog window when there are no valid moves left
        self.play_again_or_back_buttons = [
            Button(game_window, self.back_to_game, (420, 550), 220, 80, "TILBAGE", font_size=45, y_offset=20),
            Button(game_window, self.play_again, (710, 550), 240, 80, "SPIL IGEN", font_size=45, y_offset=20)
        ]

        # Buttons shown in the "Afslut" dialog window
        self.quit_buttons = [
            Button(game_window, self.back_to_game, (440, 550), 220, 80, "TILBAGE", font_size=45, y_offset=20),
            Button(game_window, self.quit_game, (710, 550), 220, 80, "AFSLUT", font_size=45, y_offset=20)
        ]

        # Buttons shown in the "Victory" dialog window
        self.play_again_or_quit_buttons = [
            Button(game_window, self.play_again, (420, 550), 240, 80, "SPIL IGEN", font_size=45, y_offset=20),
            Button(game_window, self.quit_game, (710, 550), 240, 80, "AFSLUT", font_size=45, y_offset=20)
        ]

        # Creates an object of the DoubleClick class to keep track of double clicks
        self.double_click = DoubleClick()

    # Buttons functions - called by objects of the Button class
    def help(self):
        if self.legal_moves_remain():
            self.state = "Help (Playable)"
        else:
            self.state = "Help (Unplayable)"

    @staticmethod
    def quit_game():
        pygame.quit()
        exit()

    def really_quit(self):
        self.state = "Really quit?"

    def back_to_game(self):
        self.state = "Game"

    def play_again(self):
        self.deal_cards()
        self.state = "Game"

    def deal_cards(self):
        """Resets the board and populates columns with cards"""
        self.undo_stack = []
        self.deck.shuffle()

        for column in self.columns:
            column.clear()
        self.dragged_column.clear()
        for base in self.bases:
            base.clear()

        # Puts 4 cards face down in the first 4 columns and 4 cards face up in the other 4
        for i, column in enumerate(self.columns):
            for _ in range(4):
                new_card = self.deck.draw_card()
                if i >= 4:
                    new_card.face_up()
                else:
                    new_card.face_down()
                column.add_card(new_card)

        # Puts two cards face up in every column
        for column in self.columns:
            for _ in range(2):
                new_card = self.deck.draw_card()
                new_card.face_up()
                column.add_card(new_card)

        # Puts one card face up in each of the first 4 columns
        for i in range(4):
            new_card = self.deck.draw_card()
            new_card.face_up()
            self.columns[i].add_card(new_card)

    def legal_moves_remain(self):
        """Checks if there are any legal moves left; if not, returns False, and the game is lost"""
        for this_column in self.columns:
            bottom_card = this_column.get_last_card()
            for checked_column in self.columns:
                for checked_card in checked_column.cards:
                    # Excludes matches if the card is in the same column
                    if (not checked_column == this_column
                            # Checks if the suits are the same, or the suit is "Foundation" (which accepts any king) and
                            # the card is a king AND the king is not at the top of the column (which would make it
                            # possible to move it back and forth infinitely)
                            and (checked_card.suit == bottom_card.suit
                                 or ((this_column.get_last_card().suit == "Foundation" and checked_card.rank == 13)
                                     and not checked_column.get_first_card() == checked_card))
                            # Checks if the card's rank allows it to be placed on top of another
                            and checked_card.rank + 1 == bottom_card.rank
                            # Checks if the card is not turned upside down (i.e. not in play yet)
                            and not checked_card.is_facing_up == 0):
                        return True
            # Checks if a card showing averse can be flipped to be put into play
            if (this_column.get_last_card().is_facing_up == 0
                    and not this_column.get_last_card().suit == "Foundation"):
                return True
            # Checks if the card can be moved to any of the bases
            for this_base in self.bases:
                if bottom_card.suit == this_base.suit and bottom_card.rank == this_base.get_current_rank() + 1:
                    return True
        return False

    def is_victorious(self):
        """Checks victory conditions"""
        for base in self.bases:
            if base.get_number_of_cards() < 13:
                return False
        return True

    def set_undo_button_status(self):
        """Greys out the Undo button if the undo stack is empty"""
        if self.undo_stack:
            self.on_screen_buttons[0].active = True
        else:
            self.on_screen_buttons[0].active = False

    def draw_playing_field(self, buttons_active=True):
        """Draws all the cards and on-screen buttons"""
        for base in self.bases:
            base.update()
        for column in self.columns:
            column.update_cards()
        self.dragged_column.update_cards()
        for button in self.on_screen_buttons:
            button.draw(buttons_active)

    @staticmethod
    def draw_message_window():
        """Draws a message box in the middle of the screen"""
        game_window.blit(msg_window_img, (game_window.get_width() // 2 - msg_window_img.get_width() // 2,
                                          game_window.get_height() // 2 - msg_window_img.get_height() // 2))

    def undo_last_move(self):
        """Undoes the last move"""
        if self.undo_stack:
            # Reads data from the top of the undo stack and deletes it
            undo_data = self.undo_stack.pop()
            # Checks type: moves between columns are saved as a tuple, flipping a card as int
            if type(undo_data) is tuple:
                source, index, target = undo_data
                # Moves cards from a column or base to another column or base, from the given index down
                for card in source.cards[index:]:
                    target.add_card(card)
                del source.cards[index:]
            elif type(undo_data) is int:
                index = undo_data
                # Unflips the bottom card in the column with the given index
                self.columns[index].get_last_card().flip()

    def show_message_box(self, events, button_group, text_1, y_pos_1, text_2, y_pos_2):
        """Game state: displays a window containing a message and buttons"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_group:
                    button.run_command()

        self.draw_playing_field(buttons_active=False)
        self.draw_message_window()

        game_window.blit(text_1, ((game_window.get_width() - text_1.get_width()) // 2, y_pos_1))
        game_window.blit(text_2, ((game_window.get_width() - text_2.get_width()) // 2, y_pos_2))

        for button in button_group:
            button.draw()

    def gameplay(self, events):
        """Game state: the actual game where cards are moved"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Moves the clicked card(s) to the the temporary dragged_column
                for i, column in enumerate(self.columns):
                    # Evaluates if a card has been clicked and if the card is facing up (and thus can be moved)
                    if column.get_clicked_card_index() is not None and column.get_clicked_card().is_facing_up:
                        # Records the clicked card - if by MOUSEBUTTONUP the card hasn't changed position,
                        # undo data will not be recorded
                        self.clicked_card = column.get_clicked_card()
                        # Records the clicked card's position at mousebuttondown
                        self.clicked_card_start_pos = self.clicked_card.rect.x
                        self.dragged_column.is_being_dragged = True  # dragged_column gets redrawn only when True
                        self.dragged_column.source_column = i  # index of the column from which the card originates
                        # Sets the position of dragged_column to the position of the clicked card
                        self.dragged_column.set_new_pos(column.get_clicked_card_position())
                        # Sets the offset between the card position and the mouse cursor position
                        # This is used to make sure that the position of the card remains constant relative to the
                        # mouse cursor as it is being dragged
                        self.dragged_column.set_mouse_offset(column.get_clicked_card_position(), pygame.mouse.get_pos())
                        # Transfers the clicked card and all cards below it to dragged_column
                        column.move_cards(column.get_clicked_card_index(), self.dragged_column)
                        break
                    # Checks if the clicked card is the last card in the column and is facing down; if yes, flips it
                    if (column.get_last_card().is_facing_up == 0
                            and column.get_last_card().rect.collidepoint(pygame.mouse.get_pos())):
                        self.undo_stack.append(i)
                        column.get_last_card().flip()
                # Checks if a button got clicked and if yes, calls the function assigned to it
                for button in self.on_screen_buttons:
                    button.run_command()

            if event.type == pygame.MOUSEBUTTONUP:
                # Evaluates double click conditions
                self.double_click.increment_clicks()
                if self.double_click.double_clicked():
                    # If double clicked, moves the card to its respective base (if eligible)
                    if not self.dragged_column.is_empty():
                        for base in self.bases:
                            if (self.dragged_column.get_first_card().suit == base.suit
                                    and base.get_current_rank() + 1 == self.dragged_column.get_first_card().rank):
                                self.undo_stack.append((base,
                                                        base.get_number_of_cards(),
                                                        self.columns[self.dragged_column.source_column]))
                                self.dragged_column.move_cards(0, base)
                                break

                # Moves the dragged cards to their target column
                if not self.dragged_column.is_empty():
                    self.dragged_column.is_being_dragged = False
                    for i, column in enumerate(self.columns):
                        # Condition check
                        if (not column.is_empty()
                                and column.get_last_card().rect.colliderect(self.dragged_column.get_first_card())
                                and (column.get_last_card().suit == self.dragged_column.get_first_card().suit
                                     or column.get_last_card().suit == "Foundation")
                                and column.get_last_card().rank == self.dragged_column.get_first_card().rank + 1):
                            # Adds the move data to the undo stack
                            self.undo_stack.append((self.columns[i],
                                                    self.columns[i].get_number_of_cards(),
                                                    self.columns[self.dragged_column.source_column]))
                            self.dragged_column.move_cards(0, self.columns[i])
                            # Records the card's position at mousebuttonup
                            self.clicked_card_end_pos = self.clicked_card.rect.x
                            # If the card hasn't changed position, removes the last move from the undo stack
                            if self.clicked_card_start_pos == self.clicked_card_end_pos:
                                self.undo_stack.pop()
                            break

                # Moves the dragged card to a base
                if not self.dragged_column.is_empty():
                    for base in self.bases:
                        # Condition check
                        if (self.dragged_column.get_first_card().rect.colliderect(base)
                                and len(self.dragged_column.cards) == 1
                                and self.dragged_column.get_first_card().suit == base.suit
                                and (self.dragged_column.get_first_card().rank == 1
                                     or self.dragged_column.get_first_card().rank == base.cards[-1].rank + 1)):
                            # Adds the move data to the undo stack
                            self.undo_stack.append((base,
                                                    base.get_number_of_cards(),
                                                    self.columns[self.dragged_column.source_column]))
                            self.dragged_column.move_cards(0, base)
                            break

                    # If no cconditions are met, moves the dragged cards back to the column they were taken from
                    self.dragged_column.move_cards(0, self.columns[self.dragged_column.source_column])

        # If a column is empty, adds a special invisible card with a suit of "Foundation" the King can latch onto
        for column in self.columns:
            if column.is_empty():
                column.add_card(Card(14, "Foundation", game_window))
            else:
                if len(column.cards) > 1 and column.cards[0].suit == "Foundation":
                    del column.cards[0]

        # Draws the cards and buttons
        self.draw_playing_field()

    def game_loop(self):
        """Main game loop"""
        while True:
            self.double_click.update()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Fills the background with color
            game_window.fill("#317B2F")

            # Greys out the undo button if there are no actions to undo
            self.set_undo_button_status()

            # Checks victory conditions
            if self.is_victorious():
                self.state = "Victory"

            if self.state == "Game":
                self.gameplay(events)
            # If game.state is not "Game", shows the appropriate message window
            elif self.state == "Help (Playable)":
                self.show_message_box(events,
                                      self.ok_buttons,
                                      still_playable_text_1, 370,
                                      still_playable_text_2, 450)
            elif self.state == "Help (Unplayable)":
                self.show_message_box(events,
                                      self.play_again_or_back_buttons,
                                      not_playable_text_1, 370,
                                      not_playable_text_2, 440)
            elif self.state == "Really quit?":
                self.show_message_box(events,
                                      self.quit_buttons,
                                      really_quit_text_1, 360,
                                      really_quit_text_2, 440)
            elif self.state == "Victory":
                self.show_message_box(events,
                                      self.play_again_or_quit_buttons,
                                      victory_text_1, 360,
                                      victory_text_2, 450)

            pygame.display.update()
            clock.tick(60)


game = Game()
game.deal_cards()
game.game_loop()
