from django.urls import path
from board import views

app_name = 'board'
urlpatterns = [
    path('attack_game/', views.attack_game, name='attack_game'),
    path('attack/', views.attack, name='attack'),
    path('info/<int:pk>', views.info, name='board_info'), # 게임 정보 페이지
    path('ranking', views.ranking, name='board_ranking'), # 게임 정보 페이지
    path('game_list/', views.game_list, name='game_list'),  # 전적 목록 페이지
    path('counter_attack/<int:pk>/', views.counter_attack, name='counter_attack'),
    path('delete/<int:game_id>/', views.board_delete, name='board_delete'),
]
