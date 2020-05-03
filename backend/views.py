import random
import string

from backend import models, serializers
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ErrorResponse(Response):
    def __init__(self, message, status):
        super(ErrorResponse, self).__init__({'error': message}, status=status)


def is_allowed(request, game):
    return game.players.filter(pk=request.headers.get('Player-Id')).exists()


@api_view(['POST'])
@transaction.atomic
def create_game(request):
    serializer = serializers.CreateGameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    game = models.Game()
    game.secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    game.save()

    player = models.Player(game=game, name=serializer.data.get('name'))
    player.save()

    return Response(serializers.PlayerSerializer(player).data)


@api_view(['POST'])
def join_game(request):
    serializer = serializers.JoinGameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        game = models.Game.objects.get(secret=serializer.data.get('secret'))
    except models.Game.DoesNotExist:
        return ErrorResponse('The game does not exist', status=404)

    if game.started:
        return ErrorResponse('The game is already started', status=409)

    if game.finished:
        return ErrorResponse('The game is already finished', status=409)

    if game.players.filter(name=serializer.data.get('name')).count() > 0:
        return ErrorResponse('This name has already be taken for this game', status=409)

    player = models.Player(game=game, name=serializer.data.get('name'))
    player.save()

    return Response(serializers.PlayerSerializer(player).data)


@api_view(['GET'])
def view_game(request, pk):
    try:
        game = models.Game.objects.get(pk=pk)
    except models.Game.DoesNotExist:
        return ErrorResponse('The game does not exist', status=404)

    if not is_allowed(request, game):
        return ErrorResponse('You are not allowed to access this game', status=401)

    return Response(serializers.GameSerializer(game).data)


@api_view(['POST'])
@transaction.atomic
def start_game(request, pk):
    try:
        game = models.Game.objects.get(pk=pk)
    except models.Game.DoesNotExist:
        return ErrorResponse('The game does not exist', status=404)

    if not is_allowed(request, game):
        return ErrorResponse('You are not allowed to access this game', status=401)

    if game.players.count() < 2:
        return ErrorResponse('There is not enough player', 409)

    if game.started:
        return ErrorResponse('The game is already started', status=409)

    if game.finished:
        return ErrorResponse('The game is already finished', status=409)

    if game.players.count() > models.Character.objects.count():
        return ErrorResponse('There are not enough character', status=409)

    if game.players.count() > models.Action.objects.count():
        return ErrorResponse('There are not enough action', status=409)

    characters = list(models.Character.objects.all())
    actions = list(models.Action.objects.all())

    for player in game.players.all():
        character_index = random.randint(0, len(characters) - 1)
        action_index = random.randint(0, len(actions) - 1)

        player.character = characters.pop(character_index)
        player.action = actions.pop(action_index)

        player.save()

    game.started = True
    game.current_player = game.players.order_by('name').first()
    game.save()

    return Response(serializers.GameSerializer(game).data)


@api_view(['POST'])
@transaction.atomic
def next_player(request, pk):
    serializer = serializers.NextPlayerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        game = models.Game.objects.get(pk=pk)
    except models.Game.DoesNotExist:
        return ErrorResponse('The game does not exist', status=404)

    if not is_allowed(request, game):
        return ErrorResponse('You are not allowed to access this game', status=401)

    if not game.started:
        return ErrorResponse('The game is not yet started', status=409)

    if game.finished:
        return ErrorResponse('The game is already finished', status=409)

    if str(game.current_player.id) != serializer.data.get('current_player'):
        return ErrorResponse('This is not the current player', status=409)

    players = list(game.players.order_by('id').filter(Q(character_found=False) | Q(action_found=False)).all())

    if game.current_player is None:
        game.current_player = players[0]
    else:
        current_player_index = players.index(game.current_player)

        if not game.current_player.character_found and serializer.data.get('character_found'):
            game.current_player.character_found = True
            game.current_player.save()
        
        if not game.current_player.action_found and serializer.data.get('action_found'):
            game.current_player.action_found = True
            game.current_player.save()

        if len(players) == 1 and game.current_player.character_found and game.current_player.action_found:
            game.current_player = None
            game.finished = True
        else:
            if current_player_index + 1 == len(players):
                game.current_player = players[0]
            else:
                game.current_player = players[current_player_index + 1]

    game.save()

    return Response(serializers.GameSerializer(game).data)
