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
#List of Enemies
global EnemyList
EnemyList = []
global TempEnemyList
TempEnemyList = []
#List of Players
global PlayerList
PlayerList = []
#Determines the TurnOrder...Is filled in once the game is started
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
#Max Hp for Characters Default is 100
global MaxHp
MaxHp = None
#Determines if you can create a character
global CanCreate
CanCreate = 0
#-----------------------------------

def EmptyPlayers():
    global PlayerList
    count = 0
    for player in PlayerList:
            if PlayerList[count].ID == 0:
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
       global TempEnemyList
       global PlayerList
       global CanCreate
       global MaxHp
       global Timer
       global TurnOrder
       TempEnemyList.clear()
       TurnOrder.clear()
       Timer = 60
       MaxHp = None
       CanCreate = 0
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
                        global MaxHp
                        global CanCreate
                        arg = line.split(",")
                        if 'CanCreate' in arg:
                            CanCreate = int(arg[1])
                            continue
                        if 'MaxHp' in arg:
                            MaxHp = int(arg[1])
                            continue
                        if 'Player' in arg:
                               newplayer = DPlayer.DPlayer(arg[1],int(arg[2]),int(arg[3]),int(arg[4]),0,False)
                               PlayerList.append(newplayer)
                               arg.clear()
                               continue
                        if 'Timer' in arg:
                               Timer = int(arg[1])
                               arg.clear()
                               continue
                        if 'MinPlayers' in arg:
                               MinPlayers = int(arg[1])
                               arg.clear()
                               continue
                        if 'Enemy' in arg:
                             global EnemyList
                             enemy1 = Enemy.Enemy(arg[1], int(arg[2]), int(arg[3]), int(arg[4]))
                             EnemyList.append(enemy1)
                             arg.clear()
                             continue
                        if '****' in arg:
                                return CanCreate
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
        await bot.say("Def: " + EnemyList[arg].Def)
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
async def join(ctx, member : discord.Member, playernumber : int = -1):
       global PlayerList
       count = 0

       if isPlaying == True:
                       await bot.send_message(ctx.message.author,"Game is currently in session cant join")
                       await bot.delete_message(ctx.message)
                       return
                    
       if ctx.message.author.id != member.id:
           await bot.say(ctx.message.author.mention + " You can't choose another member character!")
           return

       for player in PlayerList:
              if ctx.message.author == PlayerList[count].ID:
                     await bot.say("Your already a player Bitch!")
                     await bot.delete_message(ctx.message)
                     return
              count+=1
       if playernumber > 0:
            index = playernumber - 1
            if PlayerList[index].hasID == True:
                     await bot.say(ctx.message.author.mention + " Somebody has chosen that player already. Choose an available player.")
                     return
            PlayerList[index].ID = member
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
                     PlayerList[count].ID = member
                     PlayerList[count].hasID = True
                     await bot.say(ctx.message.author.mention + " You Joined in as Player " + player.name)
                     await bot.delete_message(ctx.message)
                     return PlayerList
       await bot.delete_message(ctx.message)       
       await bot.say(ctx.message.author.mention + " There are no more available players.")

@bot.command(pass_context = True)
async def create(ctx,*,name: str):
       global PlayerList
       global CanCreate
       if isPlaying == True:
                       await bot.send_message(ctx.message.author,"Game is currently in session cant create a character")
                       await bot.delete_message(ctx.message)
                       return
                    
       if CanCreate == 1:
           await bot.say(ctx.message.author.mention + " you can't create Characters for this Scenario")
           return
        
       if CanCreate == True:
           if MaxHp != None:
               newplayer1 = DPlayer.DPlayer(name,MaxHp,random.randint(75,150),random.randint(75,150),0,False)
               PlayerList.append(newplayer1)
               return PlayerList
           if MaxHp == None:
               newplayer1 = DPlayer.DPlayer(name,100,random.randint(75,150),random.randint(75,150),0,False)
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
       if isPlaying == True:
                       await bot.send_message(ctx.message.author,"Game is currently in session cant unjoin from game sorry its not implemented yet")
                       await bot.delete_message(ctx.message)
                       return 
       count = 0
       for player in PlayerList:
              if ctx.message.author == PlayerList[count].ID:
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
       global PlayerList
       global EnemyList
       global TurnOrder
       global Timer
       global isPlaying
       global MinPlayers
       global ScenarioName
       global isPlaying
       global TempEnemyList
       x = '<Start>'
       z = '<End>'

       
       if ScenarioName == "":
              await bot.say("There is no Scenario Selected or Loaded. Select a Scenario with the !ts <ScenarioName> command")
              return
            
       EmptyPlayers()     
       if len(PlayerList) < MinPlayers:
              await bot.say("Not Enough Players")
              return
       isPlaying = True 
       f = open(ScenarioName, "r")
       story = f.readlines()


       
       for n,para in enumerate(story, 0):
              if x in para:
                     place = n+1
              if z in para:
                     place_end = n
                     for y in range(place,place_end):
                         keywordUsed = False



                         
                         #Reads a Line with The <Players> Keyword********************************************************
                         if keywords[0] in story[y]:
                                   names = getname()
                                   story[y] = story[y].replace('<Players>', names)




                         #Reads a Line with <Battle> keyword *****************************************         
                         if keywords[1] in story[y]:
                            story[y] = story[y].replace(keywords[1],"")
                            await bot.say(story[y])
                            arg = story[y].split(" ")
                            arg2 = len(arg) - 1
                            try:
                                numofMonsters  = int(arg[arg2])
                            except:
                                numofMonsters = 100
                            keywordUsed = True
                            for player in PlayerList:
                                TurnOrder.append(player)
                            count = 0
                            for Enemy in EnemyList:
                                if count == numofMonsters:
                                    break
                                TurnOrder.append(Enemy)
                                TempEnemyList.append(Enemy)
                                count+=1
                            random.shuffle(TurnOrder)
                            count = 0
                            battleOn = True


                            
                       #Start Combat code begins here************************************************     
                            while battleOn == True:
                                if count >= len(TurnOrder):
                                    count = 0
                                if len(TempEnemyList) == 0:
                                    battleOn = False
                                    continue
                                if len(PlayerList) == 0:
                                    await bot.say("Your party has been decimated")
                                    return
                                ResetIndex = len(TurnOrder)-1



                                #AI for the enemy on his Turn************************************************
                                if TurnOrder[count].Whoami() == "Enemy":

                                    #Checks if The Enemy is Alive
                                    if TurnOrder[count].isAlive() == False:
                                        await bot.say(TurnOrder[count].name + " is Dead")
                                        TurnOrder.pop(count)
                                        countx = 0
                                        for enemy in EnemyList:
                                            if EnemyList[countx].isAlive() == False:
                                                EnemyList.pop(countx)
                                            countx += 1
                                        countx = 0
                                        for enemy in TempEnemyList:
                                            if TempEnemyList[countx].isAlive() == False:
                                                TempEnemyList.pop(countx)
                                            countx += 1    
                                        if count == ResetIndex:
                                            count = 0
                                            continue
                                        count+=1
                                        continue
                                    
                                    #Checks if theyre only one player in the list
                                    lastindex = len(PlayerList) - 1
                                    if lastindex == -1:
                                        damage = float(TurnOrder[count].CalculateDamage()) - (PlayerList[0].Def * 0.1)
                                        await bot.say(TurnOrder[count].name + " did " + str(damage) +" damage to " + PlayerList[0].name + " with a massive blow!!! ")
                                        if count == ResetIndex:
                                            count = 0
                                            continue
                                        count+=1
                                        continue
                                    
                                    #Attack an random Player
                                    Targetindex = random.randint(0,lastindex)
                                    damage = float(TurnOrder[count].CalculateDamage()) - (PlayerList[Targetindex].Def * 0.1)
                                    PlayerList[Targetindex].Hp = int(PlayerList[Targetindex].Hp - damage)    
                                    await bot.say(TurnOrder[count].name + " did " + str(damage) +" damage to " + PlayerList[Targetindex].name + " with a massive blow!!! ")
                                    if count == ResetIndex:
                                        count = 0
                                        continue
                                    count+=1
                                    continue



                                
                               #Player Controls Begin here***************************************************
                                if TurnOrder[count].Whoami() == "DPlayer":

                                    #Checks if a player is alive
                                    if TurnOrder[count].isAlive() == False:
                                        await bot.say(TurnOrder[count].name + " is Dead")
                                        TurnOrder.pop(count)
                                        countx = 0
                                        for player in PlayerList:
                                            if PlayerList[countx].isAlive() == False:
                                                PlayerList.pop(countx)
                                            countx += 1
                                        if count == ResetIndex:
                                            count = 0
                                            continue
                                        count+=1
                                        continue

                                    #Player Controls
                                    await bot.say(TurnOrder[count].ID.mention + " Its " + TurnOrder[count].name + " turn!!!")

                                    msg = await bot.wait_for_message(timeout = 60, author = TurnOrder[count].ID)



                                    if msg.content == "attack":

                                         Targetindex = random.randint(0,len(TempEnemyList)-1)
                                         damage = float(TurnOrder[count].CalculateDamage()) - (TempEnemyList[Targetindex].Def * 0.1)
                                         TempEnemyList[Targetindex].Hp = int(TempEnemyList[Targetindex].Hp - damage)
                                         await bot.say(TurnOrder[count].name + " did " + str(damage) +" damage to " + TempEnemyList[Targetindex].name + " with a massive blow!!! ")
                                         if count == ResetIndex:
                                            count = 0
                                            continue
                                         count += 1
                                         continue
                                        
                                    if msg.content == "end":
                                         await bot.say("you ended the game")   
                                         return    
                                    continue




                         #Prints Line with no Keywords in it***********************************************
                         if keywordUsed == False:
                             await bot.say(story[y])
                             
       isPlaying = False
       
#loads the Token
f = open("assets/token.txt" ,"r")
token = f.readline()
bot.run(token)
