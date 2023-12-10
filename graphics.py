import pygame

# Initiates pygame and sets the window properties
pygame.init()
game_window = pygame.display.set_mode((1374, 1024))
pygame.display.set_caption("8-Kabale")
pygame.display.set_icon(pygame.image.load("./Assets/Graphics/icon.png"))
clock = pygame.time.Clock()

# Back of card graphic
card_back_img = pygame.image.load("Assets/Graphics/card_back.png").convert_alpha()

# Message window graphics
msg_window_img = pygame.image.load("./Assets/Graphics/msg_window.png").convert_alpha()

# Font used for text messages
game_font_60 = pygame.font.Font("./Assets/Graphics/SimplySerif-Bold.ttf", size=60)
game_font_50 = pygame.font.Font("./Assets/Graphics/SimplySerif-Bold.ttf", size=50)

# Text messages
still_playable_text_1 = game_font_60.render("Der er stadig kort,", True, "#FFFFFF")
still_playable_text_2 = game_font_60.render("der kan flyttes.", True, "#FFFFFF")
not_playable_text_1 = game_font_50.render("Der kan ikke flyttes flere", True, "#FFFFFF")
not_playable_text_2 = game_font_50.render("kort. Du har tabt!", True, "#FFFFFF")
really_quit_text_1 = game_font_60.render("Er du sikker på,", True, "#FFFFFF")
really_quit_text_2 = game_font_60.render("at du vil afslutte?", True, "#FFFFFF")
victory_text_1 = game_font_60.render("Tillykke!", True, "#FFFFFF")
victory_text_2 = game_font_60.render("Du har vundet!", True, "#FFFFFF")
