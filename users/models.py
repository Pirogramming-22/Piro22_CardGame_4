from django.db import models

class User(models.Model):
    LOGIN_CHOICES = (
        ('general', '일반 로그인'),
        ('kakao', '카카오 로그인'),
        ('naver', '네이버 로그인'),

    )

    id = models.CharField(max_length=50, primary_key=True, unique=True)  # 공통 ID (카카오 ID 또는 일반 사용자 ID)
    password = models.CharField(max_length=128, blank=True, null=True)  # 일반 로그인 사용자의 비밀번호
    nickname = models.CharField(max_length=50, unique=True)  # 닉네임
    score = models.IntegerField(default=0)
    login_type = models.CharField(max_length=10, choices=LOGIN_CHOICES, default='general')  # 로그인 방식

    def __str__(self):
        return f"{self.nickname} ({self.login_type})"
