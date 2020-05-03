from backend import models
from rest_framework import serializers


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = ('text',)


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = ('text',)


class PlayerSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()
    action = ActionSerializer()

    class Meta:
        model = models.Player
        fields = ('id', 'name', 'game', 'character', 'action', 'character_found', 'action_found')


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    current_player = PlayerSerializer()

    class Meta:
        model = models.Game
        fields = ('id', 'secret', 'players', 'started', 'finished', 'current_player')


class CreateGameSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        fields = ('name',)


class JoinGameSerializer(CreateGameSerializer):
    secret = serializers.CharField()

    class Meta(CreateGameSerializer.Meta):
        fields = CreateGameSerializer.Meta.fields + ('secret',)


class NextPlayerSerializer(serializers.Serializer):
    current_player = serializers.UUIDField()
    character_found = serializers.BooleanField()
    action_found = serializers.BooleanField()
