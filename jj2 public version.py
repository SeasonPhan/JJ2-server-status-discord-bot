import discord
import asyncio
import requests
import configparser

# Config:
config = configparser.ConfigParser()
config.read('config.ini')

BOT = config['BOT']
token = BOT['token']
apiUrl = BOT['apiUrl']
api2Url = BOT['api2Url']

# updateInSec
updateInterval = 5
client = discord.Client()

# Print the starting text
print('Jazz JackRabbit server status')
print('Starting Bot...')

try:
    async def updateStatusPresence():        
        await client.wait_until_ready()
        offlinecheck = 0
        while not client.is_closed():
            url2 = api2Url
            resp2 = requests.get(url=url2)
            data2 = resp2.json()
            url = apiUrl
            resp = requests.get(url=url)
            data = resp.json()
            offlinestatus = data["error"]
            if offlinestatus == 2:
                offlinecheck +=1
                if offlinecheck == 3:
                    game = discord.Game(name="Server offline")
                    await client.change_presence(status=discord.Status.dnd, activity=game)
                    offlinecheck = 0
            else:
                gmstr = "none"
                cm = data2["plus"]["customMode"]
                gm = data2["gamemode"]
                if gm == 0 or gm == 1:
                    gmstr = "Co-op"
                elif gm == 2:
                    if cm == 0: 
                        gmstr = "Battle"
                    if cm == 1: 
                        gmstr = "RoastTag"
                    if cm == 2: 
                        gmstr = "BattleRoyale"
                    if cm == 3: 
                        gmstr = "BattleRoyale+"
                    if cm == 4: 
                        gmstr = "Zombies"
                elif gm == 5:
                    if cm == 0:
                        gmstr = "CTF"
                    if cm == 11:
                        gmstr = "TeamBattle"
                    if cm == 12:
                        gmstr = "Jailbreak"
                    if cm == 13:
                        gmstr = "DeathCTF"
                    if cm == 14:
                        gmstr = "FlagRun"
                    if cm == 15:
                        gmstr = "T.BattleRoyale"
                    if cm == 16:
                        gmstr = "Domination"
                    if cm == 17:
                        gmstr = "HeadHunters"
                elif gm == 3:
                    gmstr = "Race"
                elif gm == 4:
                    gmstr = "Treasure"
                players = data["capacity"][0]
                maxPlayers = data["capacity"][1]
                if players == 1:
                    game = discord.Game(name= str(players) + "/" + str(maxPlayers) + " [" + str(gmstr) + "]")
                    await client.change_presence(status=discord.Status.idle, activity=game)
                else:
                    game = discord.Game(name= str(players) + "/" + str(maxPlayers) + " [" + str(gmstr) + "]")
                    await client.change_presence(status=discord.Status.online, activity=game)

            await asyncio.sleep(updateInterval)
    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print('------')

        # Create task to update status
        client.loop.create_task(updateStatusPresence())
        
except Exception as e:
    print(e)

# Start bot
client.run(token)