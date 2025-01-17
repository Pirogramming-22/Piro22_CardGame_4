from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    커스텀 사용자 모델 관리자.
    """
    def create_user(self, id, nickname, password=None, **extra_fields):
        if not id:
            raise ValueError("아이디는 필수입니다.")
        if not nickname:
            raise ValueError("닉네임은 필수입니다.")
        
        user = self.model(id=id, nickname=nickname, **extra_fields)
        if password:
            user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, id, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("슈퍼유저는 is_staff=True이어야 합니다.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("슈퍼유저는 is_superuser=True이어야 합니다.")

        return self.create_user(id, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    커스텀 사용자 모델.
    """
    LOGIN_CHOICES = (
        ('general', '일반 로그인'),
        ('kakao', '카카오 로그인'),
        ('naver', '네이버 로그인'),
    )

    id = models.CharField(max_length=50, primary_key=True, unique=True)  # 공통 ID
    password = models.CharField(max_length=128, blank=True, null=True)  # 비밀번호
    nickname = models.CharField(max_length=50, unique=True)  # 닉네임
    score = models.IntegerField(default=0)
    login_type = models.CharField(max_length=10, choices=LOGIN_CHOICES, default='general')  # 로그인 방식

    # 추가 필드 (Django 인증 시스템과의 호환성)
    is_active = models.BooleanField(default=True)  # 계정 활성화 여부
    is_staff = models.BooleanField(default=False)  # 관리자 여부

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'  # 사용자 인증 시 사용할 필드
    REQUIRED_FIELDS = ['nickname']  # 슈퍼유저 생성 시 필요한 필드

    def __str__(self):
        return f"{self.nickname} ({self.login_type})"
