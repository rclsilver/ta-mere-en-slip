from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Action(BaseModel):
    text = models.CharField(max_length=256, unique=True)


class Character(BaseModel):
    text = models.CharField(max_length=256, unique=True)


class Game(BaseModel):
    secret = models.CharField(max_length=8, unique=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    current_player = models.ForeignKey('Player', related_name='+', on_delete=models.CASCADE, null=True)


class Player(BaseModel):
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    character_found = models.BooleanField(default=False)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True)
    action_found = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('game', 'name'),
            ('game', 'character'),
            ('game', 'action'),
        )
