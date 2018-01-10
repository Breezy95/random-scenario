import discord
import asyncio
import random
import time
from discord.ext import commands
from assets import Enemy
from assets import Player



#Global Game Variables
#---------------------------------
global EnemyList
EnemyList = []
global PlayerList
Player = []
#The name of the txt file that you want to be loaded
global ScenarioName
ScenarioName = ""
#Determines if their is a game currently running
global isPlaying
isPlaying = False
#Timer declares the amount of time each player will have during their turn. Can be Adjusted in the text file Via Timer <amount of time> on a line
global Timer
Timer = 60
#Minimum amount of players needed to start the scenario. Can be Adjuseted in the text file Via MinPlayers <Amount of players> on a line
global MinPlayers
MinPlayers = 1

#-----------------------------------
newplayer = Player("Jobo",100,100,100," ",False)
                       
def Clear(): 
       global EnemyList
       global PlayerList
       PlayerList.clear()
       EnemyList.clear()
       return PlayerList, EnemyList



def load():
        global ScenarioName
        with open(ScenarioName) as file:
                for line in file:
                        global PlayerList      
                        global EnemyList
                        global Timer
                        global MinPlayers
                        arg = line.split(',')
                        if 'Player' in arg:
                               newplayer = Player.Player(arg[1],arg[2],arg[3],arg[4]," ",False)
                               PlayerList.append(newplayer)
                               arg.clear()
                               continue
                        if 'Timer' in arg:
                               Timer = arg[1]
                               arg.clear()
                               continue
                        if 'MinPlayers' in arg:
                               MinPlayers = arg[1]
                               arg.clear()
                               continue
                        if 'Enemy' in arg:
                             global EnemyList
                             enemy1 = Enemy.Enemy(arg[1], arg[2], arg[3], arg[4])
                             EnemyList.append(enemy1)
                             arg.clear()
                             continue
                        if '****' in arg:
                                return EnemyList
                                return Timer
                                return Player
                                return MinPlayers
                        arg.clear()

#Creates the bot
bot = commands.Bot(command_prefix='!', description ='Bot Description WIP', pm_help= True)


#Event Plays when Bot is Online and Connected to Server
@bot.event
async def on_ready():
        print('Logged in as ')
        print(bot.user.name)



@bot.command(pass_context = True)
async def test(ctx):
       arg = ctx.message.content
       await bot.say(arg)
       

       
@bot.command(pass_context = True)
async def say(ctx ,*, say: str):
        await bot.say(say)
        

@bot.command(pass_context = True)
async def aboutme(ctx):
        await bot.say(ctx.message.author)
        await bot.delete_message(ctx.message)

@bot.command(pass_context = True)
async def mInfo(ctx, arg: int):
        global EnemyList
        try:
                await bot.delete_message(ctx.message)
                await bot.say("EnemyName: " + (EnemyList[arg].name))
                await bot.say("HP: " + str(EnemyList[arg].Hp))
                await bot.say("Def: " + str(EnemyList[arg].Def))
                await bot.say("Att: " + str(EnemyList[arg].Att))
                await bot.say("Enemy Can Do: " + str(EnemyList[arg].CalculateDamage())+ " damage")
        except:
                await bot.say("There is no Enemy at that index")

#Create Functions and Commands Below vvv

@bot.command(pass_context = True)
async def playerlist(ctx):
       global Player
       for players in PlayerList:
              await bot.say(players.name)
       


@bot.command(pass_context = True)
async def loadEnemy(ctx):
        try:
                Clear()
                load_Enemy()
                await bot.say(" Enemies have been loaded")
        except:
                await bot.say("load Failed")

@bot.command(pass_context = True)
async def ts(ctx, filename):
        try:
                global isPlaying
                if isPlaying == True:
                       await bot.send_message(ctx.message.author,"Game is currently in session cant switch")
                       await bot.delete_message(ctx.message)
                       return
                global ScenarioName
                f = open(filename,"r")
                if ScenarioName != "":
                        name  = ScenarioName.split(".")    
                        name2 = filename.split(".")
                        await bot.say(name[0] + "  has been switched out for " + name2[0])
                        ScenarioName = filename    
                        try:
                               Clear()
                               load()
                        except:
                               await bot.say(ctx.author.mention + " Scenario was found but failed to load. Check the scenario file to make sure everything is up to standard.")
                        await bot.delete_message(ctx.message)
                        await bot.say(name2[0] + " scenario has been loaded and ready to play")
                        return ScenarioName    
                ScenarioName = filename
                name2 = filename.split(".")
                try:
                               Clear()
                               load()
                except:
                               await bot.say(ctx.author.mention + " Scenario was found but failed to load. Check the scenario file to make sure everything is up to standard.")
                await bot.say(name2[0] + " scenario has been loaded and ready to play")
                await bot.delete_message(ctx.message)
                return ScenarioName
        except:
                await bot.say(ctx.message.author.mention +" "+ filename + " was not found targeted make sure its in the same file path as bot ")

@bot.command(pass_context = True)
async def gameSettings(ctx):
       global MinPlayers
       global Timer
       global ScenarioName
       Name = ScenarioName.split(".")
       if ScenarioName == "":
              await bot.say("There is no Scenario Selected or Loaded. Select a Scenario with the !ts <ScenarioName> command and load it with !loadEnemy command")
              return
       await bot.say("Scenario Name: " + Name[0])
       await bot.say("Timer: " + str(Timer) +" seconds")
       await bot.say("Minimum Required Players: " + str(MinPlayers))
       await bot.delete_message(ctx.message)



@bot.command(pass_context = True)
async def join(ctx):
       global Player
       playernumber = ctx.message.content.split(" ")
       if len(playernumber) > 1:
              newplayernumber = int(playnumber[1])
              index = newplayernumber - 1
              PlayerList[index].ID = ctx.message.author.ID
              PlayerList[Index].hasID = True
              await bot.say(ctx.author.mention + " You Joined in as Player " + str(newplayernumber))
              return PlayerList
       for Players in PlayerList:  
              if Players.hasID == False:
                     Players.ID == ctx.message.author.id
                     Players.hasID == True
                     await bot.say(ctx.author.mention + " You Joined in as Player" + Players.name)
                     return PlayerList
       
              
              
@bot.command(pass_context = True)
async def Play(ctx): 
       global isPlaying
       global MinPlayers
       playercount = int(len(Player))
       if ScenarioName == "":
              await bot.say("There is no Scenario Selected or Loaded. Select a Scenario with the !ts <ScenarioName> command")
              return 
       if playercount < 10:
              await bot.say("Not Enough Players")
              return
       isPlaying == True
       
                
                
#loads the Token
f = open("assets/token.txt","r")
token = f.readline()
bot.run(token)
