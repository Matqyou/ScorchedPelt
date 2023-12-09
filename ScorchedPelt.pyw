from ProgressBar import SetProgressBarFont, SetProgressBarEndSound, TimedProgressBar
from NewServerButton import SetButtonFont, NewServerButton
from GroupOfBars import GroupOfBars
from DecalsManager import DecalsManager
from ThemeManager import ThemeManager
from ThemeButton import ThemeButton
from time import perf_counter
from math import ceil
import keyboard
import pygame

SIZE = WIDTH, HEIGHT = (509, 425)
PROGRAM_TIMESTAMP = perf_counter()
LAST_CAPTION = None
CURRENT_GROUP_ID = 1

pygame.init()
pygame.mixer.init()

best_font_ever = pygame.font.Font('BRLNSR.TTF', 16)
bigger_font_ever = pygame.font.Font('BRLNSR.TTF', 26)
SetProgressBarFont(best_font_ever)
SetButtonFont(best_font_ever)

start_sound = pygame.mixer.Sound('Start.wav')
end_sound = pygame.mixer.Sound('End.wav')
SetProgressBarEndSound(end_sound)

decal_paths = {
    'bank': 'Bank.png',
    'boat': 'Boat.png',
    'bank_red': 'BankRed.png',
    'boat_red': 'BoatRed.png',
    'bank_gray': 'BankGray.png',
    'boat_gray': 'BoatGray.png',
    'hitman': 'Hitman.png',
    'icon': 'Icon.png'
}
text_decals = {
    'rob': ('Rob', 0xFFFF00FF)
}
resize_decals = {
    'bank': (26, 26),
    'boat': (26, 26),
    'bank_red': (26, 26),
    'boat_red': (26, 26),
    'bank_gray': (26, 26),
    'boat_gray': (26, 26),
    'rob': (26, 26),
    'hitman': (20, 20),
    'icon': (32, 32)
}

decals_dict = {}
for key, decal_path in decal_paths.items():
    decals_dict[key] = pygame.image.load(decal_path)
for key, text_info in text_decals.items():
    text, text_color = text_info
    decals_dict[key] = best_font_ever.render(text, True, text_color)
for key, new_size in resize_decals.items():
    if key not in decal_paths:
        continue
    decals_dict[key] = pygame.transform.smoothscale(decals_dict[key], new_size)
decals = DecalsManager()
decals.SetDecals(decals_dict)

rob_decal = decals_dict['rob']
theme_keys = [
    *ThemeManager.themes.keys()
]
themes = ThemeManager()
theme_buttons = [ThemeButton((WIDTH - 30 - 33 * i - 10, 10, 30, 30), theme_key) for i, theme_key in enumerate(theme_keys)]


for theme_button in theme_buttons:
    theme_button.SetFunction(lambda theme_key=theme_button.theme_key: themes.SetTheme(theme_key))
robbing_progress_bar = TimedProgressBar(60, 0, (400, 15), themes, 'rob_color', (2, 2), '`')
initial_group = GroupOfBars((10, 45 + 36), themes, decals)
bar_groups = {0: initial_group}
current_group = 0
server_button = NewServerButton((10, 10, 125, 25), themes, (2, 2))
display = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Scorched Pelt')
pygame.display.set_icon(decals_dict['icon'])
clock = pygame.time.Clock()


def ResetTimedProgressBar(progress_bar: TimedProgressBar) -> None:
    progress_bar.ResetTime()
    start_sound.play()


def ListenForKeys(keyboard_event) -> None:
    if keyboard_event.event_type == keyboard.KEY_DOWN:
        if keyboard_event.name in '`~':
            ResetTimedProgressBar(robbing_progress_bar)
        if current_group is not None:
            if keyboard_event.name == 'f1':
                ResetTimedProgressBar(bar_groups[current_group].bars[0])
            elif keyboard_event.name == 'f2':
                ResetTimedProgressBar(bar_groups[current_group].bars[1])


def CreateNewGroup():
    global CURRENT_GROUP_ID, current_group
    if bar_groups:
        last_group = None
        for group in bar_groups.values():
            last_group = group
        new_position = last_group.x, last_group.bound_y + 2
    else:
        new_position = (10, 45 + 36)
        current_group = CURRENT_GROUP_ID
    new_group = GroupOfBars(new_position, themes, decals)
    bar_groups[CURRENT_GROUP_ID] = new_group
    new_group.SetFunction(lambda id_=CURRENT_GROUP_ID: SelectCurrentGroup(id_))
    new_group.SetFunction2(lambda id_=CURRENT_GROUP_ID: DeleteGroup(id_))
    CURRENT_GROUP_ID += 1


def SelectCurrentGroup(index: int) -> None:
    global current_group
    current_group = index


def DeleteGroup(index: int) -> None:
    global current_group
    bar_groups.pop(index)
    if index == current_group:
        if bar_groups:
            current_group = list(bar_groups.keys())[0]
        else:
            current_group = None


def GetTimeText(seconds) -> str:
    if seconds >= 3600:
        return f'Scorched Pelt | {seconds // 3600:>02}:{(seconds // 60) % 60: >02}:{seconds % 60:>02}'
    else:
        return f'Scorched Pelt | {seconds // 60:>02}:{seconds % 60:>02}'


initial_group.SetFunction(lambda: SelectCurrentGroup(0))
initial_group.SetFunction2(lambda: DeleteGroup(0))
server_button.SetFunction(CreateNewGroup)
keyboard.hook(ListenForKeys)

Running = True
while Running:
    # Keyboard, mouse and window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for clickable_box in [*theme_buttons, *bar_groups.values(), server_button]:
                clickable_box.ClickEvent(event)

    # Logic
    elapsed = ceil(perf_counter() - PROGRAM_TIMESTAMP)
    caption = GetTimeText(elapsed)
    if LAST_CAPTION != caption:
        pygame.display.set_caption(caption)
    LAST_CAPTION = caption
    mouse_x, mouse_y = pygame.mouse.get_pos()
    collides = server_button.Tick(mouse_x, mouse_y)
    robbing_progress_bar.Tick()
    for bar_group in bar_groups.values():
        bar_group.Tick(mouse_x, mouse_y)
    for theme_button in theme_buttons:
        theme_button.Tick(mouse_x, mouse_y)

    # Drawing
    display.fill(themes.window_background)

    server_button.Draw(display)

    display.blit(rob_decal, (20, 45))
    display.blit(robbing_progress_bar.GetSurface(), (56, 50))

    for i, bar_group in bar_groups.items():
        bar_group.Draw(display, i == current_group)
    for theme_button in theme_buttons:
        theme_button.Draw(display)

    pygame.display.update()

    clock.tick(15)
