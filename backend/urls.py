from django.urls import path, include
from apps.core.views import test_view

urlpatterns = [
    path('api/test/', test_view),
]