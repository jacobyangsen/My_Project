# 任务队列的链接地址
broker_url = 'redis://127.0.0.1:6379/15'
# 结果队列的链接地址
result_backend = 'redis://127.0.0.1:6379/14'

# 定时任务
from celery.schedules import crontab
from .main import app
# 定时任务的调度列表，用于注册定时任务
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'check_order_outtime': {
        # 本次调度的任务
        'task': 'check_order', # 这里的任务名称必须先到main.py中注册
        # 定时任务的调度周期
        # 'schedule': crontab(minute=0, hour=0),   # 每周凌晨00:00
        # 'schedule': crontab(minute='*/15'),   # 每15分钟
        'schedule': crontab(),   # 每分钟
      	# 'args': (16, 16),  # 注意：任务就是一个函数，所以如果有参数则需要传递
    },
}