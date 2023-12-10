import pygame


class Button:
    """Instantiates a button with given properties"""
    def __init__(self,
                 surface,  # The surface to draw the button on
                 command,  # The name of the function to run when the button is clicked
                 x_y_pos,  # Position on the target surface
                 width,  # Button width
                 height,  # Button height
                 text,  # Button text
                 active=True,  # When False, the button is greyed out, won't highlight on mouseover and can't be clicked
                 font_size=40,  # Size of the text font
                 border_color="#FFFFFF",  # Color of the button border
                 text_color="#FFFFFF",  # Color of the text
                 highlight_color="#F53536",  # Color of the mouseover highlight
                 inactive_border_color="#B4C8AD",  # Color of the border when button is inactive
                 inactive_text_color="#B4C8AD",  # Color of the text when button is inactive
                 border_width=3,  # Width of the border
                 border_radius=10,  # How rounded the corners are; 0 means no rounding
                 y_offset=11,  # For adjusting position of the text in the y axis
                 argument=None):  # Argument for the function that runs when button gets clicked (self.command)
        self.surface = surface
        self.x_pos, self.y_pos = x_y_pos
        self.width = width
        self.height = height
        self.active = active
        self.border_color = {  # Sets border color according to whether self.active is True or False
            True: border_color,
            False: inactive_border_color
        }
        self.text_color = {  # Sets text color according to whether self.active is True or False
            True: text_color,
            False: inactive_text_color
        }
        self.highlight_color = highlight_color
        self.inactive_border_color = inactive_border_color
        self.inactive_text_color = inactive_text_color
        self.thickness = border_width
        self.border_radius = border_radius
        self.y_offset = y_offset
        self.font = pygame.font.Font("./Assets/Graphics/Regisha.otf", size=font_size)
        self.text = text
        self.command = command
        self.argument = argument

    def make_active(self):
        self.active = True

    def make_inactive(self):
        self.active = False

    def check_mouseover(self):
        """Returns true on mouseover"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.x_pos <= mouse_x <= self.x_pos + self.width) and (self.y_pos <= mouse_y <= self.y_pos + self.height):
            return True
        return False

    def draw(self,
             show_highlight=True):  # Can be set to False to remove the mousover highlight even when button is active
        """Draws the button"""
        # Renders the button text
        button_text = self.font.render(self.text, True, self.text_color[self.active])
        # Draws the highlight
        if self.active and show_highlight and self.check_mouseover():
            pygame.draw.rect(self.surface, self.highlight_color, (
                self.x_pos, self.y_pos, self.width, self.height), border_radius=self.border_radius)
        # Draws the border
        pygame.draw.rect(self.surface, self.border_color[self.active], (
            self.x_pos, self.y_pos, self.width, self.height), self.thickness, self.border_radius)
        # Draws the text
        self.surface.blit(
            button_text, (self.x_pos + self.width // 2 - button_text.get_width() // 2, self.y_pos + self.y_offset))

    def run_command(self):
        """Calls the function associated with the button"""
        if self.check_mouseover():
            if not self.argument:
                self.command()
            else:
                # If self.argument is not None, passes it to the called function
                self.command(self.argument)
