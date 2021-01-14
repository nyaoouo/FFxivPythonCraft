from core.Utils.Config import config

t = config.get('ball', 'type', default="input")
if t == "memory":
    from . import Memory

    c = Memory
elif t == "ocr":
    from . import Ocr

    c = Ocr
elif t == "input":
    from . import Input

    c = Input
else:
    raise Exception("Unknown ball geter type:" + t)


def get_ball():
    return c.get_ball()
