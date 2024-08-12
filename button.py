import pygame.font

class Button:
    """a class to built buttons for game"""
    def __init__(self, ai_game, msg):
        """initialize button attribute"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # set the dimensions and property of the button
        self.width, self.height = 200,50

        self.button_colour = (0,135,0)
        self.text_colour = (255,255,255)

        self.font = pygame.font.SysFont(None,48)
        # built the buttons rect object and centre it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # the button msg need to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """turn msg into rendered image and centre text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw blank button and then draw msg"""
        self.screen.fill(self.button_colour,self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

