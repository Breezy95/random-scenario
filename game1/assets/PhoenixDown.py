import random
import time
import asyncio
import discord
import assets.cogTest
from discord.ext import commands


def setup(bot):
    bot.add_cog(PhoenixDown(bot))

class PhoenixDown:
    def __init__(self,bot):
        self.isActive = False
        self.counter = 0
        self.bot = bot

    def Randomizer(self, pee):
        self.isActive = pee
        return pee

    
    async def downInitializer(self):
        if self.isActive == True:
           await self.bot.say(assets.cogTest.Mycog(self.bot).testvar) 
           await self.bot.say("isActive is" + str(self.isActive))
           await self.bot.say("HI") 
        else:
            await self.bot.say("POO")
   # if __name__ == '__main__':
   #        Down = PhoenixDown()      
       

