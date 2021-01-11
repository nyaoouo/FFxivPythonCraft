from core.Simulator.Manager import SkillManager
from core.Simulator.Status import Status
from core.Utils.Logger import Logger

def Terminator(status:Status):
    Logger("terminate!!!",tag="terminator")
    if status.currentCp>=SkillManager.getCp('坯料加工',status)*status.ball.cp:
        return '坯料加工'
    return '仓促'
