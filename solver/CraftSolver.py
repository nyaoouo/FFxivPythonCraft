from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from solver.stages import Stage1, Stage2, Stage3, Stage4

Stages = [
    Stage1,
    Stage2,
    Stage3,
    Stage4,
]


def init(player:Crafter,target:Target):
    for stage in Stages:
        stage.init(player,target)

def StatusSolve(status: Status):
    if status.rounds == 1:
        for stage in Stages:
            stage.reset()
    for stage in Stages:
        if not stage.is_finished(status):
            return stage.solve(status)
    return None
