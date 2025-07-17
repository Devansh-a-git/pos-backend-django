from django.contrib import admin

from .models import MenuItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "price", "available_quantity", "is_available")
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
        order = form.instance
        super().save_related(request, form, formsets, change)
        if order.pk:
            order.process_items_and_inventory()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity")
    list_filter = ("menu_item",)
    search_fields = ("order__id", "menu_item__name")
