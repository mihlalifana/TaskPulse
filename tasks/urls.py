from django.urls import path
from tasks import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('task-list/', views.task_list, name='task_list'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('progress/', views.progress_view, name='progress'), 
    path('mood_checkin/', views.mood_checkin, name='mood_checkin'),  # Mood check-in form
    path('mood_success/', views.mood_checkin, name='mood_success'),
]