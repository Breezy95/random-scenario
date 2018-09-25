import discord
from discord.ext import commands
import assets.PhoenixDown

class Mycog:
    def __init__(self,bot):
        self.bot = bot
        #await self.bot.say("class instantiated")
        self.Down = assets.PhoenixDown.PhoenixDown(bot)
        self.testvar = 45454545545
        print("class created in Mycog class")

    async def receiveList(self, list):
        await self.bot.say(str(list[1]))



    async def downActions(self):
        await self.Down.downInitializer()
        await self.bot.say("is active is " + str(self.Down.isActive))
        await self.bot.say(self.Down.Randomizer(False))
        await self.Down.downInitializer()
        await self.bot.say(self.Down.Randomizer(True))
        await self.Down.downInitializer()
    
    def listss(self):
        return [1,2,3]

    async def math(self):
        x = self.listss()
        await self.bot.say(x[1])

    def mycom(self):
        print("I can do stuff!")

def setup(bot):
    bot.add_cog(Mycog(bot))


if __name__ == '__main__':
    print("HE")
    sa = Mycog()
    sa.math()
    sa.Down.downInitializer()