from django.urls import path, include
from django.contrib.auth import views as auth_views
from . views import CalendarView, DisplayTasks, AddTask, GetAboutTask, ChangetTask, ChangeStatusTaskToFinish, ChangeStatusTaskToStart

urlpatterns = [
    path('', CalendarView.as_view(), name='calendar_board'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tasks/', DisplayTasks.as_view(), name='display_tasks'),
    path('add/', AddTask.as_view(), name='add_task'),
    path('about/', GetAboutTask.as_view(), name='about_task'),
    path('change/', ChangetTask.as_view(), name='change_task'),
    path('finish_status/', ChangeStatusTaskToFinish.as_view(), name='finish_status'),
    path('start_status/', ChangeStatusTaskToStart.as_view(), name='start_status'),
]