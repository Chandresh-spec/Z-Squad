from django.urls import path
from .views import ParseCommandView

urlpatterns = [
    path('parse/', ParseCommandView.as_view(), name='voice_parse_command'),
]
