from django.db import models
from users.models import User

# Create your models here.
class Board(models.Model):
    howTowinChoice = (
        ('L', "Low"),
        ('H', "High")
    )
    statusChoice = (
        ('진', "진행중"),   # 4-1 경우
        # ('반', "반격가능"), # 4-2는 4-1과 같은 상태의 게임임. 공격자가 공격을 선언했고 방어자가 수락(반격,대응)하지 않은 상태
        ('종', "종료")      # 4-3 경우
    )
    resultChoice = (
        ('A', "Attacker"),  # 공격자가 승리
        ('D', "Defender"),  # 방어자가 승리
    )
    
    howTowin = models.CharField("승리조건", choices=howTowinChoice, max_length=1)
    attacker_id = models.ForeignKey(User, models.CASCADE, verbose_name="공격자 id")
    attack_num = models.IntegerField("공격자 카드 숫자")
    defender_id = models.ForeignKey(User, models.CASCADE, verbose_name="방어자 id")
    defend_num = models.IntegerField("방어자 카드 숫자", null=True)
    status = models.CharField("상태", choices=statusChoice, default="진", max_length=1)
    result = models.CharField("결과", choices=resultChoice, null=True)
    created_at = models.DateTimeField("생성 일시", auto_now_add=True)
    
    
