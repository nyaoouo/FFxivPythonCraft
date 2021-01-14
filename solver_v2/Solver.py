import time
import os

from core.Simulator import Manager, Role, Status
from core.Utils import Logger, Config, GetBall
from core.Utils.TTS import TTS
from .Utils import *
from .stages import Terminator,Stage1,Stage2,Stage3,Stage4
from core.Utils.i18n import system_to_client_text as _

Manager.managers_load()
Stages = [Stage1.Stage1, Stage2.Stage2, Stage3.Stage3, Stage4.Stage4]


class Solver(object):
    def __init__(self, recall: callable = None, used_config: Config._config = None):
        self.recall = recall
        if used_config is None:
            self.conf = Config.config
        else:
            self.conf = used_config
        self.player = Role.Crafter(
            int(self.conf.get('player', 'lv', require=True)),
            int(self.conf.get('player', 'craft', require=True)),
            int(self.conf.get('player', 'control', require=True)),
            int(self.conf.get('player', 'cp', require=True)),
        )
        self.target = Role.Target(
            int(self.conf.get('target', 'rlv', require=True)),
            int(self.conf.get('target', 'Durability', require=True)),
            int(self.conf.get('target', 'Progress', require=True)),
            int(self.conf.get('target', 'Quality', require=True))
        )

        self.use_memFix = self.conf.get('MemoryFixStatus', 'open', default='False') == 'True'
        if self.use_memFix:
            from core.Utils import FFxivCraftMem
            self.memFixer = FFxivCraftMem

        self.use_terminator = self.conf.get('AutoTerminator', 'open', default='False') == 'True'

        self.use_log = self.conf.get('Log', 'open', default='True') == 'True'
        if self.use_log:

            log_name = self.conf.get('Log', 'file_name', default="log_{time}.txt").format(time=int(time.time()))
            folder_path=os.path.join(self.conf.BasePath, 'logs')
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            self.log_path = os.path.join(folder_path, log_name)

        self.Stages = [stage(self) for stage in Stages]
        self.cli_logger = Logger.Logger
        self.update_ball = GetBall.get_ball
        self.terminator = Terminator.Terminator(self)
        self.reset()

    def log(self, msg, *msgs, lv=0, tag="Solver"):
        self.cli_logger(msg, *msgs, lv=lv, tag=tag)

    def __call__(self, msg: str):
        self.log("Revive:", msg)
        data = msg.split(" ", 1)
        if data[0] == 'start':
            return self.start_round()
        elif data[0] == 'use':
            if len(data) < 2:
                self.log("command length incorrect")
            else:
                data = data[1].rsplit(" ", 1)
            if len(data) == 2:
                data[0] += "" if data[1] == _("Success") else ":fail"
            if data[0] in Manager.SkillManager:
                return self.use_skill(Manager.SkillManager[data[0]])
            else:
                return "unknown skill %s" % data[0]
        elif data[0] == 'end':
            return self.end_round()
        else:
            self.log("Unknown command:", data[0])
            return None

    def start_round(self):
        self.reset()
        if self.use_memFix:
            self.memFixer.fix_crafter(self.player)
        self.status = Status(
            self.player, self.target,
            Manager.BallManager.defaultBall
        )
        self.round_history = [[None, type(self.status.ball).__name__]]
        self.start = time.perf_counter()
        self.start_time_stamp = int(time.time())
        print_status(self.status)
        return self.deal(self.status)

    def use_skill(self, skill):
        if self.status is not None:
            self.log("use skill %s" % skill.name)
            self.round_history[-1][0] = skill.name
            self.status = self.status.use_skill(skill)
            if not self.status.is_finish():
                time.sleep(0.5)
                self.status.ball = self.update_ball()
                if self.use_memFix:
                    self.memFixer.fix_status(self.status)
                self.round_history.append([None, type(self.status.ball).__name__])
                print_status(self.status)
                return self.deal(self.status, skill)
            return None

    def end_round(self):
        if self.use_log and self.round_history and self.status is not None:
            with open(self.log_path, "a+") as f:
                f.write(str(self.start_time_stamp) + '|')
                f.write('|'.join('%s;%s' % (i[0], i[1]) for i in self.round_history))
                f.write('|%s|%s|%s\n' % (self.status.currentProgress, self.status.currentQuality, time.perf_counter() - self.start))
        print("#" * 10 + "end" + "#" * 10)


    def reset(self):
        for stage in self.Stages:
            stage.reset()
        self.round_history = list()
        self.status = None
        self.start = 0
        self.start_time_stamp = 0
        self.terminate = False
        self.on_stage = 0

    def deal(self, status, prev_skill=None):
        if self.terminate:
            ans= self.terminator.deal(status)
        else:
            ans = None
            while len(self.Stages) > self.on_stage:
                if self.Stages[self.on_stage].is_finished(status, prev_skill):
                    self.log("Deal Next Stage")
                    self.on_stage += 1
                else:
                    ans = self.Stages[self.on_stage].deal(status, prev_skill)
                    break
            if ans == 'terminate' and self.use_terminator:
                self.terminate = True
                ans = self.terminator.deal(status)
        if ans is not None:
            self.log("recommend:", ans)
            if self.recall is not None:self.recall(ans)
            TTS(ans)
        else:
            print("no recommend")
        return ans
