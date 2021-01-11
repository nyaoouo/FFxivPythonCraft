from core.Simulator.Status import Status


def print_status(status: Status):
    print("#" * 10 + "r %s" % status.rounds + "#" * 10)
    print("ball:\t{}".format(status.ball.name))
    print("durability:\t{}/{}".format(status.currentDurability, status.target.maxDurability))
    print("progress:\t{}/{}".format(status.currentProgress, status.target.maxProgress))
    print("quality:\t{}/{}".format(status.currentQuality, status.target.maxQuality))
    if status.buffs: print("buffs:", " ".join([str(buff) for buff in status.buffs.values()]))
    print("CP:\t{}/{}".format(status.currentCp, status.player.maxCp))
