from pymem import Pymem
from .Config import config
from .Logger import Logger
from core.Simulator.Status import Status
from core.Simulator.Manager import BallManager
from core.Simulator.Role import Crafter
from core.Utils.SetAdmin import check
from .i18n import get_client_offset

check()
config_section_name = 'FFxivMemory'
client_offset = get_client_offset()


def log(msg):
    Logger(msg, tag="FFxivMem")


def get_config_hex(key: str):
    temp = config.try_get(config_section_name, key)
    if temp is None: return None
    log("Load config:" + key)
    return int(temp.lstrip('0x'), 16)


hs2int = lambda x: int(x.lstrip('0x'), 16)


def get_value(addr, length):
    return int.from_bytes(pm.read_bytes(addr, length), byteorder='little')


pid = config.try_get(config_section_name, 'application_pid')
if pid is not None:
    pm = Pymem()
    log("Load config:" + 'application_pid')
    pm.open_process_from_id(int(pid))
else:
    pm = Pymem(config.try_get(config_section_name, 'application_name') or 'ffxiv_dx11.exe')
'''
progress_offset = get_config_hex('current_progress') or 0x1D51C8C
cp_offset = get_config_hex('player_cp') or 0x1D307B4
actor_table_offset = get_config_hex('actor_table') or 0x1d2cf20
'''

progress_offset = hs2int(client_offset['CurrentProgress'])
cp_offset = hs2int(client_offset['MaxCp'])
actor_table_offset = hs2int(client_offset['ActorTable'])
cProgress_adr = pm.process_base.lpBaseOfDll + progress_offset
cQuality_adr = cProgress_adr + 0x8
cDurability_adr = cProgress_adr + 0x14
# rounds_adr = cProgress_adr - 0x4
ball_adr = cProgress_adr + 0x1c
mCp_adr = pm.process_base.lpBaseOfDll + cp_offset
lv_adr = mCp_adr - 0x114
craft_adr = mCp_adr + 0xec
control_adr = mCp_adr + 0xf0
actor_table_adr = pm.process_base.lpBaseOfDll + actor_table_offset


def _(adr, len=4):
    return lambda: get_value(adr, len)


ballColor = {
    0: "defaultBall",
    1: "WhiteBall",
    2: "RedBall",
    3: "RainbowBall",
    4: "BlackBall",
    5: "YellowBall",
    6: "BlueBall",
    7: "GreenBall",
    8: "DeepBlueBall",
    9: "PurpleBall",
}

currentProgress = _(cProgress_adr)
currentQuality = _(cQuality_adr)
currentDurability = _(cDurability_adr)
# rounds = _(rounds_adr,1)
ball = lambda: getattr(BallManager, ballColor[(get_value(ball_adr, 1))])
maxCp = _(mCp_adr)
lv = _(lv_adr, 2)
craft = _(craft_adr)
control = _(control_adr)
currentCp = lambda: get_value(get_value(actor_table_adr, 8) + 0x18AE, 2)


def fix_crafter(crafter: Crafter):
    if crafter.lv != lv():
        log("Player Lv incorrect")
        crafter.update(lv=lv())
    if crafter.craft != craft():
        log("Player craft {} incorrect, set {}".format(crafter.craft, craft()))
        crafter.update(craft=craft())
    if crafter.control != control():
        log("Player control {} incorrect, srt {}".format(crafter.control, control()))
        crafter.update(control=control())
    if crafter.maxCp != maxCp():
        log("Player max cp {} incorrect, set {}".format(crafter.maxCp, maxCp()))
        crafter.update(maxCp=maxCp())


def fix_status(status: Status):
    if status.currentDurability != currentDurability():
        log("Fix status current durability {} -> {}".format(status.currentDurability, currentDurability()))
        status.currentDurability = currentDurability()
    if status.currentProgress != currentProgress():
        log("Fix status current progress {} -> {}".format(status.currentProgress, currentProgress()))
        status.currentProgress = currentProgress()
    if status.currentQuality != currentQuality():
        log("Fix status current quality {} -> {}".format(status.currentQuality, currentQuality()))
        status.currentQuality = currentQuality()
    if status.ball != ball():
        log("Fix status ball {} -> {}".format(status.ball.name, ball().name))
        status.ball = ball()
    if status.currentCp != currentCp():
        log("Fix status current cp {} -> {}".format(status.currentCp, currentCp()))
        status.currentCp = currentCp()
