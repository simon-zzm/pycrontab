pycrontab
=========
　　当前使用tornado框架，但是系统里有很多需要定时执行的报表，为了系统迁移方便，并且定时任务随web启停，系统的Crontab不能满足需求。
　　通过网上查找，虽然python里有sched模块和第三方apsched，但是感觉不能满足当前需要。自己动手写一个类似crontab。
　　代码如下，功能基本和语法与系统crontab相似，只是处理方式不同，我命名为pycrontab.py。处理到秒怕精度不够，所以也只是到分。有需要的自行修改。
　　最后用tornado框架的callback机制定时调用pycrontab.py处理。
http://www.simonzhang.net/?p=2479
