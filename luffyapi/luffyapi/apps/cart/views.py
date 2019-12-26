from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from courses.models import Course
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection

class CartAPIViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]
    def add_cart(self,request):
        """添加商品到购物车"""
        # 获取用户ID
        user_id = request.user.id

        # 获取客户端发送过来的course_id
        course_id = request.data.get("course_id")

        # 验证课程是否存在
        try:
            Course.objects.get(pk=course_id, is_show=True, is_delete=False)
        except:
            return Response({"message":"对不起，添加的商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 设置有效期和勾选状态的默认值
        expire = 0 # 0表示没有设置默认值，或者将来我们完成课程的有效期时，重新定义0代表的意思。

        # 打开redis的链接
        redis_conn = get_redis_connection("cart")

        # 保存数据到redis中
        # 把商品ID和商品的有效期存放到hash中
        pipe = redis_conn.pipeline()
        pipe.multi()

        pipe.hset("cart_%s" % user_id, course_id, expire )
        pipe.sadd("selected_%s" % user_id, course_id ) # 默认勾选的状态，如果用户不希望将来这个商品进行结算状态，我们在购物车商品列表中提供按钮给用户去掉

        pipe.execute()

        # 返回响应结果
        return Response({"message":"成功添加商品到购物车"})

    def list(self, request):
        """购物车商品列表"""
        # 获取登录用户id
        user_id = request.user.id

        # 1. 打开redis链接
        redis_conn = get_redis_connection("cart")

        # 2. 从redis读取购物车信息[[id,course_img,name,price]]和勾选商品集合
        cart_dict_bytes = redis_conn.hgetall("cart_%s" % user_id)
        print(cart_dict_bytes) # {b'1': b'0', b'3': b'0', b'4': b'0'}

        selected_set_bytes = redis_conn.smembers("selected_%s" % user_id)

        # 3. 把勾选状态信息和商品信息组合成一个数据列表
        data = []
        for course_id_bytes, expire_bytes in cart_dict_bytes.items():
            course_id = course_id_bytes.decode()
            expire = expire_bytes.decode()
            try:
                course = Course.objects.get(pk=course_id, is_show=True, is_delete=False)
            except:
                course = None

            if course:
                data.append({
                    "course_id": course.id,
                    "course_name": course.name,
                    "course_img": course.course_img.url,
                    "price": course.discount_price( course.real_price(expire) ), # 真实价格
                    "expire": expire,  # 用户购物车中的有效期选项
                    "expire_list": course.expire_list, # 有效期选项列表
                    "selected": course_id_bytes in selected_set_bytes, # 勾选状态
                })

        # 4. 返回数据
        return Response(data)

    def change_select_status(self,request):
        """切换商品勾选状态"""
        # 获取用户ID
        # 获取登录用户id
        user_id = request.user.id
        # 获取客户端提交过来的勾选状态
        selected = request.data.get("selected")
        # 获取课程ID
        course_id = request.data.get("course_id")
        # 验证数据
        try:
            course = Course.objects.get(pk=course_id, is_show=True, is_delete=False)
        except:
            return Response({"message":"对不起，操作的商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 链接redis，修改指定商品的勾选状态
        redis_conn = get_redis_connection("cart")
        if selected:
            """添加商品的勾选状态"""
            redis_conn.sadd("selected_%s" % user_id, course_id)
        else:
            """移除商品的勾选状态"""
            redis_conn.srem("selected_%s" % user_id, course_id)

        # 返回响应结果
        return Response({"message":"切换勾选状态成功！"})

    def delete(self, request):
        """"删除购物车中的商品信息"""
        # 接受数据
        user_id = request.user.id
        course_id = request.query_params.get("course_id")

        # 验证数据
        try:
            course = Course.objects.get(pk=course_id, is_show=True, is_delete=False)
        except:
            return Response({"message":"对不起，操作的商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 操作redis
        redis_conn = get_redis_connection("cart")
        pipe = redis_conn.pipeline()
        pipe.multi()
        pipe.hdel("cart_%s" % user_id, course_id)
        pipe.srem("selected_%s" % user_id, course_id)
        pipe.execute()

        # 响应结果
        return Response({"message":"购物车删除商品成功！"}, status=status.HTTP_204_NO_CONTENT)

    def change_course_expire(self,request):
        """切换课程有效期"""
        # 获取登录用户id
        user_id = request.user.id
        # 获取客户端提交过来的课程有效期时间
        time = request.data.get("time")
        # 获取课程ID
        course_id = request.data.get("course_id")
        # 验证数据
        try:
            course = Course.objects.get(pk=course_id, is_show=True, is_delete=False)
            if int(time) != 0:
                course_expire = course.courseexpire.get(timer=time, course_id=course.id)
            else:
                if float(course.price) == 0:
                    raise Exception("对应的价格选项不存在！")
        except:
            return Response({"message":"对不起，操作的商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 链接redis，修改指定商品的勾选状态
        redis_conn = get_redis_connection("cart")
        redis_conn.hset("cart_%s" % user_id, course_id, time)

        return Response({"messsage":"切换有效期成功！"})

    def get_selected_course(self, request):
        """获取已经勾选的商品信息"""
        # 获取登录用户id
        user_id = 1 # request.user.id

        # 从redis提取购物车信息
        # 连接redis
        redis = get_redis_connection("cart")

        course_set = redis.smembers("selected_%s" % user_id)
        cart_list = redis.hgetall("cart_%s" % user_id)

        # 对购物车信息进行筛选
        # 计算所有商品的总价
        total_price = 0
        # 创建一个空的列表用于保存商品课程列表
        course_list = []
        for course_id_bytes in course_set:
            course_expire_bytes = cart_list[course_id_bytes]
            expire_time = course_expire_bytes.decode()
            course_id = int(course_id_bytes.decode())

            try:
                course = Course.objects.get(pk=course_id)
            except:
                return Response({"message":"对不起，商品课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)


            if expire_time == "0":
                expire_text = "永久有效"
            else:
                try:
                    # 获取当前本次用户购买商品的有效期选项文本格式
                    expire_obj = course.courseexpire.get(timer=expire_time)
                    expire_text = expire_obj.text
                except:
                    return Response({"message": "对不起，商品课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

            # 对购物车中信息进行补充和完善
            course_list.append({
                "course_id": course.id,
                "course_img": course.course_img.url,
                "name": course.name,
                "discount_name": course.discount_name,
                "expire": expire_text,
                "price": course.real_price(expire_time), # 没有打折的价格
                "discount_price": course.discount_price(course.real_price( expire_time )),
            })

        return Response(course_list)