from rest_framework.views import APIView
from alipay import AliPay
from orders.models import Order
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime
from coupon.models import UserCoupon
from users.models import UserCourse
from django.http.response import HttpResponse

class AlipayAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """支付宝接口视图"""
    def get(self,request):
        """提供支付宝支付链接地址给客户端"""
        # 获取订单号
        order_number = request.query_params.get("order_number")
        # 判断订单是否存在
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message": "对不起，订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建支付宝应用对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug = settings.ALIAPY_CONFIG["debug"]  # 默认False
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG["return_url"],
            notify_url=settings.ALIAPY_CONFIG["notify_url"]  # 可选, 不填则使用默认notify url
        )

        # 拼接支付链接地址
        url = settings.ALIAPY_CONFIG["gateway_url"] + order_string

        return Response({"url":url})


class AlipayResultAPIView(APIView):

    def get(self,request):
        """支付宝的支付结果处理[同步通知]"""
        # 接受客户端转发过来的支付结果
        data = request.query_params.dict()
        # 提取签名
        signature = data.pop("sign")

        # 创建支付宝应用对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )

        success = alipay.verify(data,signature)

        if success:
            # 获取支付成功的结果中的订单号
            order_number = data.get("out_trade_no")
            try:
                order = Order.objects.get(order_number=order_number,order_status=0)
                user = order.user
            except Order.DoesNotExist:
                return Response({"message": "对不起，支付结果查询失败！订单不存在！请联系客服工作人员"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with transaction.atomic():
                # 事务回滚点
                save_id = transaction.savepoint()
                try:
                    # 修改订单状态和订单支付时间
                    order.pay_time = datetime.now()
                    order.order_status = 1
                    order.save()

                    # 优惠券处理
                    user_coupon_id = order.coupon
                    if user_coupon_id > 0:
                        user_coupon = UserCoupon.objects.get(pk=user_coupon_id, is_use=False, is_show=True,
                                                             is_deleted=False)
                        user_coupon.is_use = True
                        user_coupon.save()

                    # 积分处理
                    credit = order.credit
                    if credit > 0:
                        user.credit -= credit
                        user.save()

                        # 补充积分流水

                    # 记录用户成功购买课程的记录, 增加课程的购买人数
                    order_detail_list = order.order_courses.all()
                    # 返回给客户端的课程列表
                    course_data_list = []
                    for order_detail in order_detail_list:
                        """循环本次订单中所有购买的商品课程"""
                        course = order_detail.course
                        course.students += 1
                        course.save()

                        # 增加用户的课程购买记录
                        try:
                            # 查询之前有没有购买记录
                            user_course = UserCourse.objects.get(course=course, user=user)
                            # 之前购买过同一个课程
                            if user_course.out_time.timestamp() > datetime.now().timestamp():
                                """之前购买的课程没有过期，更新当前记录的过期时间[过期时间+本次购买的课程有效期]"""
                                """判断本次购买课程是购买一段时间还是永久购买"""
                                if order_detail.expire > 0:
                                    """有效期购买"""
                                    # 计算新的过期时间戳
                                    out_time = user_course.out_time.timestamp() + order_detail.expire * 24 * 60 * 60
                                    # 把时间戳转换成日期时间对象
                                    user_course.out_time = datetime.fromtimestamp(out_time)

                                else:
                                    """永久  购买"""
                                    user_course.out_time = "2199-01-01 00:00:00"
                            else:
                                """之前购买的课程已经过期，更新当前记录的过期时间[当前时间+本次购买的课程有效期]"""
                                if order_detail.expire > 0:
                                    """有效期购买"""
                                    out_time = datetime.now().timestamp() + order_detail.expire * 24 * 60 * 60
                                    user_course.out_time = datetime.fromtimestamp(out_time)
                                else:
                                    """永久  购买"""
                                    user_course.out_time = "2199-01-01 00:00:00"

                            user_course.trade_no = data.get("trade_no")
                            user_course.save()

                        except UserCourse.DoesNotExist:
                            """之前没有过同一个课程，则新增记录"""
                            if order_detail.expire > 0:
                                """有效期购买"""
                                out_time = datetime.now().timestamp() + order_detail.expire * 24 * 60 * 60
                            else:
                                """永久  购买"""
                                out_time = "2199-01-01 00:00:00"

                            UserCourse.objects.create(
                                user=user,
                                course=course,
                                trade_no=data.get("trade_no"),
                                buy_type=1,
                                pay_time=datetime.now(),
                                out_time=out_time
                            )

                        course_data_list.append({"course_id":course.id, "course_name": course.name})
                except:
                    transaction.savepoint_rollback(save_id)
                    return Response({"message": "参数无效！发生了未知错误！"})

            return Response({"pay_time": order.pay_time, "real_price":order.real_price, "course_data_list": course_data_list})

        return Response({"message":"参数无效！无法获取支付的结果！"})

    def post(self,request):
        """支付宝的支付结果处理[异步通知]"""
        """支付宝的支付结果处理[同步通知]"""
        # 接受客户端转发过来的支付结果
        data = request.data.dict()
        # 提取签名
        signature = data.pop("sign")

        # 创建支付宝应用对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_path=settings.ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )

        success = alipay.verify(data,signature)

        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
            # 获取支付成功的结果中的订单号
            order_number = data.get("out_trade_no")
            try:
                order = Order.objects.get(order_number=order_number,order_status=0)
                user = order.user
            except Order.DoesNotExist:
                return HttpResponse("success")

            with transaction.atomic():
                # 事务回滚点
                save_id = transaction.savepoint()
                try:
                    # 修改订单状态和订单支付时间
                    order.pay_time = datetime.now()
                    order.order_status = 1
                    order.save()

                    # 优惠券处理
                    user_coupon_id = order.coupon
                    if user_coupon_id > 0:
                        user_coupon = UserCoupon.objects.get(pk=user_coupon_id, is_use=False, is_show=True,
                                                             is_deleted=False)
                        user_coupon.is_use = True
                        user_coupon.save()

                    # 积分处理
                    credit = order.credit
                    if credit > 0:
                        user.credit -= credit
                        user.save()

                        # 补充积分流水

                    # 记录用户成功购买课程的记录, 增加课程的购买人数
                    order_detail_list = order.order_courses.all()
                    # 返回给客户端的课程列表
                    course_data_list = []
                    for order_detail in order_detail_list:
                        """循环本次订单中所有购买的商品课程"""
                        course = order_detail.course
                        course.students += 1
                        course.save()

                        # 增加用户的课程购买记录
                        try:
                            # 查询之前有没有购买记录
                            user_course = UserCourse.objects.get(course=course, user=user)
                            # 之前购买过同一个课程
                            if user_course.out_time.timestamp() > datetime.now().timestamp():
                                """之前购买的课程没有过期，更新当前记录的过期时间[过期时间+本次购买的课程有效期]"""
                                """判断本次购买课程是购买一段时间还是永久购买"""
                                if order_detail.expire > 0:
                                    """有效期购买"""
                                    # 计算新的过期时间戳
                                    out_time = user_course.out_time.timestamp() + order_detail.expire * 24 * 60 * 60
                                    # 把时间戳转换成日期时间对象
                                    user_course.out_time = datetime.fromtimestamp(out_time)

                                else:
                                    """永久  购买"""
                                    user_course.out_time = "2199-01-01 00:00:00"
                            else:
                                """之前购买的课程已经过期，更新当前记录的过期时间[当前时间+本次购买的课程有效期]"""
                                if order_detail.expire > 0:
                                    """有效期购买"""
                                    out_time = datetime.now().timestamp() + order_detail.expire * 24 * 60 * 60
                                    user_course.out_time = datetime.fromtimestamp(out_time)
                                else:
                                    """永久  购买"""
                                    user_course.out_time = "2199-01-01 00:00:00"

                            user_course.trade_no = data.get("trade_no")
                            user_course.save()

                        except UserCourse.DoesNotExist:
                            """之前没有过同一个课程，则新增记录"""
                            if order_detail.expire > 0:
                                """有效期购买"""
                                out_time = datetime.now().timestamp() + order_detail.expire * 24 * 60 * 60
                            else:
                                """永久  购买"""
                                out_time = "2199-01-01 00:00:00"

                            UserCourse.objects.create(
                                user=user,
                                course=course,
                                trade_no=data.get("trade_no"),
                                buy_type=1,
                                pay_time=datetime.now(),
                                out_time=out_time
                            )

                        course_data_list.append({"course_id":course.id, "course_name": course.name})
                except:
                    transaction.savepoint_rollback(save_id)
                    return Response({"message": "参数无效！发生了未知错误！"})

            # 告诉给支付，支付处理成功！
            return HttpResponse("success")

        return Response({"message":"参数无效！无法获取支付的结果！"})