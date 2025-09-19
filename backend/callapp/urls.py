from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.generate_token, name='generate_token'),
    path('voice/', views.voice_response, name='voice_response'),
]
