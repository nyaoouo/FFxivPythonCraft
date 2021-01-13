from . import Maths
from .Utils import CallOrVar


class StatusBuff(object):
    def __str__(self):
        return str(self.buff) + str(self.buff.get_comments(self))

    def __init__(self, buff, rounds=None, data=None):
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.buff = buff
        self.rounds = rounds
        buff.defaultStatus(self)
    def clone(self):
        return StatusBuff(self.buff, rounds=self.rounds,data=self.data)

    def nextRound(self, status):
        temp = self.clone()
        temp.rounds-=1
        temp.buff.nextRound(temp, status)
        return temp

    def progressBuff(self, skill, glob):
        return CallOrVar(self.buff.progressBuff, skill, self, glob)

    def qualityBuff(self, skill, glob):
        return CallOrVar(self.buff.qualityBuff, skill, self, glob)

    def cpBuff(self, skill, glob):
        return CallOrVar(self.buff.cpBuff, skill, self, glob)

    def durabilityBuff(self, skill, glob):
        return CallOrVar(self.buff.durabilityBuff, skill, self, glob)


class Status(object):
    def __init__(self, player, target, ball, rounds=1, baseProgress=None, baseQuality=None,
                 currentDurability=None, currentProgress=0, currentQuality=0, currentCp=None, buffs=None, data=None):
        self.player = player
        self.target = target
        self.ball = ball
        self.rounds = rounds
        self.currentProgress = currentProgress
        self.currentQuality = currentQuality
        self.baseProgress = baseProgress if baseProgress is not None else Maths.base_progress(player.craft, player.clv, target.rlv)
        self.baseQuality = baseQuality if baseQuality is not None else [Maths.base_quality(player.control * (i * 0.2 + 1), player.clv, target.rlv) for
                                                                        i in range(11)]
        self.currentDurability = currentDurability if currentDurability is not None else target.maxDurability
        self.currentCp = currentCp if currentCp is not None else player.maxCp
        self.buffs = buffs if buffs is not None else dict()
        self.data = data if data is not None else dict()
        self.buffsToRemove = []
        self.buffsToAdd = []

    def get_status_string(self):
        return ":".join([self.ball.name, str(self.currentProgress), str(self.currentQuality), str(self.currentDurability), str(self.currentCp),
                         ','.join([str(buff) for buff in self.buffs.values()])])

    def is_finish(self):
        return self.currentProgress >= self.target.maxProgress

    def clone(self):
        return Status(player=self.player, target=self.target, rounds=self.rounds, baseProgress=self.baseProgress,
                      baseQuality=self.baseQuality, currentDurability=self.currentDurability,
                      currentProgress=self.currentProgress, currentQuality=self.currentQuality, currentCp=self.currentCp,
                      buffs={key:buff.clone() for key, buff in self.buffs.items()}, ball=self.ball, data=self.data)

    def buff_goes_next(self):
        self.buffs = {name: buff.nextRound(self) for name, buff in self.buffs.items()}
        self.buffs = {name: buff for name, buff in self.buffs.items() if buff.rounds > 0}
        self.rounds += 1

    def use_skill(self, skill, forceBall=None):
        temp = self.clone()
        if forceBall is not None:
            temp.ball = forceBall
        """if not skill.can_use(temp):
            print(temp.get_status_string())
            print(skill.name)
            raise Exception("skill cannot be used")"""
        temp.currentProgress = min(temp.currentProgress + skill.calc_progress(temp), temp.target.maxProgress)
        temp.currentQuality = min(temp.currentQuality + skill.calc_quality(temp), temp.target.maxQuality)
        temp.currentCp = max(temp.currentCp - skill.calc_cp(temp), 0)
        temp.currentDurability = max(temp.currentDurability - skill.calc_durability(temp), 0)
        skill.after_use(temp)
        while temp.buffsToRemove:
            tempBuff = temp.buffsToRemove.pop()
            if tempBuff.name in temp.buffs:
                del temp.buffs[tempBuff.name]
        if not skill.KEEP_ROUND:
            temp.buff_goes_next()
        temp.ball.after_use(temp)
        while temp.buffsToAdd:
            tempBuff = temp.buffsToAdd.pop()
            temp.buffs[tempBuff.buff.name] = tempBuff
        temp.buffs = {k: v for k, v in sorted(temp.buffs.items())}
        return temp

    def remove_buff(self, buff):
        self.buffsToRemove.append(buff)

    def execute_buff_change(self):
        while self.buffsToRemove:
            tempBuff = self.buffsToRemove.pop()
            if tempBuff.name in self.buffs:
                del self.buffs[tempBuff.name]
        while self.buffsToAdd:
            tempBuff = self.buffsToAdd.pop()
            self.buffs[tempBuff.buff.name] = tempBuff

    def add_buff(self, buff):
        self.remove_buff(buff)
        temp = StatusBuff(buff)
        self.buffsToAdd.append(temp)

    def has_buff(self, buff: str):
        return buff in self.buffs

    def get_buff(self, buff: str):
        return self.buffs[buff] if self.has_buff(buff) else None

    def recoverCp(self, amount):
        self.currentCp = min(self.currentCp + amount, self.player.maxCp)

    def recoverDurability(self, amount):
        self.currentDurability = min(self.currentDurability + amount, self.target.maxDurability)
