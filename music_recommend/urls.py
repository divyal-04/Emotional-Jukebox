# your_django_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('emotion-detection/', include('emotion_detection.urls')),
]
