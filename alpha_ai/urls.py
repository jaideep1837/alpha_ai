from django.contrib import admin
from django.urls import path, include
from alpha_ai import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', views.homepage),
]