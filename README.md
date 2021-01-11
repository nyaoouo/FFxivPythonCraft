高难外置思考回路
====

注意
----
> * 使用本工具有导致账号遭封禁的风险
> * ~~本来想写两点可是通宵太累忘了~~
> * 记起来了，本工具处于迭代期，任何奇奇怪怪的bug都有可能出现，欢迎提issue也欢迎提意见 ~~最好空降生产算法双料大佬帮忙写手法~~，请尽量保持更新

功能
----
> * python实现的生产模拟器
> * 一个用作模拟器demo的高难手法


适用范围
----
>内置手法配合 [nga月下大佬的攻略](https://ngabbs.com/read.php?pid=348434012) 进行
<br>有能力可以自己进行修改Solver模块

环境
----
>需求ACT
>- ACT需求插件：鲶鱼精邮差，triggernometry

>需求python
>- 内存读球需要x64环境，admin权限
>- python 需求库：看requirement.txt

食用方式
----
>- triggernometry导入TriggernometryExport.xml
>- 启动main.py
>- 请在游戏“消息过滤”内——“战斗”类勾选“自己的技能”以及“通知”类勾选“自己的制作信息”
>- 预先把生产面板恢复默认位置（不能遮盖球的范围)(ocr读球适用)
>- 开始生产，将自动执行（ ~~如果tts报terminate就是建议倒掉，不过可以试试手动救~~ ~~自毁模式，自动连刷高速/仓促~~ 好吧恢复了tts报terminate）
>- triggernometry将产生当前建议日志行——格式：@pythonCraft res [技能、建议]

config文件的一些项目
----
> * server
>   - hostName：监听地址
>   - port：监听端口
> * player
>   - lv：玩家等级
>   - craft：玩家作业精度
>   - control：玩家加工精度
>   - cp：玩家制作力上限
> * target
>   - rlv：配方等级
>   - Durability：配方耐久
>   - Progress：配方进度
>   - Quality：配方品质
> * Namazu
>   - hostName:鲶鱼精地址
>   - port:鲶鱼精端口
> * ball
>   - type:可选 memory / ocr / input
> * TTS
>   - open:可以关掉烦人的TTS
> * MemoryFixStatus
>   - open:是否启用内存纠错（包括角色三围，生产模拟的问题）

Reference:
----
>[[5.x][制造][采集]制造采集属性相关机制分享/探讨(5.2修订版)](https://ngabbs.com/read.php?tid=18839082)


声明
-----
>本工具仅作学习用途，bla bla bla bla，别拿来做坏事.jpg
