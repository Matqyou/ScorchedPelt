class ClickableBox:
    def __init__(self, rect: tuple):
        self.x, self.y, self.w, self.h = rect
        self.bound_x = self.x + self.w
        self.bound_y = self.y + self.h
        self.function = None
        self.function2 = None
        self.hover = False

    def UpdateSize(self, size: tuple):
        self.w, self.h = size
        self.bound_x = self.x + self.w
        self.bound_y = self.y + self.h

    def UpdateRect(self, rect: tuple):
        self.x, self.y, self.w, self.h = rect
        self.UpdateSize((self.w, self.h))

    def SetFunction(self, function):
        self.function = function

    def SetFunction2(self, function):
        self.function2 = function

    def PointCollidesBox(self, x, y):
        return self.x <= x <= self.bound_x and self.y <= y <= self.bound_y

    def ClickEvent(self, event):
        if self.PointCollidesBox(*event.pos):
            if self.function is not None and event.button == 1:
                self.function()
            elif self.function2 is not None and event.button == 3:
                self.function2()

    def Tick(self, x, y):
        self.hover = self.PointCollidesBox(x, y)
