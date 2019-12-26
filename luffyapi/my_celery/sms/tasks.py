from my_celery.main import app
from .yuntongxun.sms import CCP
from luffyapi.settings import constants
import logging

log = logging.getLogger("django")

# @app.task(name="send_sms")
# def send_sms(mobile):
#     print("发送短信给%s的异步任务执行了" % mobile)
#     return "任务结果！"


@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    """异步发送短信"""
    ccp = CCP()
    try:
        result = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME//60 ], constants.SMS_TEMPLATE_ID)
        return result
    except:
        log.error("发送短信验证码失败！手机号：%s" % mobile)

