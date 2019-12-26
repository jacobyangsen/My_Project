from my_celery.main import app
from orders.models import Order
from datetime import datetime
from luffyapi.settings import constants

@app.task(name="check_order")
def check_order():
    """检查订单是否超时"""
    now = datetime.now().timestamp()
    timeout_number = now - constants.ORDER_TIMEOUT
    timeout = datetime.fromtimestamp(timeout_number)
    timeout_order_list = Order.objects.filter(order_status=0, create_time__lte=timeout)
    for order in timeout_order_list:

        order.order_status = 3
        # 补充下优惠券和积分的逻辑
        # 判断订单的积分是否大于0，大于0则还原积分
        # 判断订单的优惠券是否大于0，大于0，则还原优惠券的使用状态
        order.save()