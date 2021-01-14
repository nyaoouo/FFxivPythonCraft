from .Models import BallBase


class WhiteBall(BallBase):
    pass


class RedBall(BallBase):
    quality = 1.5


class BlueBall(BallBase):
    durability = 0.5


class GreenBall(BallBase):
    cp = 0.5


class YellowBall(BallBase):
    pass


class RainbowBall(BallBase):
    quality = 4


class BlackBall(BallBase):
    quality = 0.5


class DeepBlueBall(BallBase):
    progress = 1.5


class PurpleBall(BallBase):

    def after_use(self, status):
        for buff in status.buffsToAdd:
            buff.rounds *= 2


DefaultBall = WhiteBall()
