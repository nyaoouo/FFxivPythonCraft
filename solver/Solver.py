from core.Utils.GetBall import get_ball

from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Manager import SkillManager, BuffManager, BallManager, managers_load
from core.Utils.TTS import TTS
from core.Utils.Namazu import use_skill
from core.Utils.Logger import Logger
from time import sleep
import json
import time
import os
from solver import CraftSolver
from core.Utils.Config import config

'please load the data of managers before everything'
managers_load()

'''
Crafter: player object
Crafter([lv],[craft],[control],[maxCp])

Target: the formula object
Target([rlv], [maxDurability], [maxProgress], [maxQuality])
'''
player = Crafter(
    int(config['player']['lv']),
    int(config['player']['craft']),
    int(config['player']['control']),
    int(config['player']['cp']),
)
target = Target(
    int(config['target']['rlv']),
    int(config['target']['Durability']),
    int(config['target']['Progress']),
    int(config['target']['Quality'])
)

'''
Status: object store the craft state
Status([Crafter], [Target], [the ball state])
'''
status = None
memFix = config['MemoryFixStatus']['open'] == 'True'
terminator = config['AutoTerminator']['open'] == 'True'
log_name = "log.txt"

Logger.hideTag("Math")
CraftSolver.init(player, target)
Logger.showTag("Math")
data_queue = []
if memFix: from core.Utils.FFxivCraftMem import fix_status, fix_crafter
if terminator: from solver.stages.Terminator import Terminator
terminate=False

def format_status(status):
    print("#" * 10 + "r %s" % status.rounds + "#" * 10)
    print("ball:\t{}".format(status.ball.name))
    print("durability:\t{}/{}".format(status.currentDurability, status.target.maxDurability))
    print("progress:\t{}/{}".format(status.currentProgress, status.target.maxProgress))
    print("quality:\t{}/{}".format(status.currentQuality, status.target.maxQuality))
    if status.buffs: print("buffs:", " ".join([str(buff) for buff in status.buffs.values()]))
    print("CP:\t{}/{}".format(status.currentCp, status.player.maxCp))


def deal_status(status):
    global terminate
    recommend =Terminator(status) if terminate else CraftSolver.StatusSolve(status)
    if recommend is not None:
        print("recommend:\t{}".format(recommend))
        if recommend == "terminate" and terminator:
            terminate=True
            recommend = Terminator(status)
        if recommend != "terminate":
            use_skill(recommend)
        TTS(recommend)
        return recommend
    else:
        print("no recommend")
        return None


start_time_stamp = None
start = None


def solver(msg):
    global status, data_queue, start, start_time_stamp,terminate
    Logger(msg, tag="Solver")
    data = msg.split(" ", 1)
    if data[0] == "start":
        if memFix: fix_crafter(player)
        status = Status(player, target, BallManager.defaultBall)
        format_status(status)
        data_queue = [[None, type(BallManager.defaultBall).__name__]]
        start = time.perf_counter()
        start_time_stamp = int(time.time())
        return deal_status(status)
    elif data[0] == "use":
        if len(data) == 2 and status is not None:
            data = data[1].rsplit(" ", 1)
            skill = data[0] if len(data) == 1 or data[1] == "成功" else data[0] + ":fail"
            if skill in SkillManager:
                print("use:", skill)
                data_queue[-1][0] = skill
                status = status.use_skill(SkillManager[skill])
                if not status.is_finish():
                    sleep(0.5)
                    status.ball = get_ball()
                    if memFix: fix_status(status)
                    data_queue.append([None, type(status.ball).__name__])
                    format_status(status)
                    return deal_status(status)
            else:
                raise Exception("unknown skill %s" % skill)
    elif data[0] == "end":
        if data_queue and status is not None:
            with open(os.path.join(config.BasePath, log_name), "a+") as f:
                f.write(str(start_time_stamp) + "|")
                f.write("|".join("{};{}".format(i[0], i[1]) for i in data_queue))
                f.write("|{}|{}|{}\n".format(status.currentProgress, status.currentQuality, time.perf_counter() - start))
        print("#" * 10 + "end" + "#" * 10)
        TTS("finsih")
        status = None
        terminate=False
        return ("end")
    else:
        print("unknown")
    return ""
