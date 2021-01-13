from .Models import BuffBase
from .Definitions import names
import math


class Observe(BuffBase):
    rounds = 1


class Veneration(BuffBase):
    rounds = 4
    progressBuff=0.5


class Innovation(BuffBase):
    rounds = 4
    qualityBuff=0.5


class InnerQuiet(BuffBase):
    defaultLv = 1

    def defaultStatus(self, status):
        super().defaultStatus(status)
        if "lv" not in status.data:
            status.data["lv"] = self.defaultLv

    def qualityBuff(self, skill, status, glob):
        if status.data["lv"] < 11: status.data["lv"] += 1
        return 0

    def get_comments(self, status):
        return status.data["lv"]


class Reflect(InnerQuiet):
    name=InnerQuiet().name
    defaultLv = 3


class WasteNot(BuffBase):
    rounds = 4
    durabilityBuff=-0.5


class WasteNotTwo(WasteNot):
    name=WasteNot().name
    rounds = 8


class GreatStrides(BuffBase):
    rounds = 3

    def qualityBuff(self, skill, status, glob):
        glob.remove_buff(self)
        return 1


class NameOfTheElements(BuffBase):
    rounds = 3

    def progressBuff(self, skill, status, glob):
        if skill.name != names["BrandOfTheElements"]:
            return 0
        else:
            return 0.02 * math.ceil((glob.target.maxProgress - glob.currentProgress) / glob.target.maxProgress * 100)

class CarefulObservation(BuffBase):
    rounds=5

    def nextRound(self, status, globStatus):
        if globStatus.currentProgress>=globStatus.target.maxProgress:
            globStatus.currentProgress = globStatus.target.maxProgress-1

class MuscleMemory(BuffBase):
    rounds=5
    def progressBuff(self, skill, status, glob):
        glob.remove_buff(self)
        return 1

class Manipulation(BuffBase):
    rounds=8
    def nextRound(self, status, globStatus):
        globStatus.recoverDurability(5)
