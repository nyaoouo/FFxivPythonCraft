from core.Simulator.Manager import SkillManager
from core.Simulator.Status import Status
from . import StageBase


class Terminator(StageBase):
    def deal(self, status: Status, prev_skill=None):
        self.log("terminate!!!")
        if status.currentCp >= SkillManager.getCp('坯料加工', status) * status.ball.cp:
            return '坯料加工'
        return '仓促'
