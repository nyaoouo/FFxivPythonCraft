from .Maths import lv2clv


class Crafter(object):
    def __init__(self, lv: int, craft: int, control: int, maxCp: int):
        self.lv = lv
        self.craft = craft
        self.control = control
        self.maxCp = maxCp
        self.clv = lv2clv(lv)

    def update(self, lv: int = None, craft: int = None, control: int = None, maxCp: int = None):
        if lv is not None:
            self.lv = lv
            self.clv = lv2clv(lv)
        self.craft = craft or self.craft
        self.control = control or self.control
        self.maxCp = maxCp or self.maxCp


class Target(object):
    def __init__(self, rlv, maxDurability, maxProgress, maxQuality):
        self.rlv = rlv
        self.maxDurability = maxDurability
        self.maxProgress = maxProgress
        self.maxQuality = maxQuality
