from rest_framework import serializers
from .models import MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'available_quantity', 'is_available']

    def get_is_available(self, obj):
        return obj.is_available

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be a positive integer.')
        return value

    def validate(self, attrs):
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'timestamp', 'status', 'items']

    from django.db import transaction

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        errors = []
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            if menu_item.available_quantity < quantity:
                errors.append(f'Not enough quantity for menu item "{menu_item.name}". Available: {menu_item.available_quantity}, Requested: {quantity}')
        if errors:
            raise serializers.ValidationError({'detail': errors})
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            menu_item.available_quantity -= quantity
            menu_item.save()
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        # Only update status for simplicity
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
