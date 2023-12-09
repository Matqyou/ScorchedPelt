class DecalsManager:
    def __init__(self):
        self.bank = None
        self.boat = None
        self.bank_red = None
        self.boat_red = None
        self.bank_gray = None
        self.boat_gray = None
        self.rob = None
        self.hitman = None
        self.icon = None

    def SetDecals(self, decals: dict):
        for key, value in decals.items():
            setattr(self, key, value)
