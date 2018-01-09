import discord
import asyncio
import random
import sys
from discord.ext import commands
from assets import Player
from assets import Enemy





#Global Game Variables
global Enemy
Enemy = []
global Player
Player = []
global Item
Item = []
global loadedP
loadedP = None
#-----------------------------------
def loadP():
          global Player
          global loadedP
          Player = []
          with open("assets/testplayer.txt","r") as f:
                        for line in f:
                                line = line.split(', ')
                                if((line[0])!= 'Player'):
                                        continue #allows skip of line that doesnt start with player
                                else:
                                        Player.append(line[1:]) #[1:] lets you go past first item
                                        loadedP = True
                        return Player
async def assign(ctx):
   global loadedP
   global Player
   if loadedP == True:
                await bot.say('Select your hero')
                for user in range(len(Player)):
                        if user == len(Player)-1 :
                                
                                await bot.say('welp... its just you, enter yes')
                                msgs = await bot.wait_for_message(author=ctx.message.author, content='yes')
                                await bot.say( msgs.author.name + ' you are ' + Player[user][0])
                                Player[user][4] = str(msgs.author.id)
                                Player[int(user)][5] = True
                                break
                        await bot.say('Player {}... choose choose your destiny'.format(user + 1))
                        await bot.say('type yes if you want to be ' + Player[user][0])
                        msg = await bot.wait_for_message(author=ctx.message.author, content='yes')
                        Player[user][4] = str(msg.author.id) #this is for the id
                        Player[int(user)][5] = True  #the 5 value is the boolean hasid
 
                        
   else:
           await bot.say('load players first')
   return Player
                        



#Creates the bot
bot = commands.Bot(command_prefix='!', description ='Bot Description WIP', pm_help= True)


#Event Plays when Bot is Online and Connected to Server


@bot.event
async def on_ready():
        print('Logged in as ')
        print(bot.user.name)
        print("Scenario Bot is Online and ready to fuck your day up")
        
@bot.command(pass_context = True)
async def say(ctx ,*, say: str):
        await bot.say(say)


@bot.command(pass_context = True)
async def test(ctx, arg):
        await bot.say(ctx.message.author)


@bot.command(pass_context = True)
async def aboutme(ctx):
        bot.deleteMessage(ctx.message)
        Myname = ctx.message.author
        bot.say(ctx.message.author)

        
#Create Functions and Commands Below vvv

#loads player from text file
@bot.command(pass_context = True)
async def loadp(ctx):
        try:
                loadP()
                loadedP = True
                await bot.say('Heros loaded')
              
        except:
                await bot.say('Perhaps loadP() didnt work sir')

#assigns player/char/hero to  discord id
@bot.command(pass_context = True)
async def assignP(ctx):
        try:
                await assign(ctx)
        except:
               await bot.say('perhaps something in assign(ctx) sir?') 
     

'''@bot.command(pass_context=True)
async def assignP(arg):
         global x
         hasID = False
         if(loadedP == True):   
                await bot.say(arg + ' players need to be loaded')
                for  p in arg:
                              await bot.say('type yes if you want to be this character')
         else:
                        return await bot.say("something happened")'''

'''@bot.event
async def on_message(message):
    if message.content.startswith('start'):
        await bot.send_message(message.channel, 'Type $stop 4 times. ' + 'id: ' + message.author.id)
        for i in range(4):
            msg = await bot.wait_for_message(author=message.author, content='stop')
            fmt = '{} left to go...'
            await bot.send_message(message.channel, fmt.format(3 - i))

        await bot.send_message(message.channel, 'Good job!')'''


                





#loads the Token
f = open("assets/tokenforFBbot.txt","r")
token = f.readline()
bot.run(token)



                


  



