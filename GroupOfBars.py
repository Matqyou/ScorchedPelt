from ToggleableButton import ToggleableButton
from ProgressBar import TimedProgressBar
from DecalsManager import DecalsManager
from ClickableBox import ClickableBox
from ThemeManager import ThemeManager
import pygame

BANK_RESET_TIME = 12 * 60
BOAT_RESET_TIME = 6 * 60 + 36

BAR_SPACING = 10


class GroupOfBars(ClickableBox):
    def __init__(self, pos: tuple, themes: ThemeManager, decals: DecalsManager):
        super().__init__((*pos, 0, 0))
        self.themes = themes
        self.decals = decals
        self.hitman_box = ToggleableButton((BAR_SPACING, BAR_SPACING, 26, 26), themes, False, decals.hitman)
        self.bank_bar = TimedProgressBar(BANK_RESET_TIME, 0, (400, 15), themes, 'bank_color', (2, 2), 'F1')
        self.boat_bar = TimedProgressBar(BOAT_RESET_TIME, 0, (400, 15), themes, 'boat_color', (2, 2), 'F2')
        self.bars = [
            self.bank_bar,
            self.boat_bar
        ]
        self.bar_icons = [[self.decals.bank, self.decals.boat],
                          [self.decals.bank_red, self.decals.boat_red],
                          [self.decals.bank_gray, self.decals.boat_gray]]

        longest_bar = max([bar.surface.get_width() for bar in self.bars])
        width = BAR_SPACING * 2 + longest_bar + 36 + 33
        height = 5 + BAR_SPACING + len(self.bars) * 31
        self.UpdateSize((width, height))

        self.surface = pygame.Surface((self.w, self.h))

    def GetSurface(self):
        self.surface.fill((self.themes.group_background, self.themes.group_background_hover)[self.hover])
        for i, bar in enumerate(self.bars):
            self.surface.blit(self.bar_icons[self.themes.theme_index][i], (BAR_SPACING + 31, BAR_SPACING + i * 31))
            self.surface.blit(bar.GetSurface(), (BAR_SPACING + 31 + 33, 5 + BAR_SPACING + i * 31))
        self.hitman_box.Draw(self.surface)
        return self.surface

    def ClickEvent(self, event):
        if not self.hitman_box.ClickEvent(event, (self.x, self.y)):
            if self.PointCollidesBox(*event.pos):
                if self.function is not None and event.button == 1:
                    self.function()
                elif self.function2 is not None and event.button == 3:
                    self.function2()

    def Tick(self, x, y):
        super().Tick(x, y)
        self.hitman_box.Tick(x - self.x, y - self.y)
        for bar in self.bars:
            bar.Tick()

    def Draw(self, target_surface: pygame.Surface, outline: bool):
        target_surface.blit(self.GetSurface(), (self.x, self.y))
        if outline:
            pygame.draw.rect(target_surface, self.themes.group_outline, (self.x, self.y, self.w, self.h), 3)