import discord
import asyncio
import random
from discord.ext import commands
from assets import Enemy



#Global Game Variables
#---------------------------------
global EnemyList
EnemyList = []
global Player
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
#Stores the damage the player will do the enemy
global P2EDamage
#Minimum amount of players needed to start the scenario. Can be Adjuseted in the text file Via MinPlayers <Amount of players> on a line
global MinPlayers
MinPlayers = 1
#-----------------------------------

                
def Clear(): 
       global EnemyList
       global Player
       Player.clear()
       EnemyList.clear()
       return Player, EnemyList



def load_Enemy():
        global ScenarioName
        with open(ScenarioName) as file:
                for line in file:
                        global EnemyList
                        arg = line.split(' ')
                        if 'Enemy' in arg:
                             global EnemyList
                             enemy1 = Enemy.Enemy(arg[1], arg[2], arg[3], arg[4])
                             EnemyList.append(enemy1)
                        if '****' in arg:
                                return EnemyList
                        arg.clear()

#Creates the bot
bot = commands.Bot(command_prefix='!', description ='Bot Description WIP', pm_help= True)


#Event Plays when Bot is Online and Connected to Server
@bot.event
async def on_ready():
        print('Logged in as ')
        print(bot.user.name)

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
                EnemyList[arg].Hp = 20
                await bot.say("EnemyName: " + (EnemyList[arg].name))
                await bot.say("HP: " + str(EnemyList[arg].Hp))
                await bot.say("Def: " + str(EnemyList[arg].Def))
                await bot.say("Att: " + str(EnemyList[arg].Att))
                await bot.say(str(EnemyList[arg].CalculateDamage()))
        except:
                await bot.say("There is no Enemy at that index")

#Create Functions and Commands Below vvv

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
                global ScenarioName
                f = open(filename,"r")
                if ScenarioName != "":
                        await bot.say(ScenarioName + "  is gonna be switched out for " + filename)
                        ScenarioName = filename
                        return ScenarioName
                ScenarioName = filename
                await bot.say(filename + " has been targeted and ready to load")
                return ScenarioName
        except:
                await bot.say(ctx.message.author.mention +" "+ filename + " was not found/ targeted make sure its in the same file path as bot ")

@bot.command(pass_context = True)
async def attack(ctx):
       global isPlaying
       if isPlaying == False:
             await bot.say("There is no game currently running")



@bot.command(pass_context = True)
async def defend(ctx):
       global isPlaying
       if isPlaying == False:
             await bot.say("There is no game currently running")
              

                
                
#loads the Token
f = open("assets/token.txt","r")
token = f.readline()
bot.run(token)
