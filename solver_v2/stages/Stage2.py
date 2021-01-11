from core.Simulator.Manager import BallManager
from core.Simulator.Status import Status
from . import StageBase


class Stage2(StageBase):
    def reset(self):
        self.count = 0

    def deal(self, status, prev_skill=None):
        self.count += 1
        if status.rounds >= 25 or status.currentCp < 300 or (self.count >= 8 and status.get_buff('内静').data["lv"] < 7):
            return 'terminate'
        if status.ball == BallManager.GreenBall:
            if not status.has_buff('掌握'):
                return "掌握"
            if status.currentDurability < 20:
                return "精修"
        if status.currentDurability <= 10:
            return "精修"
        if status.ball == BallManager.RedBall:
            if status.get_buff('内静').data["lv"] < 10:
                return "集中加工"
            return "秘诀"
        elif status.ball == BallManager.YellowBall:
            if status.get_buff('内静').data["lv"] < 7:
                return '专心加工'
            return "仓促"
        if status.currentDurability - (status.ball.durability * 10) <= 10:
            return "精修"
        if status.get_buff('内静').data["lv"] < 6 and self.count < 5:
            return '专心加工'
        if not status.has_buff('俭约'):
            return "俭约加工"
        return "仓促"

    def is_finished(self, status: Status, prev_skill=None):
        return not (status.has_buff('内静') and status.get_buff('内静').data["lv"] < 8)
