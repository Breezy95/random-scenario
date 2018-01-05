import discord
import asyncio
import random
from discord.ext import commands



#Global Game Variables
global Enemy
Enemy = []
global Player
Player = []
global Item
Item = []
#-----------------------------------




#Creates the bot
bot = commands.Bot(command_prefix='!', description ='Bot Description WIP', pm_help= True)


#Event Plays when Bot is Online and Connected to Server
@bot.event
async def on_ready():
        print('Logged in as ')
        print(bot.user.name)
        bot.say("Scenario Bot is Online and ready for some order's")

@bot.command(pass_context = True)
async def say(ctx ,*, say: str):
        await bot.say(say)


@bot.command(pass_context = True)
async def test(ctx, arg):
        await bot.say(ctx.message.author)


@bot.command()
async def aboutme(ctx):
        bot.deleteMessage(ctx.message)
        Myname = ctx.message.author
        bot.say(ctx.message.author)



#Create Functions and Commands Below vvv

#loads the Token
f = open("assets/token.txt","r")
token = f.readline()
bot.run(token)
