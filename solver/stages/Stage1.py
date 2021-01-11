from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Definitions import names
from core.Simulator.Manager import BallManager, SkillManager
from core.Utils.Logger import Logger
SynthesisPush = 0


def init(player: Crafter, target: Target):
    global SynthesisPush
    SynthesisPush = Status(player, target, BallManager.WhiteBall).use_skill(SkillManager[names["BasicSynthesis"]]).currentProgress

def solve(status: Status):
    if status.rounds >= 20 or status.currentCp<300:
        #Logger("进入自毁模式",tag="stage_1")
        return 'terminate'
    if status.rounds == 1:
        return names["Reflect"]
    if status.ball == BallManager.GreenBall:
        if names["Manipulation"] not in status.buffs: return names["Manipulation"]
        if status.currentDurability < 20: return names["MastersMend"]
        # if names["WasteNot"] not in status.buffs: return names["WasteNotTwo"]
    if status.ball == BallManager.RedBall:
        if names["InnerQuiet"] in status.buffs and status.buffs[names["InnerQuiet"]].data["lv"] < 10 and status.currentDurability > 10:
            return names["PreciseTouch"]
        return names["TricksOfTheTrade"]
    if status.ball == BallManager.YellowBall:
        if names["InnerQuiet"] in status.buffs and status.buffs[names["InnerQuiet"]].data["lv"] < 6 and status.currentDurability > 10:
            return names["PatientTouch"]
    if status.currentDurability - (status.ball.durability * 10) <= 0:
        return names["MastersMend"]
    if names["Veneration"] not in status.buffs:
        return names["Veneration"]
    else:
        return names["RapidSynthesis"]


def is_finished(status: Status):
    return status.currentProgress + SynthesisPush >= status.target.maxProgress


def reset():
    pass
