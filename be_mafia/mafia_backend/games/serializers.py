from rest_framework import serializers
from .models import Game, UserPlay, Role
from users.models import User

class UserPlaySerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

  class Meta: 
    model = UserPlay
    fields = [
      'user',
      'play_role',
      'foul',
      'tech_foul',
      'score_plus',
      'score_minus',
      'score_ci',
      'thoughts',
      'protocol',
    ]
  
  def validate_score_plus(self, value):
    if value is not None and value < 0: 
      raise serializers.ValidationError('score_plus не может быть меньше 0')
    return value

  def validate_score_minus(self, value):
    if value is not None and value < 0:
      raise serializers.ValidationError('score_minus не может быть меньше 0')
    return value
  
  def validate_score_ci(self, value):
    if value is not None and value < 0:
      raise serializers.ValidationError('score_ci не может быть меньше 0')
    return value
  
  def validate_foul(self, value):
    if value > 4:
      raise serializers.ValidationError('Максимальное количество фолов - 4')
    return value
  
  def validate_tech_foul(self, value):
    if value > 2:
      raise serializers.ValidationError('Максимальное количество технических фолов - 2')
    return value
    
class GameSerializer(serializers.ModelSerializer):
  players = UserPlaySerializer(source='userplay_set', many=True, read_only=True)

  class Meta:
    model = Game
    fields = [
      'id',
      'referee',
      'tournament',
      'result',
      'players',
    ]
    read_only_fields = ['id',]
  


class GameCreateSerializer(serializers.ModelSerializer):
  players = UserPlaySerializer(many=True)

  class Meta: 
    model = Game 
    fields = ['referee', 'tournament', 'result', 'players',]

  def validate(self, data):
    players = data.get('players', [])

    roles = [p['play_role'] for p in players]

    if roles.count(Role.DON) != 1: 
      raise serializers.ValidationError('Должен быть 1 дон')

    if roles.count(Role.SHERIFF) != 1: 
      raise serializers.ValidationError('Должен быть 1 шериф')
    
    if roles.count(Role.MAFIA) != 1: 
      raise serializers.ValidationError('Должна быть 1 мафия')
    
    if roles.count(Role.CIVILIAN) != 7:
      raise serializers.ValidationError('Должно быть 7 мирных')
    
    users_id = [p['user'].id for p in players]

    if len(users_id) != len(set(users_id)):
      raise serializers.ValidationError('Игроки не должны повторяться')
    
    if len(users_id) != 10:
      raise serializers.ValidationError('Должно быть ровно 10 игроков')
    
    return data
  
  def create(self, validated_data):
    players_data = validated_data.pop('players')

    game = Game.objects.create(**validated_data)

    for player_data in players_data:
      UserPlay.objects.create(game=game, **player_data)

    return game
