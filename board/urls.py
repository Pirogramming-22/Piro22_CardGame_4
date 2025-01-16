from django.urls import path
from board import views

app_name = 'board'

urlpatterns = [
    path('info/<int:pk>', views.info, name='board_info'), # 게임 정보 페이지
    path('ranking', views.ranking, name='board_ranking'), # 게임 정보 페이지
]