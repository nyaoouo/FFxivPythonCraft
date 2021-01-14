from core.Simulator.Manager import BallManager, SkillManager
from core.Simulator.Status import Status
from core.Utils.i18n import solver_to_client_text as _
from . import StageBase


class Stage2(StageBase):
    def reset(self):
        self.count = 0

    def deal(self, status, prev_skill=None):
        if prev_skill == SkillManager[_('专心加工')+':fail']:
            self.count += 1
        if status.rounds >= 25 or status.currentCp < 300 or self.count >= 2:
            return 'terminate'
        if status.ball == BallManager.GreenBall:
            if not status.has_buff(_('掌握')):
                return _("掌握")
            if status.currentDurability < 20:
                return _("精修")
        if status.currentDurability <= 10:
            return _("精修")
        if status.ball == BallManager.RedBall:
            if status.get_buff(_('内静')).data["lv"] < 10:
                return _("集中加工")
            return _("秘诀")
        elif status.ball == BallManager.YellowBall:
            if 1<status.get_buff(_('内静')).data["lv"] < 7:
                return _('专心加工')
            return _("仓促")
        if status.currentDurability - (status.ball.durability * 10) <= 10:
            return _("精修")
        if 1<status.get_buff(_('内静')).data["lv"] < 6:
            return _('专心加工')
        if not status.has_buff(_('俭约')):
            return _("俭约加工")
        return _("仓促")

    def is_finished(self, status: Status, prev_skill=None):
        return not (status.has_buff(_('内静')) and status.get_buff(_('内静')).data["lv"] < 8)
