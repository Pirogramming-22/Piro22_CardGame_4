# Generated by Django 5.1.5 on 2025-01-17 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('howTowin', models.CharField(choices=[('L', 'Low'), ('H', 'High')], max_length=1, verbose_name='승리조건')),
                ('attack_num', models.IntegerField(verbose_name='공격자 카드 숫자')),
                ('defend_num', models.IntegerField(blank=True, null=True, verbose_name='방어자 카드 숫자')),
                ('status', models.CharField(choices=[('진', '진행중'), ('종', '종료')], default='진', max_length=1, verbose_name='상태')),
                ('result', models.CharField(blank=True, choices=[('A', 'Attacker'), ('D', 'Defender')], max_length=1, null=True, verbose_name='결과')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('attacker_card_number', models.IntegerField(default=0, verbose_name='공격자 카드 번호')),
                ('defender_card_number', models.IntegerField(null=True, verbose_name='방어자 카드 번호')),
                ('attacker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker_boards', to='users.user', verbose_name='공격자 id')),
                ('defender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender_boards', to='users.user', verbose_name='방어자 id')),
                ('attacker_card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attacker_cards', to='board.card')),
                ('defender_card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defender_cards', to='board.card')),
            ],
        ),
    ]