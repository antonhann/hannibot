import random
from collections import Counter
import cassiopeia as cass
from cassiopeia import Champion, Champions
from datapipelines import NotFoundError

with open("riotapi.txt") as file:
    riotKey = file.read()
cass.set_riot_api_key(riotKey)  # This overrides the value set in your configuration/settings.
# summoner = cass.get_summoner(name="newjeansenjoyer", region="NA")

def summonerObject(ign):
    #to take ign argument and create it as a summoner class using cassiopeia
    return cass.get_summoner(name=f"{ign}", region="NA")

def getCurrentMatchData(ign):
    summoner = summonerObject(ign)
    #function creates a dictionary of the participants user name in the IGN's current game (if they are in one) to the participants rank and returns the information to the user.
    try:
        participants = {}
        current_match = summoner.current_match
        if current_match.exists:
            for i in current_match.participants:
                name = i.summoner.name
                player = cass.get_summoner(name=f"{name}", region="NA")
                participants[name] = getSummonerRank(name)
        response = ''
        count = 0
        for participant, rank in participants.items():
            if count == 5:
                response += "\n"
            response += f"{participant}: {rank}\n"
            count += 1
        return response
    except:
        return "either user not in game/ or my bot sucks"

def getSummonerRank(ign):
    #returns the IGN's rank of the current season
    summoner = summonerObject(ign)
    entries = summoner.league_entries
    for position in entries:
        return (f"{position.tier} {position.division}")

def getTopChampions(ign):
    #returns the top 5 champions the user plays based of their mastery points
    summoner = summonerObject(ign)
    result = []
    champions = summoner.champion_masteries[:5]
    for i, champ in enumerate(champions, start = 1):
        result.append(f"{i}. {champ.champion.name}\n")
    return result
def getRandomChampion():
    #collects data of all the champions in the game and used the random library to return a random champion
    champions = cass.get_champions(region = "NA")
    randomChampion = random.choice(champions)
    return randomChampion.name

def checkUser(ign):
    #checks whether the user exists in riot's database
    summoner = summonerObject(ign)
    return summoner.exists

def getPastNumberofMatches(summoner, games = 5):
    #returns the past number of games(default = 5)
    matchHistory = summoner.match_history
    pastMatches = []
    for match in matchHistory:
        if len(pastMatches) == games:
            break
        pastMatches.append(match)
    return pastMatches

def summonerWinRate(ign, games = 5):
    #returns the winrate of the user of certain number of games (default = 5)
    summoner = summonerObject(ign)
    matches = getPastNumberofMatches(summoner, games)
    wins = 0
    lost = 0
    for i in matches:
        win = (i.participants[summoner].stats.win)
        if win:
            wins += 1
        else:
            lost += 1
    winrate = f"{summoner.name} has won {wins} and lost {lost} in their past {len(matches)} recent games."
    return winrate

def getChampTips(typeOf, championName):
    #returns the champion tips based on whether the champion is an ally or an enemy
    championName = championName.replace("'","").replace(".","").title()
    #fix is to fix the user's input in order to properly work with the database
    fix = {
        "Leblanc": "LeBlanc",
        "Chogath": "Cho'Gath",
        "Drmundo": "Dr. Mundo",
        "Jarvan": "Jarvan IV",
        "Kaisa": "Kai'sa",
        "Khazix": "Kha'Zix",
        "Kogmaw": "Kog'Max",
        "Ksante": "K'Sante",
        "Lee": "Lee Sin",
        "Miss": "Miss Fortune",
        "Master": "Master Yi",
        "Nunu": "Nunu & Willump",
        'Reksai': "Rek'Sai",
        "Renata": "Renata Glasc",
        "Tahm": "Tahm Kench",
        "Twisted": "Twisted Fate",
        "Velkoz": "Vel'Koz",
        "Xin": "Xin Zhao",
    }

    #below fixes the user's input and checks whether the champion actually exist in the database
    championName = championName if championName not in fix else fix[championName]
    allChampions = cass.get_champions(region="NA")
    result = []
    for i in allChampions:
        result.append(i.name)
    if championName not in result:
        return "Champion does not exist!"

    #Lastly grabs cassiopeia's database of tips for each champion and returns a random tips of the one provided
    champion = Champion(name = f"{championName}", region = "NA")
    tips = champion.ally_tips if typeOf.lower() == "ally" else champion.enemy_tips
    return random.choice(tips)

# if __name__ == "__main__":
#     print(getChampTips("ally", "Xina"))
