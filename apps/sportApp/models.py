from django.db import models
from django.db import connection

class Team(models.Model):
    team_name = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    ability = models.DecimalField(max_digits=5, decimal_places=2)
    team_num = models.IntegerField()
    image_tag = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return (f'Team_num:{self.team_num} team_name:{self.team_name} ability: {self.ability} ||| \n')

class Players(models.Model):
    name = models.CharField(max_length=45)
    year = models.IntegerField()
    position = models.CharField(max_length=12)
    ability = models.DecimalField(max_digits=6, decimal_places=3)
    team = models.ForeignKey(Team, related_name="players")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'Year: {self.year} Ability: {self.ability} \n')


class Settings(models.Model):
    numOfTeams = models.IntegerField()
    myTeam = models.IntegerField()
    week_num = models.IntegerField()
    season_num = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Standings(models.Model):
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    win_pct = models.DecimalField(max_digits=5, decimal_places=2)
    pts_for = models.IntegerField()
    pts_against = models.IntegerField()

class historicalStandings(models.Model):
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    win_pct = models.DecimalField(max_digits=5, decimal_places=2)
    pts_for = models.IntegerField()
    pts_against = models.IntegerField()
    champ_wins = models.IntegerField()
    champ_losses = models.IntegerField()
    champ_win_pct = models.DecimalField(max_digits=5, decimal_places=2)

    def __repr__(self):
        return (f'{self.id}: {self.wins}-{self.losses}-{self.ties} %{self.win_pct} \n')

class Schedule(models.Model):
    home_team = models.IntegerField()
    away_team = models.IntegerField()
    home_score = models.IntegerField(default=None, blank=True, null=True)
    away_score = models.IntegerField(default=None, blank=True, null=True)
    result = models.IntegerField(default=None, blank=True, null=True)
    week_num = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __repr__(self):
        return (f'WK{self.week_num} Home: {self.home_team}, Away: {self.away_team}, Home Score: {self.home_score}, Away Score: {self.away_score}, result {self.result}  \n')

