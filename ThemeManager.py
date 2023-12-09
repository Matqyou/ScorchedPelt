class ThemeManager:
    themes = {
        'default': {
            'bar_frame': 0x978052,
            'rob_color': 0xAAAA33,
            'bank_color': 0xAA3333,
            'boat_color': 0x3333AA,
            'group_background': 0x383226,
            'group_background_hover': 0x544B39,
            'group_outline': 0x993399,
            'window_background': 0x2D291F,
            'toggle_on': 0x560000,
            'toggle_outline': 0x911F1F,
            'emptied_bar': 0x282828
        },
        'red': {
            'bar_frame': 0x513838,
            'rob_color': 0xAAAA33,
            'bank_color': 0xAA3333,
            'boat_color': 0x3333AA,
            'group_background': 0x160202,
            'group_background_hover': 0x2D1010,
            'group_outline': 0xB50000,
            'window_background': 0x0A0101,
            'toggle_on': 0x720063,
            'toggle_outline': 0xB542A7,
            'emptied_bar': 0x282828
        },
        'gray': {
            'bar_frame': 0x777777,
            'rob_color': 0xAAAA33,
            'bank_color': 0xAA3333,
            'boat_color': 0x3333AA,
            'group_background': 0x262626,
            'group_background_hover': 0x565656,
            'group_outline': 0x25C4C4,
            'window_background': 0x111111,
            'toggle_on': 0x1D5B23,
            'toggle_outline': 0x39B544,
            'emptied_bar': 0x262300
        }
    }
    num_themes = len(themes)

    def __init__(self):
        self.theme_index = None

        self.bar_frame = None
        self.rob_color = None
        self.bank_color = None
        self.boat_color = None
        self.group_background = None
        self.group_background_hover = None
        self.group_outline = None
        self.window_background = None
        self.toggle_on = None
        self.toggle_outline = None
        self.emptied_bar = None
        self.SetTheme('default')

    def SetTheme(self, theme_key: str):
        if theme_key not in self.themes:
            return

        self.theme_index = list(self.themes.keys()).index(theme_key)
        for key, value in self.themes[theme_key].items():
            setattr(self, key, value)

