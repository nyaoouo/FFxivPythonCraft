from PIL import ImageGrab
from core.Simulator.Manager import BallManager
def color_lv(n):
    return 2 if n > 200 else 1 if n > 100 else 0

def get_color(red, green, blue):
    temp = color_lv(red) * 100 + color_lv(green) * 10 + color_lv(blue)
    if temp == 222:
        return BallManager.WhiteBall
    elif temp == 221:
        return BallManager.YellowBall
    elif temp == 211:
        return BallManager.RedBall
    elif temp == 10 or temp == 20:
        return BallManager.GreenBall
    elif temp == 12 or temp == 22:
        return BallManager.BlueBall
    else:
        raise Exception("Unknown color")


def get_ball():
    return get_color(*get_pixel(65, 302))

def get_pixel(x,y):
    return ImageGrab.grab(bbox=(x,y,x+1,y+1)).load()[0,0]


if __name__ == "__main__":
    import time
    BallManager.load()
    while True:
        print(get_pixel(65, 302),get_ball().name)
        time.sleep(0.5)
