from ClickableBox import ClickableBox
from ThemeManager import ThemeManager
import pygame
FONT = None


def SetButtonFont(font: pygame.font.Font) -> None:
    global FONT
    FONT = font


class NewServerButton(ClickableBox):
    def __init__(self, rect: tuple, themes: ThemeManager, padding: tuple = (0, 0)):
        super().__init__(rect)
        self.x_inner = padding[0]
        self.y_inner = padding[1]
        self.w_inner = self.w - self.x_inner * 2
        self.h_inner = self.h - self.y_inner * 2
        self.themes = themes

        self.text_surface = FONT.render(f'+ Add Server', True, 0xFFFFFFFF)
        self.text_position = (self.x + self.w_inner/2 - self.text_surface.get_width()/2 + self.x_inner, self.y + self.y_inner)

    def Tick(self, x, y):
        super().Tick(x, y)

    def Draw(self, target_surface):
        pygame.draw.rect(target_surface, self.themes.bar_frame, (self.x, self.y, self.w, self.h))
        inner_color = (self.themes.group_background, self.themes.group_background_hover)[self.hover]
        pygame.draw.rect(target_surface, inner_color, (self.x + self.x_inner, self.y + self.y_inner,
                                                               self.w_inner, self.h_inner))
        target_surface.blit(self.text_surface, self.text_position)
