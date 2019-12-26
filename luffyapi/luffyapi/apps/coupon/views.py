# Create your views here.
from rest_framework.generics import ListAPIView
from .models import UserCoupon
from .serializers import UserCouponModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
class UserCouponListAPIView(ListAPIView):
    queryset = UserCoupon.objects.filter(is_delete=False,is_show=True,is_use=False)
    serializer_class = UserCouponModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_id']
