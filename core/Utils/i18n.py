import sys
from os import path
from .Config import config
from.configparserNoLower import ConfigParser
from core.Simulator.Definitions import set_names

class _i18n(object):
    def __init__(self, name):
        self.BasePath = path.dirname(sys.argv[0])
        localizePath = path.join(self.BasePath, 'localize', name + '.ini')
        if not path.exists(localizePath):
            raise Exception(localizePath + " not found")
        self.configparser = ConfigParser()
        self.configparser.read(localizePath, encoding='utf-8')
        self.translateToSystem = {v: k for k, v in self.configparser['Translate'].items()}
        self.translateFromSystem = {k: v for k, v in self.configparser['Translate'].items()}


solver_localize = _i18n(config.get('I18N', 'Solver', default='cn'))
client_localize = _i18n(config.get('I18N', 'Client', default='cn'))
set_names(client_localize.translateFromSystem)

def get_client_offset():
    return {k:v for k,v in client_localize.configparser['Offset'].items()}

def system_to_client_text(text: str):
    if text in client_localize.translateFromSystem:
        return client_localize.translateFromSystem[text]
    else:
        return text


def client_to_system_text(text: str):
    if text in client_localize.translateToSystem:
        return client_localize.translateToSystem[text]
    else:
        return text

def solver_to_client_text(text: str):
    if text in solver_localize.translateToSystem:
        return system_to_client_text(solver_localize.translateToSystem[text])
    else:
        return text
