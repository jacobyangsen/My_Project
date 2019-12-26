
# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderModelSerializer
from .models import Order
class OrderCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


from .serializers import OrderListModelSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListModelSerializer
    queryset = Order.objects.all().order_by("-create_time")
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id', ]

    def list(self,request,**kwargs):
        if request.user.id != int(request.query_params.get("user_id")):
            return Response({"message":"对不起，您无法查看其他用户的订单信息"}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request,**kwargs)