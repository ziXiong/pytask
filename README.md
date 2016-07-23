PyTask
======
一个基于数据库的定时任务组件, 在指定的时间点执行任务, 超实用!!!  
不同于sched、schedule、crontab等执行`周期性任务`, pytask是执行`定时`任务。

## 安装

    pip install https://github.com/ziXiong/pytask.git@master#egg=pytask
或

    git clone https://github.com/ziXiong/pytask.git
    cd pytask & python setup.py install
  
## 原理简介
pytask把任务的执行时间和数据存储在数据库, 在另一个线程中循环地取出到时间的任务并执行。
执行一个任务需要两步:
* 注册任务
* 执行任务
  
## 使用

### 配置数据库, 初始化数据库(第一次使用时)
pytask依赖于SQLAchemy存储任务信息到数据库

```python
# 本地数据库, sqlchemy
sqlchemy_db = dict(
    drivername='mysql+mysqlconnector',
    host='localhost',
    username='root',
    password='rootmima',
    database='apphelper',
)
import pytask
pytask.conf(sqlchemy_db)

pytask.init_db()
```

### 注册任务
例如一个30分钟后订单过期的任务
```python
from pytask import TaskHandler, register_handler

class OrderTimeoutHandler(TaskHandler):
    def handle(self, task):
    ## do the timing task ##
    print(task)
    ... 
    
    def get_biz_code(self):
        return 'order_timeout'  # this code identify a task
        
register_handler(OrderTimeoutHandler)
```
biz_code标识了一个任务(业务码), 在添加任务时要填写相应的code, pytask才会找到handler.

### 添加任务

```python
import json
from datetime import datetime, timedelta
from pytask import add_task, Task

timeout_time = datetime.now() + timedelta(minutes=30)
data = dict()  # whatever data you need when calling handler.
add_task(Task(biz_code='order_timeout', when=timeout_time, biz_ext=json.dumps(data)))
```
添加一条任务, biz_code为任务的标识(业务码), 对应注册任务时的biz_code, when指定任务被执行的时间, biz_ext传入任务执行时需要的数据。


### 完成了~~
