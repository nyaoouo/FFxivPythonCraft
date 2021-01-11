from core.Simulator.Status import Status
from core.Simulator.Role import Crafter, Target
from core.Simulator.Manager import BallManager, SkillManager, BuffManager
import traceback
import time

from core.Utils.Logger import Logger

durReq = 21
cpReq = 131
AllowBuffs = {
    '阔步': '阔步',
    '改革': '改革',
    '俭约': '俭约',
    #'长期俭约': '俭约',
}
AllowSkillSet = {
    '坯料加工',
    '集中加工',
    '俭约加工',
}
Prequeue=[]

def allowSkills(status: Status):
    remainCp = status.currentCp - cpReq
    ans = list()
    if remainCp<0:return ans
    if remainCp >= SkillManager.getCp('精修', status) and status.target.maxDurability- status.currentDurability>=30:
        ans.append(['精修'])
    #if remainCp >= SkillManager.getCp('掌握', status):
    #    ans.append(['掌握'])
    if status.ball==BallManager.RedBall:
        ans.append(['秘诀'])
    for buff in AllowBuffs:
        if not status.has_buff(buff) and remainCp >= SkillManager.getCp(buff, status):
            ans.append([buff])
    if ['改革'] not in ans:
        for skill in AllowSkillSet:
            if status.currentDurability > SkillManager.getDurability(skill, status) and remainCp >= SkillManager.getCp(skill, status) and SkillManager[skill].can_use(status):
                ans.append([skill])
        if remainCp >= 25 and status.currentDurability >= 10:
            ans.append(['观察', '注视加工'])
    return ans


def init(player: Crafter, target: Target):
    pass


def solve(status: Status):
    print(Prequeue)
    return Prequeue.pop(0)

def try_solve(status: Status,timeLimit=None):
    best=None
    queue=[[status,[]]]
    Logger.hideTag("Math")
    record=set()
    start=time.perf_counter()
    while queue:
        if timeLimit is not None and time.perf_counter()-start > timeLimit:
            Logger.showTag("Math")
            return best
        tempData=queue.pop(0)
        allow=allowSkills(tempData[0])
        for skills in allow:
            tempStats=tempData[0]
            for i,skill in enumerate(skills):
                tempStats=tempStats.use_skill(SkillManager[skill])
                if tempStats.ball!=BallManager.WhiteBall:tempStats.ball=BallManager.WhiteBall
            if tempStats.get_status_string() not in record:
                record.add(tempStats.get_status_string())
                newData = [tempStats,tempData[1]+skills]
                if tempStats.currentDurability>durReq and(best is None or tempStats.currentQuality>best[0].currentQuality):
                    for s in newData[1]:
                        if s not in AllowBuffs:
                            best=newData
                            break
                queue.append(newData)
    Logger.showTag("Math")
    return best



def is_finished(status: Status):
    global Prequeue
    if not bool(Prequeue) or status.ball!=BallManager.WhiteBall:
        start=time.perf_counter()
        ans=try_solve(status,5)
        if ans:
            Prequeue = ans[1]
            Logger("new plan in {:.2f}s:{}({})".format(time.perf_counter()-start,Prequeue,ans[0].currentQuality),tag="stage_3")
    return not bool(Prequeue)


def reset():
    Prequeue.clear()
