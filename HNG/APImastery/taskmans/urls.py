""" Urls path for the app taskmans. """
from django.urls import path
from .views import (
    UserSignup,
    UserLogin,
    UserDetail,
    Logout,
    GetUsers,

    TaskList,
    TaskDetail,
    TaskCreate,
    TaskSearch,
    # TaskUpdate,
    # TaskDelete,

    TagView
    
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # List all tasks on the homepage
    path('', TaskList.as_view(), name='task-list'),
    path('search/', TaskSearch.as_view(), name='task-search'),
    path('users/allusers/', GetUsers.as_view(), name='allusers'),
    
    
    
    
    # create a new user
    path('users/register/', UserSignup.as_view(), name='user-create'),
    path('users/login/', UserLogin.as_view(), name='user-login'),
    

    # view each user details clicked wit    h the user id
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    # user id and update the user
    path('users/<int:pk>/update/', UserDetail.as_view(), name='user-update'),
    path('users/logout/', Logout.as_view(), name='user-logout'),
    # user id and delete the user
    path('users/<int:pk>/delete/', UserDetail.as_view(), name='user-delete'),
    
    
    
    
    # create a new task
    path('create_task/', TaskCreate.as_view(), name='create_tasks'),
    # view each task clicked with the task id
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    # task id and update the task
    path('tasks/<int:pk>/update/', TaskDetail.as_view(), name='task-update'),
    # task id and delete the task
    path('tasks/<int:pk>/delete/', TaskDetail.as_view(), name='task-delete'),
    
    # JWT token views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('tags/', TagView.as_view(), name='tags'),
    
]
