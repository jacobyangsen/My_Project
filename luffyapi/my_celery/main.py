from celery import Celery

# 1. 注册和创建celery应用实例对象
app = Celery("luffy")

# 把celery和django组合使用，需要先对django进行初始化
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
import django
django.setup()

# 2. 加载配置信息
app.config_from_object("my_celery.config")

# 3. 注册任务模块
app.autodiscover_tasks(["my_celery.sms","my_celery.order"])

# 4. 启动celery即可
# 强烈建议切换目录到项目的根目录下启动celery!!
# celery -A my_celery.main worker --loglevel=info