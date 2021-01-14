from core.Simulator.Manager import BallManager, SkillManager
from core.Utils.i18n import solver_to_client_text as _
from . import StageBase
from ..Utils import *


class Stage1(StageBase):
    def is_finished(self, status, prev_skill=None):
        return self.is_progress_finished and InnerQuietLv(status) >= 8

    def is_progress_finished(self, status, prev_skill=None):
        temp = Status(status.player, status.target, BallManager.WhiteBall).use_skill(SkillManager[_('制作')]).currentProgress
        return status.currentProgress + temp >= status.target.maxProgress

    def careful_check(self, status, skill):
        temp = status.use_skill(skill)
        if not status.has_buff(_('最终确认')) and temp.is_finish():
            return _('最终确认')
        else:
            return skill.name

    def process_skill(self, status):
        if self.is_progress_finished(status.use_skill(SkillManager[_('模范制作')])):
            return self.careful_check(status, SkillManager[_('模范制作')])
        else:
            return self.careful_check(status, SkillManager[_('高速制作')])

    def deal(self, status, prev_skill=None):
        if status.currentCp < 300:
            return 'terminate'
        if status.rounds == 1: return _('闲静')
        if status.ball == BallManager.GreenBall:
            if not status.has_buff(_('掌握')): return _('掌握')
            if status.currentDurability < 20: return _('精修')
        if status.ball == BallManager.RedBall:
            if InnerQuietLv(status) < 10 and status.currentDurability > 10:
                return _('集中加工')
            return _('秘诀')
        if status.ball == BallManager.PurpleBall:
            if not status.has_buff(_('掌握')): return _('掌握')
            if not status.has_buff(_('崇敬')): return _('崇敬')
            if not status.has_buff(_('俭约')): return _('长期俭约')
        if status.currentDurability - (status.ball.durability * 10) <= 0:
            return _('精修')
        if status.ball == BallManager.DeepBlueBall and not self.is_progress_finished(status):
            return self.process_skill(status)
        if status.has_buff(_('崇敬')) and not self.is_progress_finished(status):
            return self.process_skill(status)
        if InnerQuietLv(status)<=8:
            return _('仓促')
        return _('崇敬')
