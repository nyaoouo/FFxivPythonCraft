from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Manager import BallManager
from core.Utils.Logger import Logger

count=5

def init(player: Crafter, target: Target):
    pass


def solve(status: Status):
    global count
    count+=1
    if status.rounds >= 25 or status.currentCp<300 or (count>=8 and status.buffs["内静"].data["lv"]<7):
        #Logger("进入自毁模式", tag="stage_2")
        return 'terminate'
    if status.ball == BallManager.GreenBall:
        if "掌握" not in status.buffs:
            return "掌握"
        if status.currentDurability < 20:
            return "精修"
    if status.currentDurability <= 10:
        return "精修"
    if status.ball == BallManager.RedBall:
        if status.buffs["内静"].data["lv"] < 10:
            return "集中加工"
        return "秘诀"
    elif status.ball == BallManager.YellowBall:
        if status.buffs["内静"].data["lv"] < 7:
            return '专心加工'
        return "仓促"
    if status.currentDurability - (status.ball.durability * 10) <= 10:
        return "精修"
    if status.buffs["内静"].data["lv"] < 6 and count<5:
        return '专心加工'
    if '俭约' not in status.buffs:
        return "俭约加工"
    return "仓促"


def is_finished(status: Status):
    return not("内静" in status.buffs and status.buffs["内静"].data["lv"] < 8)


def reset():
    global count
    count=0
