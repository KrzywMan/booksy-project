"""
URL configuration for booksy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),
    path('api/inventory/', views.get_inventory, name='inventory'),
    path('api/ai-search/', views.ai_search, name='ai_search'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/inventory/', views.get_inventory, name='inventory'),
    path('api/rent/<int:item_id>/', views.rent_item, name='rent_item'),
    path('api/return/<int:item_id>/', views.return_item, name='return_item'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('api/hardware/add/', views.add_hardware),
    path('api/hardware/delete/<int:item_id>/', views.delete_hardware),
    path('api/users/add/', views.add_user),
]
