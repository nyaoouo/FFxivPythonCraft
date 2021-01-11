from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Manager import SkillManager, BuffManager, BallManager
from solver.Solver import format_status,solver

for manager in [SkillManager, BuffManager, BallManager]: manager.load()
player = Crafter(80, 2758, 2917, 657)
target = Target(511, 50, 11126, 82400)
status = Status(player, target, BallManager.defaultBall)
status.ball=BallManager.RedBall
q=[["\u95f2\u9759", "WhiteBall"], ["\u5d07\u656c", "WhiteBall"], ["\u9ad8\u901f\u5236\u4f5c", "BlueBall"], ["\u638c\u63e1", "GreenBall"], ["\u9ad8\u901f\u5236\u4f5c:fail", "GreenBall"], ["\u9ad8\u901f\u5236\u4f5c:fail", "GreenBall"], ["\u5d07\u656c", "WhiteBall"], ["\u9ad8\u901f\u5236\u4f5c:fail", "GreenBall"], ["\u9ad8\u901f\u5236\u4f5c", "WhiteBall"], ["\u9ad8\u901f\u5236\u4f5c", "WhiteBall"], ["\u7cbe\u4fee", "BlueBall"], ["\u4e13\u5fc3\u52a0\u5de5", "WhiteBall"], ["\u4fed\u7ea6\u52a0\u5de5", "WhiteBall"], ["\u638c\u63e1", "GreenBall"], ["\u4fed\u7ea6\u52a0\u5de5", "GreenBall"], ["\u4fed\u7ea6\u52a0\u5de5", "GreenBall"], ["\u4fed\u7ea6", "GreenBall"], ["\u6539\u9769", "YellowBall"], ["\u576f\u6599\u52a0\u5de5", "YellowBall"], ["\u576f\u6599\u52a0\u5de5", "BlueBall"], ["\u89c2\u5bdf", "BlueBall"], ["\u576f\u6599\u52a0\u5de5", "BlueBall"], ["\u6539\u9769", "WhiteBall"], ["\u89c2\u5bdf", "WhiteBall"], ["\u6ce8\u89c6\u52a0\u5de5", "WhiteBall"], ["\u79d8\u8bc0", "RedBall"], ["\u4fed\u7ea6\u52a0\u5de5", "YellowBall"], ["\u79d8\u8bc0", "RedBall"], ["\u9614\u6b65", "YellowBall"], ["\u6539\u9769", "RedBall"], ["\u89c2\u5bdf", "GreenBall"], ["\u6ce8\u89c6\u52a0\u5de5", "WhiteBall"], ["\u9614\u6b65", "WhiteBall"], ["\u6bd4\u5c14\u683c\u7684\u795d\u798f", "RedBall"], ["\u5236\u4f5c", "GreenBall"]]
solver("start")
while q:
    action=q.pop(0)
    status.ball=getattr(BallManager,action[1])
    format_status(status)
    use = action[0]
    if use in SkillManager:
        print("use:", use)
        status = status.use_skill(SkillManager[use])
    else:
        print("invalid input")
format_status(status)
