from . import StageBase

combo = ['阔步', '改革', '观察', '注视加工', '阔步', '比尔格的祝福', '制作']


class Stage4(StageBase):
    def __init__(self, solver):
        super().__init__(solver)
        self.Prequeue = []
        self.count = 0

    def deal(self,status,prev_skill=None):
        self.count += 1
        if self.count >= len(combo) and status.currentQuality < 58000:
            return 'terminate'
        return self.Prequeue.pop(0)

    def is_finished(self,status,prev_skill=None):
        if self.count == 0: self.Prequeue = combo[:]
        return False

    def reset(self):
        self.count = 0
        self.Prequeue.clear()
