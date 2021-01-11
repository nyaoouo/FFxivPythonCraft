from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Utils.Logger import Logger

combo = ['阔步', '改革', '观察', '注视加工', '阔步', '比尔格的祝福', '制作']
Prequeue = []
count = 0


def init(player: Crafter, target: Target):
    pass


def solve(status: Status):
    global count
    count += 1
    if count >= len(combo) and status.currentQuality < 58000:
        #Logger("进入自毁模式", tag="stage_4")
        return 'terminate'
    return Prequeue.pop(0)


def is_finished(status: Status):
    global Prequeue
    if count == 0: Prequeue = combo[:]
    return False


def reset():
    global count
    count = 0
    Prequeue.clear()
