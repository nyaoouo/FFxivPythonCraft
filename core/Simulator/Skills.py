from .Models import SkillBase
from .Manager import BuffManager, BallManager
import math
from .Definitions import names

class TEST_FULL_progress(SkillBase):
    name = "test full progress"
    progress = 9999999999
    HIDE = True


class BasicSynthesis(SkillBase):
    def progress(self, status):
        return 120 if status.player.lv >= 31 else 100

    durability = 10


class BasicTouch(SkillBase):
    quality = 100

    durability = 10
    cp = 18


class MastersMend(SkillBase):
    cp = 88

    def after_use(self, status):
        status.recoverDurability(30)


class HastyTouch(SkillBase):
    quality = 100
    durability = 10


class HastyTouchFail(SkillBase):
    name = names["HastyTouch"] + ":fail"
    durability = 10
    HIDE = True


class RapidSynthesis(SkillBase):
    durability = 10

    def progress(self, status):
        return 500 if status.player.lv >= 63 else 250


class RapidSynthesisFail(SkillBase):
    name = names["RapidSynthesis"] + ":fail"
    durability = 10
    HIDE = True


class InnerQuiet(SkillBase):
    cp = 18

    def after_use(self, status):
        status.add_buff(BuffManager.InnerQuiet)


class Observe(SkillBase):
    cp = 7

    def after_use(self, status):
        status.add_buff(BuffManager.Observe)


class TricksOfTheTrade(SkillBase):

    def can_use(self, status):
        return status.ball == BallManager.RedBall

    def after_use(self, status):
        status.recoverCp(20)


class WasteNot(SkillBase):
    cp = 56

    def after_use(self, status):
        status.add_buff(BuffManager.WasteNot)


class Veneration(SkillBase):
    cp = 18

    def after_use(self, status):
        status.add_buff(BuffManager.Veneration)


class StandardTouch(SkillBase):
    quality = 125
    durability = 10
    cp = 32


class GreatStrides(SkillBase):
    cp = 32

    def after_use(self, status):
        status.add_buff(BuffManager.GreatStrides)


class Innovation(SkillBase):
    cp = 18

    def after_use(self, status):
        status.add_buff(BuffManager.Innovation)


class NameOfTheElements(SkillBase):
    cp = 30

    def after_use(self, status):
        status.add_buff(BuffManager.NameOfTheElements)


class BrandOfTheElements(SkillBase):
    cp = 6
    progress = 100
    durability = 10


class CarefulObservation(SkillBase):
    cp = 1
    KEEP_ROUND = True

    def after_use(self, status):
        status.add_buff(BuffManager.CarefulObservation)


class WasteNotTwo(SkillBase):
    cp = 98

    def after_use(self, status):
        status.add_buff(BuffManager.WasteNotTwo)


class ByregotsBlessing(SkillBase):
    durability = 10
    cp = 24

    def can_use(self, status):
        return status.has_buff(names["InnerQuiet"]) and status.get_buff(names["InnerQuiet"]).data["lv"] > 1

    def quality(self, status):
        if names["InnerQuiet"] in status.buffs:
            return (status.buffs[names["InnerQuiet"]].data["lv"] - 1) * 20 + 100
        else:
            return 100

    def after_use(self, status):
        status.remove_buff(buff=BuffManager.InnerQuiet)


class PreciseTouch(SkillBase):
    quality = 150
    durability = 10
    cp = 18

    def can_use(self, status):
        return status.ball == BallManager.RedBall

    def after_use(self, status):
        if names["InnerQuiet"] in status.buffs and status.buffs[names["InnerQuiet"]].data["lv"] < 11:
            status.buffs[names["InnerQuiet"]].data["lv"] += 1


class MuscleMemory(SkillBase):
    progress = 300
    cp = 6
    durability = 10

    def can_use(self, status):
        return status.rounds == 1

    def after_use(self, status):
        status.add_buff(BuffManager.MuscleMemory)


class CarefulSynthesis(SkillBase):
    cp = 7
    progress = 150
    durability = 10


class PatientTouch(SkillBase):
    cp = 6
    quality = 100
    durability = 10

    def after_use(self, status):
        if names["InnerQuiet"] in status.buffs:
            status.buffs[names["InnerQuiet"]].data["lv"] = min((status.buffs[names["InnerQuiet"]].data["lv"] - 1) * 2, 11)


class PatientTouchFail(SkillBase):
    name = names["PatientTouch"] + ":fail"
    cp = 6
    durability = 10
    HIDE = True

    def after_use(self, status):
        if names["InnerQuiet"] in status.buffs:
            status.buffs[names["InnerQuiet"]].data["lv"] = math.ceil(status.buffs[names["InnerQuiet"]].data["lv"] / 2)


class Manipulation(SkillBase):
    cp = 96

    def after_use(self, status):
        status.add_buff(BuffManager.Manipulation)


class PrudentTouch(SkillBase):
    cp = 25
    quality = 100
    durability = 5

    def can_use(self, status):
        return not status.has_buff(BuffManager.WasteNot.name)


class FocusedSynthesis(SkillBase):
    cp = 5
    durability = 10
    progress = 200


class FocusedTouch(SkillBase):
    cp = 18
    durability = 10
    quality = 150

    def can_use(self, status):
        return status.has_buff(names["Observe"])


class FocusedSynthesisFail(SkillBase):
    name = names["FocusedSynthesis"] + ":fail"
    cp = 5
    durability = 10


class FocusedTouchFail(SkillBase):
    name = names["FocusedTouch"] + ":fail"
    cp = 18
    durability = 10


class Reflect(SkillBase):
    quality = 100
    cp = 24
    durability = 10

    def can_use(self, status):
        return status.rounds == 1

    def after_use(self, status):
        status.add_buff(BuffManager.Reflect)


class PreparatoryTouch(SkillBase):
    quality = 200
    cp = 40
    durability = 20

    def after_use(self, status):
        if names["InnerQuiet"] in status.buffs and status.buffs[names["InnerQuiet"]].data["lv"] < 11:
            status.buffs[names["InnerQuiet"]].data["lv"] += 1


class Groundwork(SkillBase):
    def progress(self, status):
        return 300 if status.currentDurability < self.cp else 150

    cp = 18
    durability = 20


class DelicateSynthesis(SkillBase):
    progress = 100
    quality = 100
    cp = 32
    durability = 10


class IntensiveSynthesis(SkillBase):
    progress = 300
    durability = 10
    cp = 6

    def can_use(self, status):
        return status.ball == BallManager.RedBall


class TrainedEye(SkillBase):
    cp = 250

    def after_use(self, status):
        status.currentQuality = status.target.maxQuality


class DesignChanges(SkillBase):
    KEEP_ROUND = True
