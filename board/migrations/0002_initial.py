# Generated by Django 5.1.5 on 2025-01-17 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('board', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='attacker_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker_boards', to=settings.AUTH_USER_MODEL, verbose_name='공격자 id'),
        ),
        migrations.AddField(
            model_name='board',
            name='defender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender_boards', to=settings.AUTH_USER_MODEL, verbose_name='방어자 id'),
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='board',
            name='attacker_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attacker_cards', to='board.card'),
        ),
        migrations.AddField(
            model_name='board',
            name='defender_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defender_cards', to='board.card'),
        ),
    ]