from rest_framework.views import APIView
from rest_framework.response import Response
from luffyapi.libs.geetest import GeetestLib
from django.conf import settings

# Create your views here.
class CaptchaAPIView(APIView):
    """验证码接口"""
    def get(self,request):
        """提供生成验证码流水号"""
        user_id = 'test'
        gt = GeetestLib(settings.GEETEST["pc_geetest_id"], settings.GEETEST["pc_geetest_key"])
        status = gt.pre_process(user_id)
        # request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self,request):
        """二次验证"""
        gt = GeetestLib(settings.GEETEST["pc_geetest_id"], settings.GEETEST["pc_geetest_key"])
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        # if status:
        #     result = gt.success_validate(challenge, validate, seccode, user_id)
        # else:
        result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        # if result:
        #     result = {"status": "success"}
        # else:
        #     result = {"status": "fail"}
        return Response(result)


from .models import User
from rest_framework import status
class MobileAPIView(APIView):
    """手机号验证接口"""
    def get(self,request,mobile):
        """验证手机号是否已经被注册了
        url: /users/mobile/(?P<mobile>1[3-9]\d{9})/
        """
        try:
            # 查询出来结果有用户，在表示已经被注册了
            User.objects.get(mobile=mobile)
            return Response({"status":False,"message":"当前手机号已经被注册了"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"status":True})


import random
from luffyapi.settings import constants
class SMSAPIView(APIView):
    """短信接口API"""
    def get(self,request,mobile):
        """发送短信"""
        # 验证码手机号的有效性
        try:
            User.objects.get(mobile=mobile)
            return Response({"status": False, "message": "当前手机号已经被注册了"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("sms_code")

        # 验证短信的发送时间是否超过了1分钟，1分钟内只能发送一次
        if redis_conn.get("sms_interval_%s" % mobile):
            return Response({"status": False, "message": "请勿频繁发送短信！"},status=status.HTTP_400_BAD_REQUEST)

        # 使用随机数生成验证码，不足6位数字的，使用字符串格式化，在数字左边补充"0"
        sms_code = "%06d" % random.randint(1000, 999999)

        # 把验证码保存到redis
        pipe = redis_conn.pipeline() # 创建管道对象
        pipe.multi() # 开启事务
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code )
        pipe.setex("sms_interval_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")
        pipe.execute() # 执行管道中所有的命令

        # 调用celery执行异步任务
        from my_celery.sms.tasks import send_sms
        send_sms.delay(mobile,sms_code)

        return Response({"status": True})

from rest_framework.generics import CreateAPIView
from .serializers import UserModelSerializer
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer