numOfTeams = 6

function createSchedule(numOfTeams) { //EACH TEAM SHOULD EVERYONE (HOME && AWAY) TOTAL#OFMATCHES = numOfTeams^2-numOfTeams
    allMatches = []
    for (var home = 1; home <= numOfTeams; home++) {
        for (var away = 1; away <= numOfTeams; away++) {
            if (home != away) {
                allMatches.push([home, away])
                // schedule.push([away, home])
            }
        }
    }
    matchSetupCount = 0
    matchesToPlay = Math.pow(numOfTeams, 2) - numOfTeams
    matchesPerWeek = numOfTeams / 2
    weeks = matchesToPlay / matchesPerWeek
    console.log(matchSetupCount)
    console.log(matchesToPlay)
    console.log(matchesPerWeek)
    console.log(weeks)

    for (var wk = 1; wk <= weeks; wk++) {
        allTeam = [] //EACH WEEK A MATCH INCLUDE EVERY TEAM MUST BE PLACED, BUT EACH TEAM MUST ONLY PLAY 1 MATCH A WEEK
        for (i = 1; i <= numOfTeams; i++) {
            allTeam.push(i)
        }
        matchesConfirmed = 0
        matchAssigned = false
        // for (var match = 0; match < matchesPerWeek; match++) { //WITH EVERY TEAM PLAYING A MATCH: ONLY (numOfTeams/2) MATCHES WILL BE ASSIGNED PER WEEK 
        for (var allMatchCycle = 0; allMatchCycle < matchesToPlay; allMatchCycle++) {
            teamIndexes = [];
            matchSetupCount = 0
            if (allMatches[allMatchCycle].length < 3) {
                for (var verifyIndex = 0, availTeams = allTeam.length; verifyIndex < availTeams; verifyIndex++) {
                    //HOW TO PREVENT REPEATING WEEKS FOR SAME TEAM!!
                    //5,2 AND 5,3
                    //2,4 AND 2,6
                    if (allMatches[allMatchCycle][0] == allTeam[verifyIndex] || allMatches[allMatchCycle][1] == allTeam[verifyIndex]) {
                        teamIndexes.push(verifyIndex) //AS THE AVAILABLE TEAMS ARE FOUND, THEY WILL BE REMOVED FROM THE LIST OF TEAMS NEEDING TO BE ASSIGNED TO A MATCH FOR THE WEEK
                        matchSetupCount++
                        if (matchSetupCount == 2) { //ONCE WE DETERMINE BOTH TEAMS OF A MATCH ARE AVAILABLE TO PLAY, THEN WE WILL REMOVE THEM FROM THE AVAILABLE LIST AND FINALLY ASSIGN THE MATCH A WEEK TO BE PLAYED
                            for (var teamToRemove = 1; teamToRemove >= 0; teamToRemove--) {
                                // console.log('WEEK: ', wk,'match ', allMatches[allMatchCycle], 'availableTeam ', allTeam, 'teamIndex ', teamIndexes, 'matchSetUp ', matchSetupCount, 'allTeamLEN: ', allTeam.length)
                                if (allTeam.length > 1) {
                                    for (var allTeamRemoval = teamIndexes[teamToRemove], x = allTeam.length - 1; allTeamRemoval < x; allTeamRemoval++) {
                                        temp = allTeam[allTeamRemoval]
                                        allTeam[allTeamRemoval] = allTeam[allTeamRemoval + 1]
                                        allTeam[allTeamRemoval + 1] = temp
                                    }
                                }
                                allTeam.pop()
                            }
                            allMatches[allMatchCycle].push(wk) //ADDING THE WEEK THIS MATCH IS PLAYED TO THE allMatches
                            matchesConfirmed++
                            matchAssigned = true
                        }
                        if (matchAssigned == true) {
                            matchAssigned = false
                            break;
                        }
                    }
                }
            }
            if (matchesConfirmed == matchesPerWeek) {
                break;
            }
        }
        // }
    }

    for (i = 0; i < allMatches.length; i++) {
        if (allMatches[i].length == 3) {
            allMatches[i].push(Math.random())
        }
    }

    orderedLeague = []

    for (var byWeek = 1; byWeek <= weeks; byWeek++) {
        for (i = 0; i < allMatches.length; i++) {
            if (allMatches[i].length == 4) {
                if (allMatches[i][2] == byWeek) {
                    orderedLeague.push(allMatches[i])
                }
            }
        }
    }
    return orderedLeague
}
array = createSchedule(numOfTeams)
// console.log(leagueSchedule)

// array = [5, 6, 3, 1, 8, 7, 2, 4]
// randomOrder = []

// for (i = 0; i < array.length; i++) {
//     console.log(array[i])
//     randomOrder.push([array[i], Math.random()])
// }

for (x = 0; x < array.length; x++) {
    for (i = 0; i < array.length - 1; i++) {
        if (array[i][3] < array[i + 1][3]) {
            temp = array[i]
            array[i] = array[i + 1]
            array[i + 1] = temp
        }
    }
}

for (x = 0; x < array.length; x++) {
    array[x].pop()
}
console.log(array)

