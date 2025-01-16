from django.db import models
from django.contrib.auth.models import User

from users.models import User

# Create your models here.
#카드 번호와 소유자(owner) 속성, 각 게임에서 사용될 수 있는 독립적인 엔티티
class Card(models.Model):
    number = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number} (Owner: {self.owner.username})"


# 그 다음에 Board 모델을 정의
class Board(models.Model):
    howTowinChoice = (
        ('L', "Low"),
        ('H', "High")
    )
    statusChoice = (
        ('진', "진행중"),
        ('종', "종료")
    )
    resultChoice = (
        ('A', "Attacker"),
        ('D', "Defender"),
    )
    
    howTowin = models.CharField("승리조건", choices=howTowinChoice, max_length=1)
    attacker_id = models.ForeignKey(User, models.CASCADE, verbose_name="공격자 id", related_name="attacker_boards")
    attack_num = models.IntegerField("공격자 카드 숫자")
    defender_id = models.ForeignKey(User, models.CASCADE, verbose_name="방어자 id", related_name="defender_boards")
    defend_num = models.IntegerField("방어자 카드 숫자", null=True)
    status = models.CharField("상태", choices=statusChoice, default="진", max_length=1)
    result = models.CharField("결과", choices=resultChoice, max_length=1, null=True)
    created_at = models.DateTimeField("생성 일시", auto_now_add=True)

    # 추가된 필드들
    attacker_card_number = models.IntegerField("공격자 카드 번호", default=0)
    defender_card_number = models.IntegerField("방어자 카드 번호", null=True)
    
    attacker_card = models.ForeignKey(Card, related_name="attacker_cards", on_delete=models.CASCADE, null=True)
    defender_card = models.ForeignKey(Card, related_name="defender_cards", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Board {self.id}: {self.attacker_id.username} vs {self.defender_id.username}"
