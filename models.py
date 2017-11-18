from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Gamer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    game_one_score = models.IntegerField()

    def __str__(self):
        return self.user

class Game(models.Model):
    game_name = models.CharField(max_length=50)
    game_detail = models.CharField(max_length=200)
    game_best_score = models.CharField(max_length=10)
    game_best_scorer = models.CharField(max_length=50)

    def __str__(self):
        return self.game_name+' - '+self.game_best_score+' - '+self.game_best_scorer

