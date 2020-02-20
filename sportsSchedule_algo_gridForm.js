numOfTeams = 16

scheduleGrid = []
weeklyGrid = []
for (x = 0; x < numOfTeams; x++) {
    scheduleGrid.push([])
    weeklyGrid.push([])
} //Create a grid for all matches to be played

allMatches = []
for (var home = 1; home <= numOfTeams; home++) {
    for (var away = 1; away <= numOfTeams; away++) {
        // if (home != away) {
        allMatches.push([home, away])

        // schedule.push([away, home])
        // }
    }
}//Insert all matches to be played

// console.log(allMatches)

var match = 0
var team = 1
for (x = 0; x < scheduleGrid.length; x++) {
    while (match < allMatches.length) {
        if (allMatches[match][0] != team && scheduleGrid[x][scheduleGrid.length - 1] != null) {
            break;
        }
        if (allMatches[match][0] != allMatches[match][1]) {
            scheduleGrid[x].push(allMatches[match])
            weeklyGrid[x].push([])
        }
        else {
            scheduleGrid[x].push(null)
            weeklyGrid[x].push([])
        }
        match++
    }
    team++
}
// matchSetupCount = 0
matchesToPlay = Math.pow(numOfTeams, 2) - numOfTeams
matchesPerWeek = numOfTeams / 2
weeks = matchesToPlay / matchesPerWeek

for (nullValue = 0; nullValue < numOfTeams; nullValue++) {
    weeklyGrid[nullValue][nullValue].push(null);
}

for (weekCount = 1; weekCount <= weeks / 2; weekCount++) {
    for (row = 0, RWlength = weeklyGrid.length; row < RWlength; row++) {
        for (col = 0, CLlength = weeklyGrid[row].length; col < CLlength; col++) {
            if (row == col) {
                continue;
            }
            rowTotal = 0
            for (tempCol = 0, CLlength = weeklyGrid[row].length; tempCol < CLlength; tempCol++) {
                if (weeklyGrid[row][tempCol][0] != "" && weeklyGrid[row][tempCol][0] != null) {
                    rowTotal++
                }
            }
            colTotal = 0
            for (tempRow = 0, RWlength = numOfTeams; tempRow < RWlength; tempRow++) {
                if (weeklyGrid[tempRow][col][0] != "" && weeklyGrid[tempRow][col][0] != null) {
                    colTotal++
                }
            }
            if (rowTotal == weekCount) {
                break;
            }
            if (colTotal == weekCount) {
                continue;
            }
            if (row > col) {
                continue;
            }
            if (weeklyGrid[row][col] == "") {
                weeklyGrid[row][col].push(weekCount);
                weeklyGrid[col][row].push(weekCount + ((Math.pow(numOfTeams, 2) - numOfTeams) / (numOfTeams / 2) / 2));
                break;
            }
        }
    }
}

for (homeTeam = 0; homeTeam < numOfTeams; homeTeam++) {
    for (awayTeam = 0; awayTeam < numOfTeams; awayTeam++) {
        if (scheduleGrid[homeTeam][awayTeam] == null) {
            continue;
        }
        scheduleGrid[homeTeam][awayTeam].push(weeklyGrid[homeTeam][awayTeam][0])
    }
}

leagueSchedule = []
for (weekCount = 1; weekCount <= weeks; weekCount++) {
    matchesConfirmed = 0
    for (homeTeam = 0; homeTeam < numOfTeams; homeTeam++) {
        for (awayTeam = 0; awayTeam < numOfTeams; awayTeam++) {
            if (scheduleGrid[homeTeam][awayTeam] != null) {
                if (scheduleGrid[homeTeam][awayTeam][2] == weekCount) {
                    leagueSchedule.push(scheduleGrid[homeTeam][awayTeam])
                    homeTeam++
                    awayTeam = -1
                    matchesConfirmed++
                }
            }
            if (matchesConfirmed == matchesPerWeek) {
                break;
            }
        }
        if (matchesConfirmed == matchesPerWeek) {
            break;
        }
    }
}
print(leagueSchedule)




// scheduleGrid
// weeklyGrid

/*
Loop through week counter [starting at 1]:
loop through each row
    loop through each row's Columns
        is ROW# == COL#
            (yes) set to NULL; break to next COL
        is current ROW#TOTAL == currentWeek? (what if it is less than currentWeek-1??) set these to variables and add incrementally: for(x=0;x<weeklyGrid[row].legnth;x++){if(weeklyGrid[row][x]!=null&&weeklyGrid[row][x]!=''){total}}
            (yes): set total == 0 break to next ROW; (this means the row has been accounted for)
        is the ROW# > COL#?
            (yes): loop to next COLUMN#
        is current position in weeklyGrid empty? (does the number == current week? break to next ROW#)??
            (yes):fill current spot on weeklyGrid with current week#; break to next ROW (find reverse position weeklyGrid[1][2] becomes weeklyGrid[2][1] and fill **week+1+((POW(number,2)-number)/(number/2)/2)** will calulated week )
        (no): loop next COLUMN#


*/

