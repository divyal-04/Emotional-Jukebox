from django.urls import path
from .views import detect_emotion, suggest_song  # Import the new view

urlpatterns = [
    path('', detect_emotion, name='detect_emotion'),
    path('suggest_song/', suggest_song, name='suggest_song'),  # Add the new URL pattern
]
