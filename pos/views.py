from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer
    
class AvailableMenuItemsList(generics.ListAPIView):
    queryset = MenuItem.objects.filter(available_quantity__gt=0)
    serializer_class = MenuItemSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        qs = Order.objects.all().order_by('-timestamp')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def create(self, request, *args, **kwargs):
        items = request.data.get('items', [])
        unavailable_items = []
        for item in items:
            menu_item_id = item.get('menu_item_id')
            quantity = item.get('quantity', 0)
            if menu_item_id:
                menu_item = MenuItem.objects.filter(id=menu_item_id).first()
                if not menu_item or menu_item.available_quantity < quantity:
                    unavailable_items.append(menu_item_id)
        if unavailable_items:
            raise ValidationError({'detail': f'Menu items unavailable or not enough quantity: {unavailable_items}'})
        return super().create(request, *args, **kwargs)

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        # Only allow status update
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        status_value = request.data.get('status')
        if status_value not in dict(Order.STATUS_CHOICES):
            raise ValidationError({'detail': 'Invalid status'})
        instance.status = status_value
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AverageDailySalesView(APIView):
    def get(self, request):
        today = timezone.localdate()
        days_checked = 0
        sales = []
        day = today
        while len(sales) < 4 and days_checked < 10:
            if day.weekday() < 5:  # Monday=0, ..., Friday=4
                day_orders = Order.objects.filter(
                    status='completed',
                    timestamp__date=day
                )
                total = 0
                for order in day_orders:
                    for item in order.items.all():
                        total += item.menu_item.price * item.quantity
                sales.append({'date': str(day), 'average_revenue': float(total)})
            day -= timedelta(days=1)
            days_checked += 1
        sales = sales[::-1]  # Oldest first
        return Response(sales)
