from backend import views
from django.urls import path


urlpatterns = (
    path('games/create', views.create_game, name='game-create'),
    path('games/join', views.join_game, name='game-join'),
    path('games/<uuid:pk>', views.view_game, name='game-view'),
    path('games/<uuid:pk>/start', views.start_game, name='game-start'),
    path('games/<uuid:pk>/next-player', views.next_player, name='next-player'),
)
