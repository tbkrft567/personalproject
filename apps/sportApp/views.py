from django.shortcuts import render, redirect
from .models import *
import random
import math
from decimal import *
from django.db.models import Q, Avg

##LOGIC -- NEEDS TO redirect RATHER THAN 
def startSeason(request):
    Schedule.objects.all().delete()
    Settings.objects.all().delete()
    # request.session.flush()
    
    histStandings = historicalStandings.objects.all()
    for hRecord in histStandings:
        hRecord.wins = 0
        hRecord.losses = 0
        hRecord.ties = 0
        hRecord.win_pct = 0.000
        hRecord.pts_for = 0
        hRecord.pts_against = 0
        hRecord.champ_wins = 0
        hRecord.champ_losses = 0
        hRecord.champ_win_pct = 0
        hRecord.save(update_fields=['wins', 'losses', 'ties', 'win_pct', 'pts_for', 'pts_against', 'champ_wins', 'champ_losses', 'champ_win_pct'])

    standings = Standings.objects.all()
    for record in standings:
        record.wins = 0
        record.losses = 0
        record.ties = 0
        record.win_pct = 0.000
        record.pts_for = 0
        record.pts_against = 0
        record.save(update_fields=['wins', 'losses', 'ties', 'win_pct', 'pts_for', 'pts_against'])

    
    # teams = Team.objects.all()
    # for team in teams:
    #     team.ability = random.randint(65, 100)
    #     team.save()
    # print(Team.objects.all())
    roster = Players.objects.all()
    roster.delete()
    
    return redirect('/renderNewSeason')

def renderNewSeason(request):
    context={
        'teams': Team.objects.all().order_by('team_num'), 
    }
    return render(request, 'sportApp/startseason.html', context)

##LOGIC
def nextSeason(request, seasonNum):
    numOfTeams = Settings.objects.last().numOfTeams

    removePlayers = Players.objects.filter(year=4)
    replacePlayerCount = removePlayers.count()
    removePlayers.delete()
    juniorPlayers = Players.objects.filter(year=3)
    juniorsRemoved = 0
    for player in juniorPlayers:
        if player.ability >=90:
            probability = float(((player.ability - 79)/100))**(1/2)-.09
            removalIndicator = round(random.random()/2.3+probability)
            if removalIndicator == 1:
                print(Players.objects.get(id=player.id).ability)
                Players.objects.get(id=player.id).delete()
                juniorsRemoved+=1
    
    NewRecruitsCount = replacePlayerCount+juniorsRemoved
    print('allRemoval: ', NewRecruitsCount, '3year: ', juniorsRemoved )

    teams = Team.objects.all().order_by('team_num')[:numOfTeams]
    for team in teams:
        print(team.ability, team.team_name)
        players = Players.objects.filter(team=Team.objects.get(team_num=team.team_num))
        currentCount = 15-players.count()
        for player in players:
            player.year+=1
            player.save()
            if player.year == 2:
                player.ability += round(5*random.random())
                if player.ability > 100:
                    player.ability = 100
            elif player.year == 3:
                player.ability += round(20*random.random())
                if player.ability > 100:
                    player.ability = 100
            elif player.year == 4:
                player.ability += round(10*random.random())
                if player.ability > 100:
                    player.ability = 100
            player.save()

        for player in range(currentCount): ##ADD UP TO 15 PLAYERS TO EACH TEAM
            year = 1
            ability = 60 + round(20*random.random())
            Players.objects.create(name='N/A', year=year, position='N/A', ability=ability, team=Team.objects.get(team_num=team.team_num))
        
        allPlayers = Players.objects.filter(team=Team.objects.get(team_num=team.team_num)).order_by('-ability')[:8] ##FIND AVERAGE OF STARTING LINE-UP (TOP 7 PLAYERS)
        averageAbility = allPlayers.aggregate(Avg('ability'))
        team.ability = round(averageAbility['ability__avg'],1)
        team.save()
        print(team.ability, team.team_name)

    settings = Settings.objects.last()
    settings.season_num += 1
    settings.week_num = 1
    settings.save(update_fields=['season_num', 'week_num'])
    # Save Historical Standings

    
    teams = Team.objects.all().order_by('team_num')[:numOfTeams]

    for team in teams: 
        hist_Standings = historicalStandings.objects.get(id=team.team_num)
        curr_Standings = Standings.objects.get(id=team.team_num)
        hist_Standings.wins += curr_Standings.wins
        hist_Standings.losses += curr_Standings.losses
        hist_Standings.ties += curr_Standings.ties
        hist_Standings.pts_for += curr_Standings.pts_for
        hist_Standings.pts_against += curr_Standings.pts_against
        # hist_Standings.champ_wins = curr_Standings.champ_wins
        # hist_Standings.champ_losses = curr_Standings.champ_losses
        hist_Standings.save(update_fields=['wins', 'losses', 'ties', 'pts_for', 'pts_against', 'champ_wins', 'champ_losses'])
        hist_Standings.win_pct = hist_Standings.wins/(hist_Standings.wins+hist_Standings.losses)
        hist_Standings.save()
        # hist_Standings.champ_win_pct = curr_Standings.champ_wins/(curr_Standings.champ_wins+curr_Standings.champ_losses)

    standings = Standings.objects.all()
    for record in standings:
        record.wins = 0
        record.losses = 0
        record.ties = 0
        record.win_pct = 0.000
        record.pts_for = 0
        record.pts_against = 0
        record.save(update_fields=['wins', 'losses', 'ties', 'win_pct', 'pts_for', 'pts_against'])

    Schedule.objects.all().delete()
    scheduleGrid = []
    weeklyGrid = []
    for x in range(numOfTeams):  # Create a grid for all matches to be played
        scheduleGrid.append([])
        weeklyGrid.append([])

    allMatches = []
    for home in range(1, numOfTeams+1):  # Insert all matches to be played
        for away in range(1, numOfTeams+1):
            allMatches.append([home, away])

    match = 0
    team = 1
    for x in range(len(scheduleGrid)):
        while match < len(allMatches):
            if allMatches[match][0] != team and scheduleGrid[x][len(scheduleGrid) - 1] != None:
                break

            if allMatches[match][0] != allMatches[match][1]:
                scheduleGrid[x].append(allMatches[match])
                weeklyGrid[x].append([])

            else:
                scheduleGrid[x].append(None)
                weeklyGrid[x].append([])

            match += 1

        team += 1

    matchesToPlay = pow(numOfTeams, 2) - numOfTeams
    matchesPerWeek = int(numOfTeams / 2)
    weeks = int(matchesToPlay / matchesPerWeek)

    for nullValue in range(numOfTeams):
        weeklyGrid[nullValue][nullValue].append(None)


    x = 0
    for weekCount in range(1, int(weeks)+1):
        for row in range(len(weeklyGrid)):
            for col in range(len(weeklyGrid[row])):
                if row == col:
                    continue
                rowTotal = 0
                for tempCol in range(numOfTeams):
                    if len(weeklyGrid[row][tempCol]) != 0 and weeklyGrid[row][tempCol][0] != None:
                        rowTotal += 1
                colTotal = 0
                for tempRow in range(numOfTeams):
                    if len(weeklyGrid[tempRow][col]) != 0 and weeklyGrid[tempRow][col][0] != None:
                        colTotal += 1
                if rowTotal == weekCount:
                    break
                if colTotal == weekCount:
                    continue
                if row > col:
                    continue
                if len(weeklyGrid[row][col]) == 0:
                    weeklyGrid[row][col].append(weekCount)
                    weeklyGrid[col][row].append(
                        int(weekCount + ((pow(numOfTeams, 2) - numOfTeams) / (numOfTeams / 2) / 2)))
                    break

    for homeTeam in range(numOfTeams):
        for awayTeam in range(numOfTeams):
            if scheduleGrid[homeTeam][awayTeam] == None:
                continue
            scheduleGrid[homeTeam][awayTeam].append(
                weeklyGrid[homeTeam][awayTeam][0])

    leagueSchedule = []
    for weekCount in range(1, weeks+1):
        matchesConfirmed = 0
        for homeTeam in range(numOfTeams): #Row
            for awayTeam in range(numOfTeams): #Col
                if scheduleGrid[homeTeam][awayTeam] != None:
                    if scheduleGrid[homeTeam][awayTeam][2] == weekCount:
                        leagueSchedule.append(scheduleGrid[homeTeam][awayTeam])
                        matchesConfirmed += 1
                        #if scheduleGrid[homeTeam][awayTeam][0] or [1] == homeTeam break awayTeam FOR
                        if scheduleGrid[homeTeam][awayTeam][0] == homeTeam+1 or scheduleGrid[homeTeam][awayTeam][1] == homeTeam+1:
                            break
                if matchesConfirmed == matchesPerWeek:
                    break
            if matchesConfirmed == matchesPerWeek:
                break

    for matchUp in leagueSchedule:
        Schedule.objects.create(home_team=matchUp[0], away_team=matchUp[1], week_num=matchUp[2])

    return redirect('/Homepage')
#move to next season vs. newSeason
# -- change from Season 1 to season 2

def index(request):
    context={
        'schedule': Schedule.objects.all(),
        'myTeam': Team.objects.get(team_num=1),
        'weekNum': Settings.objects.last().week_num,
        'seasonNum': Settings.objects.last().season_num,
        'finalCompleted': Schedule.objects.last().result
    }
    return render(request, 'sportApp/index.html', context)

##LOGIC
def updateWeek(request):
    if Schedule.objects.filter(week_num=Settings.objects.first().week_num).last().result == None:
        return redirect('/Homepage')

    updateWeek = Settings.objects.first()
    updateWeek.week_num+=1
    updateWeek.save()
    return redirect('/Homepage')

##LOGIC
def simEntireSeason(request):
    if Schedule.objects.filter(week_num=Settings.objects.first().week_num).last().result != None:
        updateWeek = Settings.objects.first()
        updateWeek.week_num+=1
        updateWeek.save()
    currWeek = Settings.objects.first().week_num
    lastWeek = Schedule.objects.last().week_num
    for week in range(currWeek, lastWeek+1):
        if week == lastWeek:
            updateWeek = Settings.objects.first()
            updateWeek.week_num=week
            updateWeek.save()
        weeklyMatchUps = Schedule.objects.filter(week_num=week)
        for matchUp in weeklyMatchUps:
            homeScoreKeeper = 0
            awayScoreKeeper = 0
            homeTeam = Team.objects.get(team_num=matchUp.home_team)
            awayTeam = Team.objects.get(team_num=matchUp.away_team)
            for x in range(65):
                if round(65-(100-homeTeam.ability)*32/40) >= x: #TAKE INTO ACCOUNT THE NUMBER OF ATTEMPTS TO SCORE POINTS -- THE FIRST FROM 100 THE ABILITY IS THE LESS ATTEMPTS AT A RATIO OF 32/40 (MAX:100 = 65; MIN:60 = 33)
                    score = Decimal(random.random())
                    homeScoreKeeper += round(score*((homeTeam.ability/Decimal(100.00)*Decimal(1.15)))) #PER SCORING ATTEMPT: TEAMS ABILITY WITH MULTIPLIER DETERMINES TEAMS SCORE  
                if round(65-(100-awayTeam.ability)*32/40) >= x:
                    score = Decimal(random.random())
                    awayScoreKeeper += round(score*((awayTeam.ability/Decimal(100.00)*Decimal(1.15))))
                if round(65-(100-homeTeam.ability)*32/40) <=x and  round(65-(100-awayTeam.ability)*32/40) <= x:
                    break;
            if (homeTeam.ability < awayTeam.ability and homeScoreKeeper > awayScoreKeeper or homeTeam.ability > awayTeam.ability and homeScoreKeeper < awayScoreKeeper) and homeTeam.ability - awayTeam.ability >= 5:
                print(homeScoreKeeper, ':', homeTeam.team_name, ' ', homeTeam.ability, ' vs. ', awayScoreKeeper, ':', awayTeam.team_name, ' ', awayTeam.ability)
            matchUp.home_score = homeScoreKeeper
            matchUp.save()
            matchUp.away_score = awayScoreKeeper
            matchUp.save()
            if matchUp.home_score > matchUp.away_score:
                matchUp.result = 0
                matchUp.save()
                winner = Standings.objects.get(id=matchUp.home_team)
                loser = Standings.objects.get(id=matchUp.away_team)
                winner.pts_for += matchUp.home_score
                winner.pts_against += matchUp.away_score
                loser.pts_for += matchUp.away_score
                loser.pts_against += matchUp.home_score
                winner.wins+=1
                loser.losses+=1
                winner.save(update_fields=['wins', 'pts_for', 'pts_against'])
                loser.save(update_fields=['losses', 'pts_for', 'pts_against'])
                winner.win_pct = winner.wins/(winner.wins+winner.losses)
                loser.win_pct = loser.wins/(loser.wins+loser.losses)
                winner.save()
                loser.save()

            elif matchUp.home_score < matchUp.away_score:
                matchUp.result = 1
                matchUp.save()
                winner = Standings.objects.get(id=matchUp.away_team)
                loser = Standings.objects.get(id=matchUp.home_team)
                winner.pts_for += matchUp.away_score
                winner.pts_against += matchUp.home_score
                loser.pts_for += matchUp.home_score
                loser.pts_against += matchUp.away_score
                winner.wins+=1
                loser.losses+=1
                winner.save(update_fields=['wins', 'pts_for', 'pts_against'])
                loser.save(update_fields=['losses', 'pts_for', 'pts_against'])
                winner.win_pct = winner.wins/(winner.wins+winner.losses)
                loser.win_pct = loser.wins/(loser.wins+loser.losses)
                winner.save()
                loser.save()
            else:
                matchUp.result = 2
                matchUp.save()
                tie1 = Standings.objects.get(id=matchUp.home_team)
                tie2 = Standings.objects.get(id=matchUp.away_team)
                tie1.pts_for += matchUp.home_score
                tie1.pts_against += matchUp.away_score
                tie2.pts_for += matchUp.away_score
                tie2.pts_against += matchUp.home_score
                tie1.ties+=1
                tie2.ties+=1
                tie1.save(update_fields=['ties', 'pts_for', 'pts_against'])
                tie2.save(update_fields=['ties', 'pts_for', 'pts_against'])
                if tie1.wins+tie1.losses == 0:
                    tie1.win_pct = 0
                else:    
                    tie1.win_pct = tie1.wins/(tie1.wins+tie1.losses)
                if tie2.wins+tie2.losses == 0:
                    tie2.win_pct = 0
                else:    
                    tie2.win_pct = tie2.wins/(tie2.wins+tie2.losses)
                tie1.save()
                tie2.save()


    return redirect('/Homepage')
    
def seeGame(request):
    teamCount = Settings.objects.first().numOfTeams
    context={
        'weekNum': Settings.objects.last().week_num, 
        'myTeam': Team.objects.get(team_num=1),
        'myMatch': Schedule.objects.get(Q(home_team=1) | Q(away_team=1), week_num=Settings.objects.first().week_num),
        'standings': Standings.objects.all(),
        'teams': Team.objects.all().order_by('team_num')[:teamCount],
    }
    return render(request, 'sportApp/simulation.html', context)

##LOGIC
def simGame(request):
    weeklyMatchUps = Schedule.objects.filter(week_num=Settings.objects.first().week_num) 
    for matchUp in weeklyMatchUps:
        homeScoreKeeper = 0
        awayScoreKeeper = 0
        homeTeam = Team.objects.get(team_num=matchUp.home_team)
        awayTeam = Team.objects.get(team_num=matchUp.away_team)
        for x in range(65):
            if round(65-(100-homeTeam.ability)*32/40) >= x: #TAKE INTO ACCOUNT THE NUMBER OF ATTEMPTS TO SCORE POINTS -- THE FIRST FROM 100 THE ABILITY IS THE LESS ATTEMPTS AT A RATIO OF 32/40 (MAX:100 = 65; MIN:60 = 33)
                score = Decimal(random.random())
                homeScoreKeeper += round(score*((homeTeam.ability/Decimal(100.00)*Decimal(1.15)))) #PER SCORING ATTEMPT: TEAMS ABILITY WITH MULTIPLIER DETERMINES TEAMS SCORE  
            if round(65-(100-awayTeam.ability)*32/40) >= x:
                score = Decimal(random.random())
                awayScoreKeeper += round(score*((awayTeam.ability/Decimal(100.00)*Decimal(1.15))))
            if round(65-(100-homeTeam.ability)*32/40) <=x and  round(65-(100-awayTeam.ability)*32/40) <= x:
                print('home', homeScoreKeeper, 'away', awayScoreKeeper, x)
                break;
        if homeTeam.ability < awayTeam.ability and homeScoreKeeper > awayScoreKeeper or homeTeam.ability > awayTeam.ability and homeScoreKeeper < awayScoreKeeper:
                print(homeScoreKeeper, ':', homeTeam.team_name, ' ', homeTeam.ability, ' vs. ', awayScoreKeeper, ':', awayTeam.team_name, ' ', awayTeam.ability)

        matchUp.home_score = homeScoreKeeper
        matchUp.save()
        matchUp.away_score = awayScoreKeeper
        matchUp.save()
        if matchUp.home_score > matchUp.away_score:
            matchUp.result = 0
            matchUp.save()
            winner = Standings.objects.get(id=matchUp.home_team)
            loser = Standings.objects.get(id=matchUp.away_team)
            winner.pts_for += matchUp.home_score
            winner.pts_against += matchUp.away_score
            loser.pts_for += matchUp.away_score
            loser.pts_against += matchUp.home_score
            winner.wins+=1
            loser.losses+=1
            winner.save(update_fields=['wins', 'pts_for', 'pts_against'])
            loser.save(update_fields=['losses', 'pts_for', 'pts_against'])
            winner.win_pct = winner.wins/(winner.wins+winner.losses)
            loser.win_pct = loser.wins/(loser.wins+loser.losses)
            winner.save()
            loser.save()

        elif matchUp.home_score < matchUp.away_score:
            matchUp.result = 1
            matchUp.save()
            winner = Standings.objects.get(id=matchUp.away_team)
            loser = Standings.objects.get(id=matchUp.home_team)
            winner.pts_for += matchUp.away_score
            winner.pts_against += matchUp.home_score
            loser.pts_for += matchUp.home_score
            loser.pts_against += matchUp.away_score
            winner.wins+=1
            loser.losses+=1
            winner.save(update_fields=['wins', 'pts_for', 'pts_against'])
            loser.save(update_fields=['losses', 'pts_for', 'pts_against'])
            winner.win_pct = winner.wins/(winner.wins+winner.losses)
            loser.win_pct = loser.wins/(loser.wins+loser.losses)
            winner.save()
            loser.save()

        else:
            matchUp.result = 2
            matchUp.save()
            tie1 = Standings.objects.get(id=matchUp.home_team)
            tie2 = Standings.objects.get(id=matchUp.away_team)
            tie1.pts_for += matchUp.home_score
            tie1.pts_against += matchUp.away_score
            tie2.pts_for += matchUp.away_score
            tie2.pts_against += matchUp.home_score
            tie1.ties+=1
            tie2.ties+=1
            tie1.save(update_fields=['ties', 'pts_for', 'pts_against'])
            tie2.save(update_fields=['ties', 'pts_for', 'pts_against'])
            if tie1.wins+tie1.losses == 0:
                tie1.win_pct = 0
            else:    
                tie1.win_pct = tie1.wins/(tie1.wins+tie1.losses)
            if tie2.wins+tie2.losses == 0:
                tie2.win_pct = 0
            else:    
                tie2.win_pct = tie2.wins/(tie2.wins+tie2.losses)
            tie1.save()
            tie2.save()
    
    
    # print(Schedule.objects.all())
    return redirect('/seeGame')

def seeSchedule(request, teamId):
    teamCount = Settings.objects.first().numOfTeams
    context={
        'Schedule': Schedule.objects.all(),
        'Teams': Team.objects.all().order_by('team_num')[:teamCount],
        'teamId': int(teamId),
        'teamInfo': Team.objects.get(team_num=teamId),
        'numOfTeams': Settings.objects.first().numOfTeams,
        'myTeam': Team.objects.get(team_num=1),
    }
    return render(request, 'sportApp/schedule.html', context)

def refreshSchedule(request):
    teamId = request.POST['teamId']
    return redirect('/seeSchedule/'+teamId)

def seeStandings(request):
    teamCount = Settings.objects.first().numOfTeams
    context={
        'standings': Standings.objects.all().order_by('-win_pct', '-pts_for')[:teamCount],
        'historic': historicalStandings.objects.all().order_by('-win_pct', '-pts_for')[:teamCount],
        'teams': Team.objects.all().order_by('team_num')[:teamCount],
    }
    return render(request, 'sportApp/standings.html', context)

def seeRoster(request, teamId):
    teamCount = Settings.objects.first().numOfTeams
    context={
        'roster': Players.objects.all().order_by('-ability', 'team', 'year'),
        'Teams': Team.objects.all().order_by('team_num')[:teamCount],
        'teamId': int(teamId),
        'teamInfo': Team.objects.filter(team_num=teamId),
        'numOfTeams': Settings.objects.first().numOfTeams,
        'myTeam': Team.objects.get(team_num=1),
    }
    return render(request, 'sportApp/roster.html', context)

def refreshRoster(request):
    teamId = request.POST['teamId']
    return redirect('/seeRoster/'+teamId)

##LOGIC
def randomizeTeams(team_num):
    team = Team.objects.get(team_num=team_num)
    if team.team_num != 1: #TEAM SELECTED WILL BE team_num 1 TO ALLOW CONSISTENCE FOR FUTURE CODE PROCESSES
        tempTeam = Team.objects.get(team_num=1)
        myTeam = Team.objects.get(team_num=team.team_num) 
        myTeam.team_num = 1 
        myTeam.save()
        tempTeam.team_num = team.team_num #
        tempTeam.save()

    newId = [] #RANDOMIZE THE OTHER TEAM team_num TO ALLOW DIVERSITY IN SCHEDULING MATCHUPS
    for _id in range(2,17):
        newId.append([_id,random.random()])
    
    for x in range(len(newId)-1):
        for i in range(len(newId)-1):
            if newId[i][1]>newId[i+1][1]:
                newId[i],newId[i+1] = newId[i+1],newId[i]

    for reassignTeam in range(2,15):
        fromTeam = Team.objects.get(team_num=reassignTeam)
        toTeam = Team.objects.get(team_num=newId[reassignTeam-1][0])
        fromTeam.team_num = newId[reassignTeam-1][0]
        toTeam.team_num = reassignTeam
        fromTeam.save()
        toTeam.save()


    print(Team.objects.all())

##LOGIC
def createRoster(teamCount):
    teams = Team.objects.all().order_by('team_num')[:teamCount]
    for team in teams:
        for player in range(15): ##ADD 15 PLAYERS TO EACH TEAM
            year = random.randint(1,4)
            if year == 1:
                ability = 60 + round(10*random.random())
            elif year == 2:
                ability = 65 + round(10*random.random())
            elif year == 3:
                ability = 75 + round(15*random.random())
            elif year == 4:
                ability = 85 + round(15*random.random())
            Players.objects.create(name='N/A', year=year, position='N/A', ability=ability, team=Team.objects.get(team_num=team.team_num))

        allPlayers = Players.objects.filter(team=Team.objects.get(team_num=team.team_num)).order_by('-ability')[:10] ##FIND AVERAGE OF STARTING LINE-UP (TOP 10 PLAYERS)
        averageAbility = allPlayers.aggregate(Avg('ability'))
        team.ability = averageAbility['ability__avg']
        team.save()

##LOGIC
def generateSchedule(request):
    # if Settings.objects.last().season_num != 1: #FOR FIRST TIME RUNNING
    Settings.objects.create(numOfTeams=int(request.POST['numOfTeams']), myTeam=int(request.POST['myTeam']), week_num=1, season_num=1)
    # print(Settings.objects.first().myTeam, Settings.objects.first().numOfTeams)
    randomizeTeams(Settings.objects.first().myTeam) #CHANGE THE TEAM ORDER FOR DYNAMIC SCHEDULING
    print("Randomization Completed")
    numOfTeams = Settings.objects.first().numOfTeams
    scheduleGrid = []
    weeklyGrid = []
    for x in range(numOfTeams):  # Create a grid for all matches to be played
        scheduleGrid.append([])
        weeklyGrid.append([])

    allMatches = []
    for home in range(1, numOfTeams+1):  # Insert all matches to be played
        for away in range(1, numOfTeams+1):
            allMatches.append([home, away])

    match = 0
    team = 1
    for x in range(len(scheduleGrid)):
        while match < len(allMatches):
            if allMatches[match][0] != team and scheduleGrid[x][len(scheduleGrid) - 1] != None:
                break

            if allMatches[match][0] != allMatches[match][1]:
                scheduleGrid[x].append(allMatches[match])
                weeklyGrid[x].append([])

            else:
                scheduleGrid[x].append(None)
                weeklyGrid[x].append([])

            match += 1

        team += 1

    matchesToPlay = pow(numOfTeams, 2) - numOfTeams
    matchesPerWeek = int(numOfTeams / 2)
    weeks = int(matchesToPlay / matchesPerWeek)

    for nullValue in range(numOfTeams):
        weeklyGrid[nullValue][nullValue].append(None)


    x = 0
    for weekCount in range(1, int(weeks)+1):
        for row in range(len(weeklyGrid)):
            for col in range(len(weeklyGrid[row])):
                if row == col:
                    continue
                rowTotal = 0
                for tempCol in range(numOfTeams):
                    if len(weeklyGrid[row][tempCol]) != 0 and weeklyGrid[row][tempCol][0] != None:
                        rowTotal += 1
                colTotal = 0
                for tempRow in range(numOfTeams):
                    if len(weeklyGrid[tempRow][col]) != 0 and weeklyGrid[tempRow][col][0] != None:
                        colTotal += 1
                if rowTotal == weekCount:
                    break
                if colTotal == weekCount:
                    continue
                if row > col:
                    continue
                if len(weeklyGrid[row][col]) == 0:
                    weeklyGrid[row][col].append(weekCount)
                    weeklyGrid[col][row].append(
                        int(weekCount + ((pow(numOfTeams, 2) - numOfTeams) / (numOfTeams / 2) / 2)))
                    break

    for homeTeam in range(numOfTeams):
        for awayTeam in range(numOfTeams):
            if scheduleGrid[homeTeam][awayTeam] == None:
                continue
            scheduleGrid[homeTeam][awayTeam].append(
                weeklyGrid[homeTeam][awayTeam][0])

    leagueSchedule = []
    for weekCount in range(1, weeks+1):
        matchesConfirmed = 0
        for homeTeam in range(numOfTeams): #Row
            for awayTeam in range(numOfTeams): #Col
                if scheduleGrid[homeTeam][awayTeam] != None:
                    if scheduleGrid[homeTeam][awayTeam][2] == weekCount:
                        leagueSchedule.append(scheduleGrid[homeTeam][awayTeam])
                        matchesConfirmed += 1
                        #if scheduleGrid[homeTeam][awayTeam][0] or [1] == homeTeam break awayTeam FOR
                        if scheduleGrid[homeTeam][awayTeam][0] == homeTeam+1 or scheduleGrid[homeTeam][awayTeam][1] == homeTeam+1:
                            break
                if matchesConfirmed == matchesPerWeek:
                    break
            if matchesConfirmed == matchesPerWeek:
                break

    for matchUp in leagueSchedule:
        Schedule.objects.create(home_team=matchUp[0], away_team=matchUp[1], week_num=matchUp[2])

    createRoster(numOfTeams)

    return redirect('/Homepage')

def recruits(request):
    pass

def seePlayoffs(request):
    pass




    

        



