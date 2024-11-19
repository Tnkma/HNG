""" Urls path for the app api. """
from django.urls import path
from tasks.views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskSearch,
    
)

urlpatterns = [
    # List all tasks on the homepage
    path('', TaskList.as_view(), name='task-list'),
    path('search/', TaskSearch.as_view(), name='task-search'),    
    # create a new task
    path('create_task/', TaskCreate.as_view(), name='create_tasks'),
    # view each task clicked with the task id
    path('<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    # task id and update the task
    path('<int:pk>/update/', TaskDetail.as_view(), name='task-update'),
    # task id and delete the task
    path('<int:pk>/delete/', TaskDetail.as_view(), name='task-delete'),
]
