from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]