from rest_framework import serializers
from .models import Order,OrderDetail
from datetime import datetime
import random
from django.db import transaction
from django_redis import get_redis_connection
from courses.models import Course

class OrderModelSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    class Meta:
        model = Order
        fields = [
            "id","order_title",
            "total_price","real_price","order_number","order_status",
            "pay_type","pay_time",
            "credit","coupon",
        ]
        extra_kwargs = {
            "id":{ "read_only":True,},
            "order_title":{"read_only":True,},
            "total_price":{"read_only":True,},
            "real_price":{"read_only":True,},
            "order_number":{"read_only":True,},
            "order_status":{"read_only":True,},
            "pay_time":{"read_only":True,},
            "pay_type":{"required":True,},
            "credit":{"required":True,"min_value":0},
            "coupon":{"required":True,"min_value":0},
        }

    def create(self, validated_data):
        """生成订单"""
        # 接受客户端提交的数据
        pay_type = validated_data.get("pay_type")
        credit = validated_data.get("credit", 0)
        coupon = validated_data.get("coupon", 0)

        #  生成必要参数
        user_id = self.context["request"].user.id # 获取来自于视图的request对象，通过request对象获取本次操作的用户id
        order_title = "路飞学城课程购买"
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%06d" % user_id) + ("%04d" % random.randint(0, 9999))
        order_status = 0


        # 积分数额的判断

        # 优惠券的可用性和启用时间进行判断

        with transaction.atomic():
            # 设置事务回滚点
            sid = transaction.savepoint()

            # 保存订单基本信息
            order = Order.objects.create(**{
                "order_title": order_title,
                "total_price": 0, # 订单总价格
                "real_price": 0,  # 实付价格
                "order_number": order_number,
                "order_status": order_status,
                "pay_type": pay_type,
                "credit": credit,
                "coupon": coupon,
                "order_desc": "",
                "user_id": user_id,
            })

            # 保存订单相关商品信息
            redis_conn = get_redis_connection("cart")
            # 从购物车中提取勾选的商品信息
            cart_list = redis_conn.hgetall("cart_%s" % user_id)
            course_set = redis_conn.smembers("selected_%s" % user_id)
            if course_set is None:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError("对不起，购物车中没有商品，赶紧去买买买！")

            # 订单总价，默认为0，在循环中逐个加上课程的价格
            total_price = 0

            # 开启redis的事务操作[管道操作]
            pipe = redis_conn.pipeline()
            pipe.multi()

            for course_id_bytes in course_set:
                """在循环中把每一个勾选商品同步到订单详情记录中"""
                course_expire_bytes = cart_list[course_id_bytes]
                expire = course_expire_bytes.decode()
                course_id = int( course_id_bytes.decode() )

                try:
                    course = Course.objects.get(pk=course_id)
                except:
                    transaction.savepoint_rollback(sid)
                    raise serializers.ValidationError("对不起，商品课程不存在！")

                # 提取课程的有效期选项对应的原价
                if int(expire) > 0:
                    course_expire = course.courseexpire.get(timer=expire)
                    price = course_expire.price
                    expire_time = course_expire.timer
                else:
                    price = course.price
                    expire_time = 0

                # 保存商品信息到OrderDetail中
                from decimal import Decimal
                try:
                    order_detail = OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire= int(expire_time), # 有效期选项的时间
                        price = Decimal(price),
                        real_price = Decimal( course.discount_price(price) ),
                        discount_name = course.discount_name,
                    )

                except:
                    transaction.savepoint_rollback(sid)
                    raise serializers.ValidationError("生成订单失败！")

                # 计算订单总价
                total_price += order_detail.real_price

                # 从购物车中删除订单对应的商品
                pipe.hdel("cart_%s" % user_id, course.id)
                pipe.srem("selected_%s" % user_id, course.id)


            try:
                # 保存总价到数据库中
                order.total_price = total_price
                # 将来这里补充关于积分和优惠券的处理
                # 处理优惠券
                from coupon.models import UserCoupon
                coupon_money = 0
                if coupon > 0:
                    userCoupon = UserCoupon.objects.get(is_delete=False,is_use=False, is_show=True, pk=coupon)
                    if userCoupon.coupon.coupon_type == 1:
                        """减免优惠"""
                        coupon_money = float(userCoupon.coupon.sale[1:])
                    elif userCoupon.coupon.coupon_type == 2:
                        """折扣优惠"""
                        coupon_money = float(total_price) * (1-float(userCoupon.coupon.sale[1:]))
                        print(total_price)
                # 处理积分
                from luffyapi.settings import constants
                credit_money = int(credit) / constants.RMB_CREDIT

                # 实付总价= 订单商品总价 - 优惠券抵扣金额 - 积分抵扣金额
                order.real_price = float(total_price) - coupon_money - credit_money

                if order.real_price >= 0:
                    # 扣除积分
                    if credit > 0:
                        user = self.context["request"].user
                        user.credit -= credit
                        user.save()

                    # 修改对应优惠券的使用状态
                    if coupon > 0:
                        userCoupon.is_use = True
                        userCoupon.save()

                    order.save()

                    # 执行redis的管道操作
                    pipe.execute()
                else:
                    raise serializers.ValidationError()
            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError("生成订单失败！")

        return order


"""会员订单"""
from orders.models import Order,OrderDetail
from courses.serializers import CourseRetrieveModelSerializer
class CourseModelSerializer(serializers.ModelSerializer):
    """课程详情"""
    class Meta:
        model = Course
        fields = ["id", "name", "course_img"]

class OrderDetailListModelSerializer(serializers.ModelSerializer):
    course = CourseModelSerializer()
    class Meta:
        model = OrderDetail
        fields = ("price","real_price","discount_name","expire_text","course")

class OrderListModelSerializer(serializers.ModelSerializer):
    order_courses = OrderDetailListModelSerializer(many=True)
    class Meta:
        model = Order
        fields = ("id","create_time","pay_time","order_number","real_price","total_price","order_status","order_status_text","pay_type","order_courses")