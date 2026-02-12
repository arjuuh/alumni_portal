from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('verify/', views.verify_alumni, name='verify_alumni'),
    path('approve/<int:user_id>/', views.approve_alumni, name='approve_alumni'),
]