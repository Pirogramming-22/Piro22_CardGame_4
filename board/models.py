from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    number = models.IntegerField()  
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.number} (Owner: {self.owner.username})"

class Attack(models.Model):
    attacker = models.ForeignKey(User, related_name='attacker', on_delete=models.CASCADE)
    defender = models.ForeignKey(User, related_name='defender', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} attacks {self.defender} with card {self.card.number}"
