# Generated by Django 5.1.5 on 2025-01-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('score', models.IntegerField(default=0)),
                ('login_type', models.CharField(choices=[('general', '일반 로그인'), ('kakao', '카카오 로그인')], default='general', max_length=10)),
            ],
        ),
    ]