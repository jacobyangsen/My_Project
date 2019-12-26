from rest_framework import serializers
from .models import UserCoupon,Coupon

class CouponModelSerializer(serializers.ModelSerializer):
    """优惠券序列化器"""
    class Meta:
        model = Coupon
        fields = ["name","coupon_type","duration","condition","sale"]

class UserCouponModelSerializer(serializers.ModelSerializer):
    """我的优惠券序列化器"""
    coupon = CouponModelSerializer()
    class Meta:
        model = UserCoupon
        fields = ["id","start_time","coupon"]