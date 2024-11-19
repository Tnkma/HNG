""" Urls path for the app api. """
from django.urls import path
from users.views import (
    UserSignup,
    UserLogin,
    UserDetail,
    Logout,
    GetUsers,
)

urlpatterns = [
    path('allusers/', GetUsers.as_view(), name='allusers'),
    # create a new user
    path('register/', UserSignup.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    

    # view each user details clicked wit    h the user id
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    # user id and update the user
    path('<int:pk>/update/', UserDetail.as_view(), name='user-update'),
    path('logout/', Logout.as_view(), name='user-logout'),
    # user id and delete the user
    path('<int:pk>/delete/', UserDetail.as_view(), name='user-delete'),  
]
