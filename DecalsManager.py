class DecalsManager:
    def __init__(self):
        self.bank = None
        self.boat = None
        self.rob = None
        self.hitman = None
        self.icon = None

    def SetDecals(self, decals: dict):
        for key, value in decals.items():
            setattr(self, key, value)
