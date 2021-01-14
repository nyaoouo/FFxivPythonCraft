from core.Simulator.Manager import BallManager, SkillManager
from core.Utils.Config import config
from . import StageBase
from core.Utils.i18n import solver_to_client_text as _

combo = [_('阔步'), _('改革'), _('观察'), _('注视加工'), _('阔步'), _('比尔格的祝福'), _('制作')]

skyStage = config.get('SkybuilderStage', 'Stage', default='3')
if skyStage == '4':
    grade_line = [58000, 65000, 74000]
else:
    grade_line = [58000, 65000, 77000]


def score_grade(score: int):
    if score < grade_line[0]:
        return 0
    elif score < grade_line[1]:
        return 1
    elif score < grade_line[2]:
        return 2
    else:
        return 3


class Stage4(StageBase):
    def __init__(self, solver):
        super().__init__(solver)
        self.Prequeue = []
        self.count = 0
        self.use_change = self.solver.conf.get('DesignChange', 'open') == 'True'
        self.change_grade = int(self.solver.conf.get('DesignChange', 'lv', default="3"))

    def deal(self, status, prev_skill=None):
        if prev_skill.name == _('设计变动'):
            self.design_count += 1
        self.solver.cli_logger.hideTag('Math')
        if self.Prequeue[0] == _('比尔格的祝福') and self.use_change and self.design_count < 3 and self.need_changes(status):
            return _('设计变动')
        self.solver.cli_logger.showTag('Math')
        self.count += 1
        if self.count >= len(combo) and score_grade(status.currentQuality) < 1:
            return 'terminate'
        return self.Prequeue.pop(0)

    def is_finished(self, status, prev_skill=None):
        if self.count == 0: self.Prequeue = combo[:]
        return not bool(self.Prequeue)

    def reset(self):
        self.design_count = 0
        self.count = 0
        self.Prequeue.clear()

    def need_changes(self, status):
        if status.ball == BallManager.RedBall:
            self.log("red ball")
            return False
        current_score = status.use_skill(SkillManager[_('比尔格的祝福')]).currentQuality
        current_grade = score_grade(current_score)
        if current_grade >= 3:
            self.log('no need', current_score, current_grade)
            return False
        temp = status.clone()
        temp.ball = BallManager.RedBall
        new_score = temp.use_skill(SkillManager[_('比尔格的祝福')]).currentQuality
        new_grade = score_grade(new_score)
        self.log("score if use:", new_score, new_grade)
        return new_grade >= self.change_grade and new_grade > current_grade
