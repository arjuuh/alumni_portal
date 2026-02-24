from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    #path('directory/', views.alumni_directory, name='alumni_directory'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('waiting/', views.waiting_approval, name='waiting_approval'),
    path("alumni/", views.alumni_list_view, name="alumni_list"),
]
