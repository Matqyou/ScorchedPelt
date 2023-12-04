from ProgressBar import SetProgressBarFont, SetProgressBarEndSound, TimedProgressBar
from NewServerButton import SetButtonFont, NewServerButton
from GroupOfBars import GroupOfBars, SetIconDecals
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
    'hitman': 'Hitman.png',
    'icon': 'Icon.png'
}
text_decals = {
    'rob': ('Rob', 0xFFFF00FF)
}
resize_decals = {
    'bank': (26, 26),
    'boat': (26, 26),
    'rob': (26, 26),
    'hitman': (26, 26),
    'icon': (32, 32)
}

decals = {}
for key, decal_path in decal_paths.items():
    decals[key] = pygame.image.load(decal_path)
for key, text_info in text_decals.items():
    text, text_color = text_info
    decals[key] = best_font_ever.render(text, True, text_color)
for key, new_size in resize_decals.items():
    if key not in decal_paths:
        continue
    decals[key] = pygame.transform.smoothscale(decals[key], new_size)
SetIconDecals(decals)

rob_decal = decals['rob']
theme_colors = [
    [
        0x978052,  # 0 Bar frame
        0xAAAA33,  # 1 Bar color rob
        0xAA3333,  # 2 Bar color bank
        0x3333AA,  # 3 Bar color boat
        0x383226,  # 4 Group background
        0x544B39,  # 5 Group background hover
        0x993399,  # 6 Group outline
        0x2D291F,  # 7 Window background
    ],
    [
        0x513838,  # 0 Bar frame
        0xAAAA33,  # 1 Bar color rob
        0xAA3333,  # 2 Bar color bank
        0x3333AA,  # 3 Bar color boat
        0x160202,  # 4 Group background
        0x2D1010,  # 5 Group background hover
        0xB50000,  # 6 Group outline
        0x0A0101,  # 7 Window background
    ],
    [
        0x777777,  # 0 Bar frame
        0xAAAA33,  # 1 Bar color rob
        0xAA3333,  # 2 Bar color bank
        0x3333AA,  # 3 Bar color boat
        0x262626,  # 4 Group background
        0x565656,  # 5 Group background hover
        0x25C4C4,  # 6 Group outline
        0x111111,  # 7 Window background
    ]
]
theme_buttons = [ThemeButton((WIDTH-30-33*i-10, 10, 30, 30), colors) for i, colors in enumerate(theme_colors)]
current_theme = []
current_theme[:] = theme_buttons[0].colors


def SetCurrentTheme(new_theme: list):
    global current_theme
    current_theme[:] = new_theme


for theme_button in theme_buttons:
    theme_button.SetFunction(lambda colors=theme_button.colors: SetCurrentTheme(colors))
robbing_progress_bar = TimedProgressBar(60, 0, (400, 15), current_theme, 1, (2, 2), '`')
initial_group = GroupOfBars((10, 45+36), current_theme)
bar_groups = {0: initial_group}
current_group = 0
server_button = NewServerButton((10, 10, 125, 25), current_theme, (2, 2))
display = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Scorched Pelt')
pygame.display.set_icon(decals['icon'])
clock = pygame.time.Clock()


def ResetTimedProgressBar(progress_bar: TimedProgressBar):
    progress_bar.ResetTime()
    start_sound.play()


def ListenForKeys(keyboard_event):
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
        new_position = (10, 45+36)
        current_group = CURRENT_GROUP_ID
    new_group = GroupOfBars(new_position, current_theme)
    bar_groups[CURRENT_GROUP_ID] = new_group
    new_group.SetFunction(lambda id_=CURRENT_GROUP_ID: SelectCurrentGroup(id_))
    new_group.SetFunction2(lambda id_=CURRENT_GROUP_ID: DeleteGroup(id_))
    CURRENT_GROUP_ID += 1


def SelectCurrentGroup(index: int):
    global current_group
    current_group = index


def DeleteGroup(index: int):
    global current_group
    bar_groups.pop(index)
    if index == current_group:
        if bar_groups:
            current_group = list(bar_groups.keys())[0]
        else:
            current_group = None


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
    if elapsed >= 3600:
        caption = f'Scorched Pelt | {elapsed // 3600:>02}:{(elapsed//60)%60:>02}:{elapsed % 60:>02}'
    else:
        caption = f'Scorched Pelt | {elapsed // 60:>02}:{elapsed % 60:>02}'
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
    display.fill(current_theme[7])

    server_button.Draw(display)

    display.blit(rob_decal, (20, 45))
    display.blit(robbing_progress_bar.GetSurface(), (56, 50))

    for i, bar_group in bar_groups.items():
        bar_group.Draw(display, i == current_group)
    for theme_button in theme_buttons:
        theme_button.Draw(display)

    pygame.display.update()

    clock.tick(15)
