import discord
import asyncio
import random
import time
from discord.ext import commands
from assets import DPlayer
from assets import Enemy



description = "HELLO im Scenario Bot made by Ethan and Fabrice." \
              "The Commands are listed below."\
              "\n HOW TO CREATE A SCENARIO------------------------"\
              "\n Create a new text file the name of the Textfile will be the name of your scenario"\
              " The begining of the text file should start by defining the options, players, enemeies found in the scenario."\
              "\n DECLARING ENEMIES AND PLAYERS-----------------------"\
              "\n Begin a Line With Enemy to declare an Enemy. Use a comma to seperate each attribute. "\
              "Enemy, <name>, <Hp>, <Def>, <Att>. Ex. Enemy, Bob Ross, 100, 100, 100 "\
              "\n Declare Players the same with begin a line with Player"\
              "\n Player, <name>, <Hp>, <Def>, <Att>. Ex. Player, Joeseph, 100, 100, 100,"\
              "\n CUSTOMIZING OPTIONS--------------------"\
              "\n You can customize the amount a time a turn takes, the min and max amount of players needed to play."\
              "\n Begin a line with Timer followed by a comma and the amount of time in seconds"\
              "\n Timer, <amount of time>. ex Timer, 60"\
              "\n Begin a line with MinPlayers or MaxPlayers followed by a comma and the amount of players"\
              "\n MinPlayers, <amount of players>. MinPlayers, 6"

prefix = ['!','?','/','@']

#Global Game Variables
#---------------------------------
global EnemyList
EnemyList = []
global PlayerList
PlayerList = []
global TurnOrder
TurnOrder = []
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

def EmptyPlayers():
    global PlayerList
    count = 0
    for player in PlayerList:
            if PlayerList[count].ID == '':
                PlayerList.pop(count)
                count+=1
                continue
            count+=1
    return PlayerList


def getname():
    global PlayerList
    blank = ""
    count = 0
    for Player in PlayerList:
        if count > 0:
            if len(PlayerList) == 2:
                blank = PlayerList[0].name
                blank += " and "
                blank += PlayerList[1].name
                return blank
            and_index = len(PlayerList) - 2
            if count == and_index:
                blank += ", "
                blank += PlayerList[count].name
                blank += " and "
                count+=1
                continue
            last_index = len(PlayerList) - 1 
            if count == last_index:
                blank += PlayerList[count].name
                return blank
            blank += ", "
            blank += PlayerList[count].name
            count+=1
            continue
        blank = PlayerList[count].name
        count+=1
    return blank


       
       

       
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
                        arg = line.split(",")
                        if 'Player' in arg:
                               newplayer = DPlayer.DPlayer(arg[1],arg[2],arg[3],arg[4]," ",False)
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
                                return PlayerList
                                return MinPlayers
                        arg.clear()

#Creates the bot
bot = commands.Bot(command_prefix= prefix, description = description, pm_help= True)


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
async def mInfo(ctx, arg: int):
        global EnemyList
        await bot.delete_message(ctx.message)
        Enemy1 = EnemyList[arg]
        await bot.say("EnemyName: " + (EnemyList[arg].name))
        await bot.say("HP: " + str(EnemyList[arg].Hp))
        await bot.say("Def: " + str(EnemyList[arg].Def))
        await bot.say("Att: " + str(EnemyList[arg].Att))
        await bot.say("Enemy Can Do: " + str(Enemy1.CalculateDamage()) + " damage")
       

#Create Functions and Commands Below vvv

@bot.command(pass_context = True)
async def playerlist(ctx):
       global PlayerList
       await bot.delete_message(ctx.message)
       for players in PlayerList:
              await bot.say(players.name)
              await bot.say("hasID: " + str(players.hasID))
              await bot.say("HP: " + str(players.Hp))
              await bot.say("Def: " + str(players.Def))
              await bot.say("Att: " + str(players.Att))
              
       


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
                        Clear()
                        load()
                        await bot.delete_message(ctx.message)
                        await bot.say(name2[0] + " scenario has been loaded and ready to play")
                        return ScenarioName    
                ScenarioName = filename
                name2 = filename.split(".")
                Clear()
                load()
                await bot.say(name2[0] + " scenario has been loaded and ready to play")
                await bot.delete_message(ctx.message)
                if len(PlayerList) < 1:
                       await bot.say("There are no pre-defined players. Create players for the scenario with the !create <Playername> command. Enjoy the game!")
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
       global PlayerList
       count = 0
       for player in PlayerList:
              if ctx.message.author == PlayerList[count].ID:
                     await bot.say("Your already a player Bitch!")
                     await bot.delete_message(ctx.message)
                     return
              count+=1
       playernumber = ctx.message.content.split(" ")
       if len(playernumber) > 1:
              newplayernumber = int(playernumber[1])
              index = newplayernumber - 1
              if PlayerList[index].hasID == True:
                     await bot.say(ctx.message.author.mention + " Somebody has chosen that player already. Choose an available player.")
                     return
              PlayerList[index].ID = ctx.message.author
              PlayerList[index].hasID = True
              await bot.say(ctx.message.author.mention + " You Joined in as Player " + PlayerList[index].name)
              await bot.delete_message(ctx.message)
              return PlayerList
       count = 0       
       for player in PlayerList:  
              if PlayerList[count].hasID == True:
                     count +=1
                     continue
              if PlayerList[count].hasID == False:
                     PlayerList[count].ID = ctx.message.author.id
                     PlayerList[count].hasID = True
                     await bot.say(ctx.message.author.mention + " You Joined in as Player " + player.name)
                     await bot.delete_message(ctx.message)
                     return PlayerList
       await bot.delete_message(ctx.message)       
       await bot.say(ctx.message.author.mention + " There are no more available players.")

@bot.command(pass_context = True)
async def create(ctx,*,name: str):
       global PlayerList
       newplayer1 = DPlayer.DPlayer(name,100,random.randint(75,150),random.randint(75,150),"",False)
       PlayerList.append(newplayer1)
       return PlayerList
       
              
@bot.command(pass_context = True)
async def Play(ctx): 
       global isPlaying
       global MinPlayers
       global ScenarioName
       playercount = int(len(PlayerList))
       if ScenarioName == "":
              await bot.say("There is no Scenario Selected or Loaded. Select a Scenario with the !ts <ScenarioName> command")
              return 
       if playercount < 0:
              await bot.say("Not Enough Players")
              return
       isPlaying == True
                
               
       
@bot.command(pass_context = True)
async def unjoin(ctx):
       global PlayerList
       count = 0
       for player in PlayerList:
              if ctx.message.author.id == PlayerList[count].ID:
                     PlayerList[count].ID = ''
                     PlayerList[count].hasID = False
                     await bot.say(ctx.message.author.mention + " You are no longer " + PlayerList[count].name )
                     await bot.delete_message(ctx.message)
                     return
              count+=1
       await bot.say(ctx.message.author.mention + " You are not in the game")


keywords = ['<Players>','<Battle>']
@bot.command(pass_context = True)
async def start(ctx):
       x = '<Start>'
       z = '<End>'
       f = open("assets/Test.txt", "r")
       story = f.readlines()
       global PlayerList
       global EnemyList
       global TurnOrder
       for n,para in enumerate(story, 0):
              if x in para:
                     place = n+1
              if z in para:
                     place_end = n
                     for y in range(place,place_end):
                         keywordUsed = False
                         if keywords[0] in story[y]:
                                   names = getname()
                                   story[y] = story[y].replace('<Players>', names)
                                   await bot.say(story[y])
                                   keywordUsed = True
                         if keywords[1] in story[y]:
                            story[y] = story[y].replace(keywords[1],"")
                            await bot.say(story[y])
                            keywordUsed = True
                            for player in PlayerList:
                                TurnOrder.append(player)
                            for Enemy in EnemyList:
                                TurnOrder.append(Enemy)
                            random.shuffle(TurnOrder)
                            #for turn in TurnOrder:
                         if keywordUsed == False:
                             await bot.say(story[y])
                             
             
                                       
#loads the Token
f = open("assets/token.txt" ,"r")
token = f.readline()
bot.run(token)
