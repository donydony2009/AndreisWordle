from django.urls import path
from .views import game_view, restart_game

urlpatterns = [
    path('', game_view, name='game'),
    path('restart/', restart_game, name='restart_game'),
]
