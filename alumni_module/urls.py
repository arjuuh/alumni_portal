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
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('jobs/', views.jobs, name='jobs'),
    path('events/', views.events, name='events'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("messages/", views.messages_home, name="messages"),
    path("messages/<int:conv_id>/", views.messages_home, name="messages_conv"),
    path("messages/start/<int:user_id>/", views.start_conversation, name="start_conversation"),
    path("messages/send/", views.send_message, name="send_message"),
    path("messages/<int:conv_id>/fetch/", views.fetch_messages, name="fetch_messages"),
    path("messages/<int:conv_id>/clear/", views.clear_chat, name="clear_chat"),
]