from django.db import models

class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True)
    password = models.CharField(max_length=128)
    score = models.IntegerField(default=0)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.id