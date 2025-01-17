from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'users'

urlpatterns = [
    path('', views.main_prelogin, name = 'main_prelogin' ),
    path('login/', views.login_view, name='login_view'),
    path('main/', views.main_page, name='main_page'),
    path('logout/', views.logout_view, name='logout_view'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('signup/', views.signup, name='signup'),
    path('naver/login/', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
]
