from core.Simulator.Manager import BallManager, SkillManager
from core.Simulator.Status import Status
from . import StageBase


class Stage1(StageBase):
    def is_finished(self, status, prev_skill=None):
        temp=Status(status.player, status.target, BallManager.WhiteBall).use_skill(SkillManager['制作']).currentProgress
        return status.currentProgress + temp >= status.target.maxProgress

    def deal(self, status, prev_skill=None):
        if status.rounds >= 20 or status.currentCp < 300:
            return 'terminate'
        if status.rounds == 1:
            return '闲静'
        if status.ball == BallManager.GreenBall:
            if status.has_buff('掌握'): return '掌握'
            if status.currentDurability < 20: return '精修'
            # if status.has_buff('俭约'): return '长期俭约'
        if status.ball == BallManager.RedBall:
            if status.has_buff('内静') and status.get_buff('内静').data["lv"] < 10 and status.currentDurability > 10:
                return '集中加工'
            return '秘诀'
        if status.ball == BallManager.YellowBall:
            if status.has_buff('内静') and status.get_buff('内静').data["lv"] < 6 and status.currentDurability > 10:
                return '专心加工'
        if status.currentDurability - (status.ball.durability * 10) <= 0:
            return '精修'
        if status.has_buff('崇敬'):
            return '高速制作'
        else:
            return '崇敬'
