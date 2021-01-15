import time

from core.Simulator.Manager import SkillManager, BallManager
from core.Simulator.Status import Status
from . import StageBase
from core.Utils.i18n import solver_to_client_text as _

durReq = 21
cpReq = 131
AllowBuffs = {
    _('阔步'): _('阔步'),
    _('改革'): _('改革'),
    _('俭约'): _('俭约'),
    _('观察'): _('观察'),
}
AllowSkillSet = {
    _('坯料加工'),
    _('集中加工'),
    _('俭约加工'),
}
AllowSkillSetObserve = {
    _('集中加工'),
    _('注视加工'),
}


class Stage3(StageBase):
    def __init__(self, solver):
        super().__init__(solver)
        self.Prequeue = []

    def allowSkills(self, status: Status):
        remainCp = status.currentCp - cpReq
        ans = list()
        if remainCp < 0: return ans
        if remainCp >= SkillManager.getCp(_('精修'), status) and status.target.maxDurability - status.currentDurability >= 30:
            ans.append([_('精修')])
        if status.currentCp > 200 and \
                not status.has_buff(_('掌握')) and \
                not status.has_buff(_('改革')) and \
                not status.has_buff(_('阔步')):
            ans.append([_('掌握')])
        if status.ball == BallManager.RedBall:
            ans.append([_('秘诀')])
        if not status.has_buff(_('观察')) or status.ball in [BallManager.PurpleBall]:
            for buff in AllowBuffs:
                if not status.has_buff(buff) and remainCp >= SkillManager.getCp(buff, status):
                    ans.append([buff])
        if status.has_buff(_('改革')) or remainCp < 50 or status.ball in [BallManager.RedBall,BallManager.BlueBall]:
            for skill in AllowSkillSetObserve if status.has_buff(_('观察')) else AllowSkillSet:
                if status.currentDurability > SkillManager.getDurability(skill, status) and remainCp >= SkillManager.getCp(skill, status) and \
                        SkillManager[skill].can_use(status):
                    ans.append([skill])
        return ans

    def try_solve(self, status: Status, timeLimit=None):
        best = None
        queue = [[status, []]]
        self.solver.cli_logger.hideTag("Math")
        record = set()
        start = time.perf_counter()
        while queue:
            if timeLimit is not None and time.perf_counter() - start > timeLimit:
                self.solver.cli_logger.showTag("Math")
                return best
            tempData = queue.pop(0)
            allow = self.allowSkills(tempData[0])
            for skills in allow:
                tempStats = tempData[0]
                for i, skill in enumerate(skills):
                    tempStats = tempStats.use_skill(SkillManager[skill])
                    if tempStats.ball != BallManager.WhiteBall: tempStats.ball = BallManager.WhiteBall
                if tempStats.get_status_string() not in record:
                    record.add(tempStats.get_status_string())
                    newData = [tempStats, tempData[1] + skills]
                    if skills[-1] not in AllowBuffs and tempStats.currentDurability > durReq and (
                            best is None or tempStats.currentQuality > best[0].currentQuality):
                        best = newData
                    queue.append(newData)
        self.solver.cli_logger.showTag("Math")
        return best

    def is_finished(self, status, prev_skill=None):
        if not bool(self.Prequeue) or (status.ball not in [BallManager.WhiteBall, BallManager.YellowBall, BallManager.DeepBlueBall]):
            start = time.perf_counter()
            ans = self.try_solve(status, 8)
            if ans:
                self.Prequeue = ans[1]
                self.log("new plan in {:.2f}s:{}({})".format(time.perf_counter() - start, self.Prequeue, ans[0].currentQuality))
        return not bool(self.Prequeue)

    def deal(self, status, prev_skill=None):
        self.log(self.Prequeue)
        return self.Prequeue.pop(0)

    def reset(self):
        self.Prequeue.clear()
