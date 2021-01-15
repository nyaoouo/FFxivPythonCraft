from core.Simulator.Manager import BallManager, SkillManager
from core.Simulator.Status import Status
from core.Utils.i18n import solver_to_client_text as _
from ..Utils import InnerQuietLv
from . import StageBase


class Stage1(StageBase):
    def is_finished(self, status, prev_skill=None):
        temp=Status(status.player, status.target, BallManager.WhiteBall).use_skill(SkillManager[_('制作')]).currentProgress
        return status.currentProgress + temp >= status.target.maxProgress

    def deal(self, status, prev_skill=None):
        if prev_skill == SkillManager[_('高速制作')+':fail']:
            self.count += 1
        if status.rounds == 1:
            return _('闲静')
        if self.count>3 or InnerQuietLv(status) < 2 or status.rounds >= 20 or status.currentCp < 300:
            return 'terminate'
        if status.ball == BallManager.GreenBall:
            if not status.has_buff(_('掌握')): return _('掌握')
            if status.currentDurability < 20: return _('精修')
            # if status.has_buff(_('俭约')): return _('长期俭约')
        if status.ball == BallManager.RedBall:
            if InnerQuietLv(status) < 10 and status.currentDurability > 10:
                return _('集中加工')
            return _('秘诀')
        if status.ball == BallManager.YellowBall:
            if InnerQuietLv(status) < 6 and status.currentDurability > 10:
                return _('专心加工')
        if status.currentDurability - (status.ball.durability * 10) <= 0:
            return _('精修')
        if status.has_buff(_('崇敬')):
            temp=status.use_skill(SkillManager[_('高速制作')])
            if not status.has_buff(_('最终确认')) and temp.is_finish():
                return _('最终确认')
            else:
                return _('高速制作')
        else:
            return _('崇敬')
    def reset(self):

        self.count=0
