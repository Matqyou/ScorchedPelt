from ClickableBox import ClickableBox
from ThemeManager import ThemeManager
import pygame


class ToggleableButton(ClickableBox):
    def __init__(self, rect: tuple, themes: ThemeManager, state: bool = False, icon: pygame.Surface = None):
        super().__init__(rect)
        self.themes = themes
        padding = 3
        self.x_inner = padding
        self.y_inner = padding
        self.w_inner = self.w - padding * 2
        self.h_inner = self.h - padding * 2
        self.state = state
        self.icon = icon
        size = (self.w, self.h)

        self.alpha_surface = pygame.Surface(size)
        self.alpha_surface.fill(0xFFFFFF)
        self.alpha_surface.set_alpha(75)

    def ClickEvent(self, event, translate: tuple = None):
        if translate is None:
            pos = event.pos
        else:
            pos = (event.pos[0] - translate[0], event.pos[1] - translate[1])
        if self.PointCollidesBox(*pos):
            if event.button == 1:
                if self.function is not None:
                    self.function()
                self.state = not self.state
            if self.function2 is not None and event.button == 3:
                self.function2()

    def Tick(self, x, y):
        super().Tick(x, y)

    def Draw(self, surface):
        pygame.draw.rect(surface, (self.themes.bar_frame, self.themes.toggle_outline)[self.state], (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (self.themes.group_background, self.themes.toggle_on)[self.state],
                         (self.x + self.x_inner, self.y + self.y_inner, self.w_inner, self.h_inner))
        surface.blit(self.icon, (self.x + self.x_inner, self.y + self.x_inner))
        if self.hover:
            surface.blit(self.alpha_surface, (self.x, self.y))
