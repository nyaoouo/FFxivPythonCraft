from . import Maths
from .Utils import CallOrVar
from .Definitions import names
import math


class SkillBase(object):
    HIDE = False
    KEEP_ROUND = False

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    def progress(self, status):
        return 0

    def quality(self, status):
        return 0

    def cp(self, status):
        return 0

    def durability(self, status):
        return 0

    def __str__(self):
        return self.name

    def after_use(self, status):
        pass

    def calc_progress(self, status):
        skill_base = CallOrVar(self.progress, status)
        if skill_base == 0: return 0
        progress_efficiency = Maths.total_efficiency(skill_base, sum(buff.progressBuff(self, status) for buff in status.buffs.values()))
        return Maths.total_push(progress_efficiency, status.baseProgress, status.ball.progress)

    def calc_quality(self, status):
        skill_base = CallOrVar(self.quality, status)
        if skill_base == 0: return 0
        innerQuietLv = status.buffs[names["InnerQuiet"]].data["lv"] - 1 if names["InnerQuiet"] in status.buffs else 0
        quality_efficiency = Maths.total_efficiency(skill_base, sum(buff.qualityBuff(self, status) for buff in status.buffs.values()))
        return Maths.total_push(quality_efficiency, status.baseQuality[innerQuietLv], status.ball.quality)

    def calc_cp(self, status):
        skill_base = CallOrVar(self.cp, status)
        if skill_base == 0: return 0
        cpBuffSum = sum(buff.cpBuff(self, status) for buff in status.buffs.values()) + 1
        return math.ceil(skill_base * status.ball.cp * cpBuffSum)

    def calc_durability(self, status):
        skill_base = CallOrVar(self.durability, status)
        if skill_base == 0: return 0
        durabilityBuffSum = sum(buff.durabilityBuff(self, status) for buff in status.buffs.values()) + 1
        return math.ceil(skill_base * status.ball.durability * durabilityBuffSum)

    def can_use(self, status):
        return True


class BuffBase(object):
    rounds = 999
    Tags = []

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    def __str__(self):
        return self.name

    def progressBuff(self, skill, status, glob):
        return 0

    def qualityBuff(self, skill, status, glob):
        return 0

    def cpBuff(self, skill, statu, glob):
        return 0

    def durabilityBuff(self, skill, status, glob):
        return 0

    def defaultStatus(self, status):
        if status.rounds is None:
            status.rounds = self.rounds

    def nextRound(self, status, globStatus):
        pass

    def get_comments(self, status):
        return status.rounds


class BallBase(object):
    progress = 1
    quality = 1
    durability = 1
    cp = 1

    def __init__(self):
        if not hasattr(self, "name"):
            if type(self).__name__ in names:
                self.name = names[type(self).__name__]
            else:
                self.name = type(self).__name__

    def __str__(self):
        return self.name

    def after_use(self, status):
        pass
