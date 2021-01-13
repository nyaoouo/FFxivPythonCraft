from . import Definitions
import math
from core.Utils.Logger import Logger

tag = "Math"


def lv2clv(lv: int):
    if lv <= 50: return lv
    return Definitions.clvBase[(lv - 1) // 10 - 5] + Definitions.clvAdjust[(lv - 1) % 10]


def lv_dif_progress(clv: int, rlv: int):
    dif = clv - rlv
    if dif <= -30:
        return 0.8
    elif dif < -20:
        return dif * 0.02 + 1.4
    elif dif <= 0:
        return 1
    elif dif <= 20:
        return Definitions.difProgress[dif]
    else:
        return 1.5


def lv_dif_quality(clv: int, rlv: int):
    dif = clv - rlv
    if dif <= -30:
        return 0.6
    elif dif < -20:
        return dif * 0.04 + 1.8
    else:
        return 1


def base_progress(craft: int, clv: int, rlv: int):
    return math.floor(lv_dif_progress(clv, rlv) * (0.21 * craft + 2) * (10000 + craft) / (10000 + Definitions.suggestProp[rlv][0]))


def base_quality(control: int, clv: int, rlv: int):
    return math.floor(lv_dif_quality(clv, rlv) * (0.35 * control + 35) * (10000 + control) / (10000 + Definitions.suggestProp[rlv][1]))


def total_push(efficiency, base, ball=1):
    Logger("efficiency:{}\tbase:{}\tball:{}".format(efficiency, base, ball), tag=tag)
    temp = math.floor(efficiency * base * ball)
    Logger("total push:{}".format(temp), tag=tag)
    return temp


def total_efficiency(skill, buffSum=0):
    Logger("skill:{}\tbuffSum:{}".format(skill, buffSum), tag=tag)
    return math.floor(skill * (1 + buffSum)) / 100
