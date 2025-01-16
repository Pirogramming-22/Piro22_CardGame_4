from django.urls import path
from . import views

urlpatterns = [
    path('', views.attack_game, name='attack_game'),  
    path('attack_game/', views.attack_game, name='attack_game'),
    path('attack/', views.attack, name='attack'),
]
