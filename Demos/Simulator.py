from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Manager import SkillManager, BuffManager, BallManager,managers_load

#加载技能，球色，buff的数据
managers_load()


#格式化列印status
def print_status(status: Status):
    print("#" * 10 + "r %s" % status.rounds + "#" * 10)
    print("ball:\t{}".format(status.ball.name))
    print("durability:\t{}/{}".format(status.currentDurability, status.target.maxDurability))
    print("progress:\t{}/{}".format(status.currentProgress, status.target.maxProgress))
    print("quality:\t{}/{}".format(status.currentQuality, status.target.maxQuality))
    if status.buffs: print("buffs:", " ".join([str(buff) for buff in status.buffs.values()]))
    print("CP:\t{}/{}".format(status.currentCp, status.player.maxCp))


#创建角色，对象实体
player = Crafter(80, 2758, 2917, 657)
target = Target(511, 50, 11126, 82400)

#创建status开局
status = Status(player, target, BallManager.defaultBall)

#一些直接修改局面属性的api
#注意：为了避免循环加载，或缺漏注入等情况，请不要直接import skills.py ball.py 等文件
#请使用manager相关
status.ball = BallManager.PurpleBall
status.get_buff(BuffManager.InnerQuiet)
status.execute_buff_change()
if status.has_buff('內静'):
    status.get_buff('內静').data['lv']=11

#使用use skill 创建下一回合的局面
next_status =status.use_skill(SkillManager['俭约'])

#格式化输出
print_status(next_status)
