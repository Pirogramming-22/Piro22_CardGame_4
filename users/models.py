from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField("유저 아이디", primary_key=True, max_length=10)
    score = models.IntegerField("점수", default=0)
