import win32com.client
from core.Utils.Config import config
from .Logger import Logger
speaker = win32com.client.Dispatch("SAPI.SpVoice")
try:
    whitelist=set(config.try_get('TTS','whitelist').split("|"))
    Logger("Load White list:"+str(whitelist),tag="TTS")
except:
    whitelist=None

def TTS(string: str):
    if config['TTS']['open'] == "True":
        if whitelist is None or string in whitelist:
            speaker.Speak(string)
