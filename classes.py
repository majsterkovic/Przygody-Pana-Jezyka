class item:
    def __init__(self, X, Y, Img, change, snd):
        self.X = X
        self.Y = Y
        self.Img = Img
        self.change = change
        self.snd = snd

class text:
    def __init__(self, SR):
        self.Surf = SR[0]
        self.Rect = SR[1]