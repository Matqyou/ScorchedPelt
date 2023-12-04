from ProgressBar import TimedProgressBar
from ClickableBox import ClickableBox
import pygame
DECALS = []
BANK_RESET_TIME = 12 * 60
BOAT_RESET_TIME = 6 * 60 + 36

BAR_SPACING = 10


def SetIconDecals(decals: dict):
    global DECALS
    DECALS = list(decals.values())


class GroupOfBars(ClickableBox):
    def __init__(self, pos: tuple, theme_array: list):
        super().__init__((*pos, 0, 0))
        self.theme_array = theme_array
        self.bank_bar = TimedProgressBar(BANK_RESET_TIME, 0, (400, 15), theme_array, 2, (2, 2), 'F1')
        self.boat_bar = TimedProgressBar(BOAT_RESET_TIME, 0, (400, 15), theme_array, 3, (2, 2), 'F2')
        self.bars = [
            self.bank_bar,
            self.boat_bar
        ]

        longest_bar = max([bar.surface.get_width() for bar in self.bars])
        width = BAR_SPACING * 2 + longest_bar + 36 + 33
        height = BAR_SPACING + len(self.bars) * (BAR_SPACING + 26)
        self.UpdateSize((width, height))

        self.surface = pygame.Surface((self.w, self.h))

    def GetSurface(self):
        self.surface.fill((self.theme_array[4], self.theme_array[5])[self.hover])
        for i, bar in enumerate(self.bars):
            self.surface.blit(DECALS[i], (BAR_SPACING + 31, BAR_SPACING + i * 31))
            self.surface.blit(bar.GetSurface(), (BAR_SPACING + 31 + 33, 5 + BAR_SPACING + i * 31))
        self.surface.blit(DECALS[2], (BAR_SPACING, BAR_SPACING))
        return self.surface

    def Tick(self, x, y):
        super().Tick(x, y)
        for bar in self.bars:
            bar.Tick()

    def Draw(self, target_surface: pygame.Surface, outline: bool):
        target_surface.blit(self.GetSurface(), (self.x, self.y))
        if outline:
            pygame.draw.rect(target_surface, self.theme_array[6], (self.x, self.y, self.w, self.h), 3)