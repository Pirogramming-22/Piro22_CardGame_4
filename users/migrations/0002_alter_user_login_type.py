# Generated by Django 5.1.5 on 2025-01-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_type',
            field=models.CharField(choices=[('general', '일반 로그인'), ('kakao', '카카오 로그인'), ('naver', '네이버 로그인'), ('google', '구글 로그인')], default='general', max_length=10),
        ),
    ]
