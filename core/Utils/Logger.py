class _Logger(object):
    DEBUG = 0
    INFO = 1
    WARNING = 2

    def __init__(self, ):
        self.tags = dict()
        self.lv = 0

    def __call__(self, msg, *msgs, lv=0, tag=None):
        if lv < self.lv or (tag is not None and tag in self.tags and not self.tags[tag]): return
        msg=str(msg)
        if msgs:msg+="\t"+"\t".join([str(msg) for msg in msgs])
        print("[{}]\t{}".format(tag, msg))

    def showTag(self, tag):
        self.tags[tag] = True

    def hideTag(self, tag):
        self.tags[tag] = False


Logger = _Logger()
