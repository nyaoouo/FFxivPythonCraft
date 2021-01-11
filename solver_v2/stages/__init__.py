from core.Simulator import Role


class StageBase(object):
    def __init__(self, solver):
        self.solver = solver

    def log(self, msg, *msgs, lv=0, tag=None):
        if tag is None:
            tag=type(self).__name__
        self.solver.log(msg,*msgs,lv=lv,tag=tag)

    def is_finished(self, status, prev_skill=None):
        return True

    def deal(self, status, prev_skill=None):
        return None

    def reset(self):
        pass
