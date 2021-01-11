from core.Simulator.Manager import BallManager, SkillManager
from . import StageBase

combo = ['阔步', '改革', '观察', '注视加工', '阔步', '比尔格的祝福', '制作']


class Stage4(StageBase):
    def __init__(self, solver):
        super().__init__(solver)
        self.Prequeue = []
        self.count = 0
        self.use_change = self.solver.conf.get('DesignChange', 'open') == 'True'

    def deal(self, status, prev_skill=None):
        if prev_skill.name == '设计变动':
            self.design_count += 1
        if self.Prequeue[0] == '比尔格的祝福' and self.use_change and self.design_count < 3 and self.need_changes(status):
            return '设计变动'
        self.count += 1
        if self.count >= len(combo) and status.currentQuality < 58000:
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
        current_final = status.use_skill(SkillManager['比尔格的祝福']).currentQuality
        if current_final > 77000:
            self.log('no need',current_final)
            return False
        temp = status.clone()
        temp.ball = BallManager.RedBall
        mark = temp.use_skill(SkillManager['比尔格的祝福']).currentQuality
        self.log(mark)
        return mark > 77000
