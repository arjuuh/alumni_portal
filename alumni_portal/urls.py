from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('alumni_module.urls')),
    path('teacher/', include('teacher_module.urls')),
    path('', include('alumni_module.urls')),
    path('admin/', admin.site.urls),
]