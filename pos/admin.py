from django.contrib import admin

from .models import MenuItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id","name", "price", "available_quantity", "is_available")
    list_filter = ("available_quantity",)
    search_fields = ("name",)

    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True
    is_available.short_description = 'Available'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "status")
    list_filter = ("status", "timestamp")
    inlines = [OrderItemInline]
    search_fields = ("id",)
    ordering = ("-timestamp",)

    def save_related(self, request, form, formsets, change):
        # Enforce available_quantity logic for admin order creation
        from django.core.exceptions import ValidationError as DjangoValidationError
        order = form.instance
        # Only check if this is a new order
        is_new = order.pk is None
        super().save_related(request, form, formsets, change)
        # After inlines are saved, check all items
        if is_new:
            errors = []
            items = order.items.all()
            # Check all items for stock
            for item in items:
                menu_item = item.menu_item
                if menu_item.available_quantity < item.quantity:
                    errors.append(f'Not enough quantity for menu item "{menu_item.name}". Available: {menu_item.available_quantity}, Requested: {item.quantity}')
            if errors:
                # Roll back by deleting the just-saved order and its items
                order.delete()
                raise DjangoValidationError({'__all__': errors})
            # Decrement stock
            for item in items:
                menu_item = item.menu_item
                menu_item.available_quantity -= item.quantity
                menu_item.save()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity")
    list_filter = ("menu_item",)
    search_fields = ("order__id", "menu_item__name")
