from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)

    @property
    def is_available(self):
        return self.available_quantity > 0

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def process_items_and_inventory(self):
        from django.core.exceptions import ValidationError as DjangoValidationError
        # Deduplicate items: sum quantities for each menu_item
        items = list(self.items.all())
        deduped = {}
        for item in items:
            menu_item = item.menu_item
            if menu_item in deduped:
                deduped[menu_item].quantity += item.quantity
                deduped[menu_item].save(update_fields=["quantity"])
                item.delete()
            else:
                deduped[menu_item] = item
        errors = []
        for menu_item, item in deduped.items():
            if menu_item.available_quantity < item.quantity:
                errors.append(f'Not enough quantity for menu item "{menu_item.name}". Available: {menu_item.available_quantity}, Requested: {item.quantity}')
        if errors:
            self.delete()
            raise DjangoValidationError({'__all__': errors})
        for menu_item, item in deduped.items():
            menu_item.available_quantity -= item.quantity
            menu_item.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"
