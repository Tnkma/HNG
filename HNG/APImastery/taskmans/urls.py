""" Urls path for the app taskmans. """
from django.urls import path
from .views import UserDetail, TaskList, TaskDetail, UserSignup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # List all tasks on the homepage
    path('', TaskList.as_view(), name='task-list'),
    # create a new user
    path('SignUp/', UserSignup.as_view(), name='user-create'),
    # view each user details clicked with the user id
    path('Login/', UserDetail.as_view(), name='user-login'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    # user id and update the user
    path('<int:pk>/update/', UserDetail.as_view(), name='user-update'),
    # user id and delete the user
    path('<int:pk>/delete/', UserDetail.as_view(), name='user-delete'),
    # create a new task
    path('create_task/', TaskList.as_view(), name='create_tasks'),
    # view each task clicked with the task id
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    # task id and update the task
    path('tasks/<int:pk>/update/', TaskDetail.as_view(), name='task-update'),
    # task id and delete the task
    path('tasks/<int:pk>/delete/', TaskDetail.as_view(), name='task-delete'),
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
