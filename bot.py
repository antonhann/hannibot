import discord
import cass
import download

def handleResponse(message: str) -> str:
    #fixes user input to work with my code based off what is given
    msg = message.lower() if not message[:7] == "download" else message
    seperated = msg.split(" ")
    command = seperated[0].lower()
    ign = msg[len(command):] #IN GAME NAME

    #list of commands that require specific conditions/exceptions
    oneLineCommands = ['!help', "randomchamp"]
    userCheckCommands = ["scan", "champ", "rank", "winrate"]

    #checks whether the user is properly using the commands and the information given
    if len(seperated) == 1 and msg not in oneLineCommands:
        return "use hanni bot correctly !help"
    if command in userCheckCommands:
        if not cass.checkUser(ign):
            return "user does not exists"

    #scans the IGN's current match and prints the participants in the game and their rank
    if command == 'scan':
        # sendMessage('loading...')
        response = cass.getCurrentMatchData(ign)
        return response

    #returns the IGN's top five champions based on mastery points
    if command == "champ":
        champs = cass.getTopChampions(ign)
        repsonse = ""
        for i in champs:
            repsonse += i + ' '
        return repsonse

    #returns the IGN's rank 
    if command == "rank":
        rank = cass.getSummonerRank(ign)
        if rank is None:
            rank = "Unranked"
        return f"{ign} is {rank}"

    #returns the tips of the champion provided based on if it is an ally or enemy
    if command == "tips":
        if len(seperated) != 3:
            return "!help for formatting"
        typeOf = seperated[1]
        champName = seperated[2]
        return cass.getChampTips(typeOf, champName)

    #return a random champion
    if command == "randomchamp":
        return cass.getRandomChampion()
    
    #returns the winrate of the past number of games(default = 5)
    if command == "winrate":
        return cass.summonerWinRate(ign)
    
    #directly downloads the youtube mp3 and puts it directly in my directory (personal use)
    if command == "download":
        return download.youtube2mp3(ign)
    
    #prints to the user the proper formatting for the command
    if command == '!help':
        commands = []
        commands.append('scan current league game: "scan (insert ign)"')
        commands.append('for top 5 champions of summoner: "champ (insert ign)"')
        commands.append('for rank of summoner: "rank (insert ign)"')
        commands.append('for winrate(recent 5 games) of summoner: "winrate (insert ign)"')
        commands.append('for random champion: "randomchamp"')
        commands.append('for enemy/ally champion tips: "tips (enemy or ally) (champion name)')
        commands.append('for yt to mp3: "download (insert link)"')
        help = ''
        for i, command in enumerate(commands):
            if i == len(commands) - 1:
                help += command + "\n"
            else: 
                help += command + "\n\n"
        return help
    return "try !help"


async def sendResponse(message, userMessage):
    try:
        response = handleResponse(userMessage)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    with open("discordapi.txt") as file:
        TOKEN = file.read()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        #everytime a message is sent in the server the hanni bot responds based on what was given
        if message.author == client.user:
            return
        username = str(message.author)
        userMessage = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{userMessage}" ({channel})')
        await sendResponse(message, userMessage)
    
    client.run(TOKEN)


