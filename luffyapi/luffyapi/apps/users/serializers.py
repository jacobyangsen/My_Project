from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
import logging

log = logging.getLogger("django")

class UserModelSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(max_length=6, min_length=4, write_only=True, help_text="短信验证码")
    token = serializers.CharField(max_length=1000, read_only=True, help_text="token令牌")
    class Meta:
        model = User
        fields = ["mobile", "password","sms_code","token","id","username"]
        extra_kwargs = {
            "mobile":{ "write_only": True, },
            "password":{ "write_only": True, },
            "id":{ "read_only": True, },
            "username":{ "read_only": True, }
        }


    def validate(self, attrs):
        """验证数据"""
        # 验证手机号是否格式正确
        mobile = attrs.get("mobile")
        if not re.match("^1[3-9]\d{9}$", mobile):
           return serializers.ValidationError("对不起，手机号码格式不正确！")

        # 验证手机号是否被注册了
        try:
            User.objects.get(mobile=mobile)
            return serializers.ValidationError("对不起，手机号码已经被注册了！")
        except User.DoesNotExist:
            pass

        # 作业： 验证密码的长度，必须时6-16位字符

        # 验证手机短信验证码是否过期了或者错误
        sms_code = attrs.get("sms_code")
        redis_conn = get_redis_connection("sms_code")
        code_bytes = redis_conn.get("sms_%s" % mobile)
        if not code_bytes or code_bytes.decode() != sms_code:
            """如果redis不存在对应手机的短信验证码或者提取出来的短信验证码双方不一致都是验证失败"""
            return serializers.ValidationError("对不起，验证码过期或错误！")

        # 删除短信验证码的记录
        redis_conn.delete("sms_%s" % mobile)

        return attrs

    def create(self, validated_data):
        """添加用户数据"""
        # 移除客户端提交过来的短信验证码的信息
        del validated_data["sms_code"]

        # 对数据进行保存和完成密码加密
        try:
            validated_data["username"] = validated_data["mobile"]
            # 添加用户信息
            user = super().create(validated_data=validated_data)
            # 更新密码
            user.set_password(validated_data.get("password"))
            user.save()
        except:
            log.error("用户注册信息保存失败！")
            return serializers.ValidationError("对不起，用户注册保存信息失败！请联系客服工作人员")

        # 在添加用户成功以后，需要保存登录状态返回给客户端[实现注册免登录]
        # 使用restframework_jwt提供的代码 生成token
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        # 把token返回给客户端
        return user