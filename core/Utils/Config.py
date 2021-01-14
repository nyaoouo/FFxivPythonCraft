import sys
from os import path
from .configparserNoLower import ConfigParser

filename = "config.ini"


class _config(object):
    def __init__(self, name):
        self.BasePath = path.dirname(sys.argv[0])
        configPath = path.join(self.BasePath, name)
        if not path.exists(configPath):
            raise Exception(configPath+" not found")
        self.configparser = ConfigParser()
        self.configparser.read(configPath, encoding='utf-8')

    def get(self, section: str, key: str, default=None, require=False):
        if section in self.configparser.sections() and key in self[section]:
            return self[section][key]
        elif require:
            raise Exception("%s-%s not found in config" % (section, key))
        else:
            return default

    try_get = get

    def __getitem__(self, key):
        return self.configparser[key]


config = _config(filename)
