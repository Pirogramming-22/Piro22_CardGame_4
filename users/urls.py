from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main_prelogin, name = 'main_prelogin' ),
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('main/', views.main_page, name='main_page'),
    path('logout/', views.logout_view, name='logout_view'),
]