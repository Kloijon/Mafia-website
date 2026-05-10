from users.models import User

def update_elo(game):
  players = game.players.all()

  for player in players:
    user = player.user
    user.elo += player.score_ci

    user.save()

