from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('menu-items/', views.AvailableMenuItemsList.as_view(), name='menu-items'),
    path('orders/', views.OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('analytics/average-daily-sales/', views.AverageDailySalesView.as_view(), name='average-daily-sales'),
]
