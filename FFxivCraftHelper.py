# -*- coding=utf-8 -*-

from solver_v2.Solver import Solver
from core.Utils.HttpServer import Server
from core.Utils.Config import config
import traceback
import atexit

atexit.register(input, "<<press enter to exit>>")
try:
    Server(
        config['server']['hostName'],
        int(config['server']['port']),
        Solver()
    ).start()
except:
    traceback.print_exc()
