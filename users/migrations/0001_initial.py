# Generated by Django 5.1.5 on 2025-01-16 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='유저 아이디')),
            ],
        ),
    ]
