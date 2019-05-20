
class Security():
    def __init__(self):
        self.date = ""
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.volume = 0
        self.symbol = ''
        self.name = ''
        self.zone = ''
        self.m5_change = 0
        self.m10_change = 0
        self.m15_change = 0
        self.m20_change = 0
        self.m60_change = 0
        self.rolling_mean = 0
    
    def to_class(self, **entries):
        self.__dict__.update(entries)