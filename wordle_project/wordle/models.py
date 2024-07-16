from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=5, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.word

class Guess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    guess = models.CharField(max_length=5)
    attempts = models.IntegerField()
    is_correct = models.BooleanField()
    guess_info = models.JSONField(default=list)  # Add this field to store guess info
    
    def __str__(self):
        return self.guess
