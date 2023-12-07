from ClickableBox import ClickableBox
from ThemeManager import ThemeManager
import pygame


class ThemeButton(ClickableBox):
    def __init__(self, rect: tuple, theme_key: str):
        super().__init__(rect)
        self.theme_key = theme_key
        padding = 3
        self.x_inner = padding
        self.y_inner = padding
        self.w_inner = self.w - padding * 2
        self.h_inner = self.h - padding * 2

        bar_frame = ThemeManager.themes[theme_key]['bar_frame']
        group_background = ThemeManager.themes[theme_key]['group_background']
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(bar_frame)
        pygame.draw.rect(self.surface, group_background, (self.x_inner, self.y_inner, self.w_inner, self.h_inner))
        self.surface_hover = self.surface.copy()
        alpha_layer = pygame.Surface((self.w, self.h))
        alpha_layer.fill(0xFFFFFF)
        alpha_layer.set_alpha(75)
        self.surface_hover.blit(alpha_layer, (0, 0))

    def Tick(self, x, y):
        super().Tick(x, y)

    def Draw(self, surface: pygame.Surface):
        surface.blit((self.surface, self.surface_hover)[int(self.hover)], (self.x, self.y))
