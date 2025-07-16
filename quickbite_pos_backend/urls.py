"""
URL configuration for quickbite_pos_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def root_landing(request):
    return HttpResponse('<h2>QuickBite POS Backend is running.</h2><p>Welcome to the QuickBite POS API server.</p>')

urlpatterns = [
    path('', root_landing),
    path("admin/", admin.site.urls),
    path("api/", include("pos.urls")),
]

