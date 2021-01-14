# -*- coding=utf-8 -*-

from solver_v2.Solver import Solver
from core.Utils.HttpServer import Server
from core.Utils.Config import config
import traceback
import atexit
from core.Utils.i18n import system_to_client_text as _
print(_('Success'))
atexit.register(input, "<<press enter to exit>>")
try:
    Server(
        config['server']['hostName'],
        int(config['server']['port']),
        Solver()
    ).start()
except:
    traceback.print_exc()
