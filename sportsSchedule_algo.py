

def generateSchedule(numOfTeams):
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
            scheduleGrid[homeTeam][awayTeam].append(weeklyGrid[homeTeam][awayTeam][0])

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
    return leagueSchedule

numOfTeams = 16
Schedule  = generateSchedule(numOfTeams)
print(len(Schedule))