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
            'window_background': 0x2D291F
        },
        'red': {
            'bar_frame': 0x513838,
            'rob_color': 0xAAAA33,
            'bank_color': 0xAA3333,
            'boat_color': 0x3333AA,
            'group_background': 0x160202,
            'group_background_hover': 0x2D1010,
            'group_outline': 0xB50000,
            'window_background': 0x0A0101
        },
        'gray': {
            'bar_frame': 0x777777,
            'rob_color': 0xAAAA33,
            'bank_color': 0xAA3333,
            'boat_color': 0x3333AA,
            'group_background': 0x262626,
            'group_background_hover': 0x565656,
            'group_outline': 0x25C4C4,
            'window_background': 0x111111
        }
    }

    def __init__(self):
        self.bar_frame = None
        self.rob_color = None
        self.bank_color = None
        self.boat_color = None
        self.group_background = None
        self.group_background_hover = None
        self.group_outline = None
        self.window_background = None
        self.SetTheme('default')

    def SetTheme(self, theme_key: str):
        if theme_key not in self.themes:
            return

        for key, value in self.themes[theme_key].items():
            setattr(self, key, value)

