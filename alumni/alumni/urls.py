from django.contrib import admin
from django.urls import path
from alumni_module import views as alumni_views
from teacher_module import views as teacher_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', alumni_views.home, name='home'),
    path('register/', alumni_views.register, name='register'),
    path('alumni-list/', alumni_views.alumni_list, name='alumni_list'),
    path('login/', alumni_views.alumni_login, name='alumni_login'),
    path('dashboard/', alumni_views.dashboard, name='dashboard'),
    path('logout/', alumni_views.logout_view),
    path('teacher/login/', teacher_views.teacher_login),
    path('teacher/logout/', teacher_views.teacher_logout),
    path('teacher/verify/', teacher_views.verify_alumni, name='verify_alumni'),
]
