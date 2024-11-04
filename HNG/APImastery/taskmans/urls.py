""" Urls path for the app taskmans. """
from django.urls import path
from .views import UserDetail, UserList

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('create/', UserList.as_view(), name='user-create'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('<int:pk>/update/', UserDetail.as_view(), name='user-update'),
    path('<int:pk>/delete/', UserDetail.as_view(), name='user-delete'),
]
