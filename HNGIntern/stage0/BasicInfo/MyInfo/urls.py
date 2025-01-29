from django.urls import path
from .views import MyInfo

urlpatterns = [
    path('api/', MyInfo.as_view(), name='myinfo'),
]
