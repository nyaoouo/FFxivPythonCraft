from core.Simulator.Manager import BallManager

def get_ball():
    data = {
        "white": BallManager.WhiteBall,
        "yellow": BallManager.YellowBall,
        "red": BallManager.RedBall,
        "green": BallManager.GreenBall,
        "blue": BallManager.BlueBall,
        "rainbow": BallManager.RainbowBall,
        "black": BallManager.BlackBall
    }
    temp=None
    while temp not in data:
        print("please input the color")
        temp = input(">>").lower()
    return data[temp]
