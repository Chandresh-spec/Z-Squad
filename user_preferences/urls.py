from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_preferences, name='manage_preferences'),
    path('settings/', views.get_smart_settings, name='smart_settings'),
]
