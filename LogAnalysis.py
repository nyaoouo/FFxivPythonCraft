from os import path
import atexit
from datetime import datetime
import math
atexit.register(input,"<<press enter to exit>>")
if not path.exists("log.txt"):
    print("logs file does not exist")
    exit()
data=[line.strip().split('|') for line in open("log.txt").readlines()]
data=[[int(i[0]),float(i[-1]),int(i[-3]),int(i[-2]),i[1:-3]] for i in data]
print("first record at:",datetime.fromtimestamp(data[0][0]),end="\t")
print("last record at:",datetime.fromtimestamp(data[-1][0]))
df=[d for d in data if d[2] < 11126]
d0=[d for d in data if d[2] == 11126 and d[3] < 58000]
d1=[d for d in data if d[2] == 11126 and 58000 <= d[3] < 65000]
d2=[d for d in data if d[2] == 11126 and 65000 <= d[3] < 77000]
d3=[d for d in data if d[2] == 11126 and 77000 <= d[3]]
name=["all","failed","zero","one","two","three"]
for i,d in enumerate((data,df,d0,d1,d2,d3)):
    if d:
        print("Record lv:",name[i])
        print("\tcount:{}".format(str(len(d)).zfill(2)),end="\t")
        print("average time:{}s".format(int(sum([d[1] for d in d])/len(d))),end="\t")
        print("max time:{}s".format(int(max(d[1]for d in d))),end="\t")
        print("averge quality:{}".format(int(sum([d[3] for d in d])/len(d))))
        skillTemp=dict()
        for skill in ['高速制作','专心加工']:
            skillTemp[skill]=sum(len([s for s in d[4] if s.split(';')[0]==skill]) for d in d)
            sf=skill+':fail'
            skillTemp[sf]=sum(len([s for s in d[4] if s.split(';')[0]==sf]) for d in d)
            total=skillTemp[skill]+skillTemp[sf]
            if total>0:print("\t{}\tcount：{}\tsuccess rate：{}%".format(skill,total,int(skillTemp[skill]*100/total)))
print("base efficiency(per hour):", int(((len(d1) * 175 + len(d2) * 370 + len(d3) * 1100) / sum([d[1] for d in data])) * 3600))
