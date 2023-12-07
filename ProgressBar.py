from ThemeManager import ThemeManager
from time import perf_counter
from math import ceil
import pygame
FONT = None
END_SOUND = None


def SetProgressBarFont(font: pygame.font.Font) -> None:
    global FONT
    FONT = font


def SetProgressBarEndSound(sound: pygame.mixer.Sound) -> None:
    global END_SOUND
    END_SOUND = sound


class ProgressBar:
    def __init__(self, progress: float, size: tuple, themes: ThemeManager, color_key: str,
                 padding: tuple = (0, 0)):
        self.progress = progress
        self.w, self.h = size
        self.x_inner = padding[0]
        self.y_inner = padding[1]
        self.w_inner = self.w - self.x_inner * 2
        self.h_inner = self.h - self.y_inner * 2
        self.themes = themes
        self.get_inner_color = lambda: getattr(self.themes, color_key)

        self.w_current = None
        self.surface = pygame.Surface(size)
        self.update = True

    def UpdateProgress(self, progress: float):
        self.progress = progress
        self.update = True

    def GetSurface(self):
        if self.update:
            self.surface.fill(self.themes.bar_frame)
            self.w_current = round(self.w_inner * self.progress)
            pygame.draw.rect(self.surface, 0x000000, (self.x_inner, self.y_inner, self.w_inner, self.h_inner))
            pygame.draw.rect(self.surface, self.get_inner_color(), (self.x_inner, self.y_inner, self.w_current, self.h_inner))
        return self.surface


class TimedProgressBar(ProgressBar):
    def __init__(self, period_seconds: int, progress: float, size: tuple, themes: ThemeManager,
                 color_key: str, padding: tuple = (0, 0), button: str = None):
        super().__init__(progress, size, themes, color_key, padding)

        self.period = period_seconds
        self.button = button
        self.timestamp = perf_counter()
        self.seconds = self.last_seconds = None
        self.timestamp = perf_counter()
        self.record = False
        self.last_caption = None
        self.time_elapsed = None

        self.UpdateProgress(0)

    def ResetTime(self):
        self.timestamp = perf_counter() + self.period
        self.record = True

    def GetTimeDifference(self):
        return self.timestamp - perf_counter()

    def GetSurface(self):
        if self.seconds is not None:
            self.UpdateProgress(self.seconds / self.period)
        super().GetSurface()

        if self.seconds is not None:
            ceiled_absoulte = abs(ceil(self.seconds))
            color = (0xFF0000FF, 0xFFFFFFFF)[self.seconds > 0]
            caption = f'{ceiled_absoulte//60}:{ceiled_absoulte%60:>02}'
        else:
            caption = f'Press {self.button} to begin'
            color = 0xFFFFFFFF
        if caption != self.last_caption:
            self.time_elapsed = FONT.render(caption, True, color)
        self.surface.blit(self.time_elapsed, (max(self.x_inner, self.x_inner + self.w_current - self.time_elapsed.get_width()), self.h - self.time_elapsed.get_height()))
        self.last_caption = caption
        return self.surface

    def Tick(self):
        self.last_seconds = self.seconds
        if self.record:
            self.seconds = self.GetTimeDifference()

        if self.last_seconds is not None and \
                self.seconds <= 0 and self.last_seconds > 0:
            END_SOUND.play()
